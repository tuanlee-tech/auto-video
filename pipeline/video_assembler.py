import os
import sys
import glob
import json
import time
import subprocess
import cv2
import numpy as np
from typing import List, Dict, Any, Optional
from pipeline.config import PipelineConfig, DEFAULT_CONFIG

def hex_to_bgr(hex_str: str) -> tuple:
    hex_str = hex_str.lstrip("#")
    r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
    return (b, g, r)

def load_and_fit_image(img_path: str, target_w: int, target_h: int, bg_bgr: tuple) -> np.ndarray:
    """Loads image and fits within target resolution with background padding if needed."""
    img = cv2.imread(img_path)
    if img is None:
        # Create empty placeholder canvas with cream background
        canvas = np.full((target_h, target_w, 3), bg_bgr, dtype=np.uint8)
        cv2.putText(canvas, f"Missing: {os.path.basename(img_path)}", (100, target_h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50, 50, 50), 2)
        return canvas

    ih, iw = img.shape[:2]
    scale = min(target_w / iw, target_h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC)

    canvas = np.full((target_h, target_w, 3), bg_bgr, dtype=np.uint8)
    ox = (target_w - nw) // 2
    oy = (target_h - nh) // 2
    canvas[oy:oy+nh, ox:ox+nw] = resized
    return canvas

def apply_ken_burns(canvas: np.ndarray, progress: float, max_zoom: float = 1.04) -> np.ndarray:
    """
    Subtle Ken Burns slow zoom (progress from 0.0 to 1.0).
    Zooms smoothly toward the center.
    """
    if max_zoom <= 1.001:
        return canvas

    h, w = canvas.shape[:2]
    # Ease-in-out or linear scale
    current_scale = 1.0 + (max_zoom - 1.0) * progress
    
    crop_w = int(w / current_scale)
    crop_h = int(h / current_scale)
    x1 = (w - crop_w) // 2
    y1 = (h - crop_h) // 2
    cropped = canvas[y1:y1+crop_h, x1:x1+crop_w]
    return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)

def overlay_watermark(frame: np.ndarray, watermark_img: np.ndarray, x: int = 50, y: int = 50) -> np.ndarray:
    """Overlays transparent watermark PNG onto frame."""
    if watermark_img is None or watermark_img.shape[2] != 4:
        return frame
        
    wh, ww = watermark_img.shape[:2]
    fh, fw = frame.shape[:2]
    if y + wh > fh or x + ww > fw:
        return frame
        
    alpha = (watermark_img[:, :, 3] / 255.0)[:, :, np.newaxis]
    wm_rgb = watermark_img[:, :, :3]
    
    roi = frame[y:y+wh, x:x+ww]
    frame[y:y+wh, x:x+ww] = (1.0 - alpha) * roi + alpha * wm_rgb
    return frame

def find_image_for_cut(images_dir: str, cut_info: Dict[str, Any], cut_index: int) -> Optional[str]:
    """Finds image matching cut by cut_id, scene_id, or sorted index."""
    cut_id = cut_info.get("cut_id", cut_index + 1)
    scene_id = cut_info.get("scene_id", f"{cut_id:04d}")
    expected_name = cut_info.get("expected_image_name", "")

    candidates = [
        os.path.join(images_dir, f"{cut_id}.png"),
        os.path.join(images_dir, f"{cut_id}.jpg"),
        os.path.join(images_dir, f"{cut_id:04d}.png"),
        os.path.join(images_dir, f"{cut_id:04d}.jpg"),
        os.path.join(images_dir, f"{scene_id}.png"),
        os.path.join(images_dir, expected_name) if expected_name else None
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c

    # Pattern search e.g. 1_*.* or 001_*.* or 0001_*.*
    matches = glob.glob(os.path.join(images_dir, f"{cut_id}_*.*")) + \
              glob.glob(os.path.join(images_dir, f"*{cut_id:03d}*.*")) + \
              glob.glob(os.path.join(images_dir, f"*{cut_id:04d}*.*"))
    if matches:
        return matches[0]

    # Fallback to sorted index if available
    all_imgs = sorted(glob.glob(os.path.join(images_dir, "*.png")) + glob.glob(os.path.join(images_dir, "*.jpg")))
    if cut_index < len(all_imgs):
        return all_imgs[cut_index]

    return None

def test_encoder(encoder_name: str) -> bool:
    """Tests if an FFmpeg encoder works on this system."""
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-f", "lavfi", "-i", "color=c=black:s=64x64:d=0.1",
        "-c:v", encoder_name,
        "-f", "null", "-"
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False

def get_best_encoder(prefer_gpu: bool = True) -> tuple:
    """Returns (encoder_name, preset_and_quality_args)."""
    if prefer_gpu and test_encoder("h264_nvenc"):
        return ("h264_nvenc", ["-preset", "p4", "-cq", "20"])
    # CPU fallback (universal, very fast for slides/doodles)
    return ("libx264", ["-preset", "veryfast", "-crf", "18"])

def assemble_video(
    audio_path: str,
    images_dir: str,
    manifest_path: str,
    output_path: str,
    config: PipelineConfig = DEFAULT_CONFIG,
    bgm_path: Optional[str] = None,
    watermark_path: Optional[str] = None,
    use_gpu: bool = True
) -> str:
    """
    Assembles 1080p/4K video by streaming frames into FFmpeg with Ken Burns and Cross-Dissolve.
    """
    t0 = time.time()
    width = config.width
    height = config.height
    fps = config.fps
    bg_bgr = hex_to_bgr(config.bg_color_hex)
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest: List[Dict[str, Any]] = json.load(f)
        
    if not manifest:
        raise ValueError("B-roll manifest is empty!")
        
    print(f"[Assembler] Assembling video at {width}x{height} @ {fps}fps...")
    print(f" -> Found {len(manifest)} B-roll cuts in timeline.")
    
    # Load watermark if exists
    watermark_img = None
    if watermark_path and os.path.exists(watermark_path):
        watermark_img = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)
        print(f" -> Loaded watermark from: {watermark_path}")

    # Build FFmpeg command with best available encoder
    encoder, enc_opts = get_best_encoder(use_gpu)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Audio input handling (voice + optional BGM ducking)
    has_bgm = bgm_path and os.path.exists(bgm_path)
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "bgr24",
        "-r", str(fps),
        "-i", "-"  # Video pipe from stdin
    ]
    
    if has_bgm:
        ffmpeg_cmd.extend([
            "-i", audio_path,
            "-stream_loop", "-1", "-i", bgm_path,
            "-filter_complex",
            f"[1:a]volume=1.0[voice];[2:a]volume={config.bgm_volume_ducked}[bgm];[voice][bgm]amix=inputs=2:duration=first[aout]",
            "-map", "0:v",
            "-map", "[aout]"
        ])
    else:
        ffmpeg_cmd.extend([
            "-i", audio_path,
            "-map", "0:v",
            "-map", "1:a"
        ])
        
    ffmpeg_cmd.extend([
        "-c:v", encoder,
        "-pix_fmt", "yuv420p"
    ])
    ffmpeg_cmd.extend(enc_opts)
        
    ffmpeg_cmd.extend([
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ])
    
    print(f" -> Launching FFmpeg with encoder: {encoder}")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    transition_frames = max(1, int(config.transition_duration * fps))
    total_cuts = len(manifest)

    # Preload and cache first scene image
    first_img_path = find_image_for_cut(images_dir, manifest[0], 0)
    current_canvas = load_and_fit_image(first_img_path or "", width, height, bg_bgr)
    
    total_frames_written = 0
    
    for i, cut in enumerate(manifest):
        dur = cut["duration"]
        scene_frames = max(1, int(dur * fps))
        
        # Prepare next canvas for transition
        next_canvas = None
        if i + 1 < total_cuts:
            next_img_path = find_image_for_cut(images_dir, manifest[i + 1], i + 1)
            next_canvas = load_and_fit_image(next_img_path or "", width, height, bg_bgr)
            
        hold_frames = max(0, scene_frames - transition_frames) if next_canvas is not None else scene_frames

        # 1. Render hold phase (with subtle Ken Burns zoom)
        for f_idx in range(hold_frames):
            progress = f_idx / max(1, scene_frames)
            frame = apply_ken_burns(current_canvas, progress, config.ken_burns_zoom)
            if watermark_img is not None:
                frame = overlay_watermark(frame, watermark_img)
            proc.stdin.write(frame.tobytes())
            total_frames_written += 1

        # 2. Render transition phase (Cross-dissolve to next canvas)
        if next_canvas is not None:
            for t_idx in range(transition_frames):
                alpha = t_idx / float(transition_frames)
                curr_frame = apply_ken_burns(current_canvas, (hold_frames + t_idx) / scene_frames, config.ken_burns_zoom)
                next_frame = apply_ken_burns(next_canvas, 0.0, config.ken_burns_zoom)
                
                # Blend frames
                blended = cv2.addWeighted(curr_frame, 1.0 - alpha, next_frame, alpha, 0)
                if watermark_img is not None:
                    blended = overlay_watermark(blended, watermark_img)
                    
                proc.stdin.write(blended.tobytes())
                total_frames_written += 1
                
            current_canvas = next_canvas

        if (i + 1) % 10 == 0 or (i + 1) == total_cuts:
            pct = ((i + 1) / total_cuts) * 100
            print(f" [Rendering] Scene {i + 1}/{total_cuts} ({pct:.1f}%) processed...")

    proc.stdin.close()
    proc.wait()
    
    elapsed = time.time() - t0
    fps_speed = total_frames_written / max(0.1, elapsed)
    print(f"[Assembler] Done! Rendered {total_frames_written} frames in {elapsed:.1f}s ({fps_speed:.1f} fps).")
    print(f" -> Output Video: {output_path}")
    return output_path
