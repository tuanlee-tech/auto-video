"""
Video Watermark Remover using Reverse Alpha Blending & Contour Laplace Diffusion.
Directly implements Google Flow Extension's native mathematical formulation for video.

Zero zoom. Zero crop. Zero vertical smudging.
100% native frame preservation (1280x720, 1920x1080, etc.).
"""

import os
import sys
import subprocess
import cv2
import numpy as np

# Path to the 48x48 Google diamond watermark template
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'google_watermark_48.png')

class VideoWatermarkRemover:
    def __init__(self, template_path=None):
        if template_path is None:
            template_path = TEMPLATE_PATH
            
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Watermark template not found at {template_path}")
            
        tmpl_img = cv2.imread(template_path)
        if tmpl_img is None:
            raise ValueError(f"Failed to read template image from {template_path}")
            
        # JS formulation: max(R, G, B) / 255.0
        self.tmpl_48 = np.max(tmpl_img, axis=2).astype(np.float64) / 255.0
        self._cached_templates = {}

    def _get_template_and_edge_mask(self, scale):
        scale_key = round(scale, 3)
        if scale_key in self._cached_templates:
            return self._cached_templates[scale_key]
            
        size = int(round(48 * scale))
        tmpl = cv2.resize(self.tmpl_48, (size, size), interpolation=cv2.INTER_LINEAR)
        
        # Sobel edge gradient (> 0.15) dilated by 3x3 kernel (exact nr(n, a) from extension)
        padded = np.pad(tmpl, 1, mode='edge')
        gx = (padded[0:-2, 2:] + 2*padded[1:-1, 2:] + padded[2:, 2:]) - \
             (padded[0:-2, 0:-2] + 2*padded[1:-1, 0:-2] + padded[2:, 0:-2])
        gy = (padded[2:, 0:-2] + 2*padded[2:, 1:-1] + padded[2:, 2:]) - \
             (padded[0:-2, 0:-2] + 2*padded[0:-2, 1:-1] + padded[0:-2, 2:])
        grad = np.abs(gx) + np.abs(gy)
        edge = (grad > 0.15).astype(np.uint8)
        edge_dilated = cv2.dilate(edge, np.ones((3, 3), np.uint8), iterations=1)
        
        entry = (tmpl, size, edge_dilated)
        self._cached_templates[scale_key] = entry
        return entry

    @staticmethod
    def _laplace_diffusion(image_patch, mask, iterations=40):
        """
        Fast Laplace diffusion smoothing (equivalent to ot in extension).
        Initializes boundary colors then performs vectorized 4-neighbor averaging.
        """
        patch_u8 = np.clip(image_patch * 255.0, 0, 255).astype(np.uint8)
        inited = cv2.inpaint(patch_u8, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA).astype(np.float64) / 255.0
        
        m_inner = mask.copy()
        m_inner[0, :] = 0; m_inner[-1, :] = 0
        m_inner[:, 0] = 0; m_inner[:, -1] = 0
        m_bool = m_inner == 1
        
        s = inited
        for _ in range(iterations):
            avg = 0.25 * (s[:-2, 1:-1] + s[2:, 1:-1] + s[1:-1, :-2] + s[1:-1, 2:])
            s[1:-1, 1:-1] = np.where(m_bool[1:-1, 1:-1], avg, s[1:-1, 1:-1])
            
        return s

    def detect_watermark_geometry(self, frame):
        """
        Calculates exact deterministic coordinates based on frame dimensions:
        Scale S = height / 720.0
        Margin = 96 * S
        Size = 48 * S
        (x0, y0) = (W - margin - size, H - margin - size)
        """
        h_f, w_f = frame.shape[:2]
        scale = h_f / 720.0
        template, size, edge_mask = self._get_template_and_edge_mask(scale)
        
        margin = int(round(96 * scale))
        x0 = w_f - margin - size
        y0 = h_f - margin - size
        
        # Search in small window [-6, +6] around expected location for peak NCC
        crop_y0 = max(0, y0 - int(round(8 * scale)))
        crop_y1 = min(h_f, y0 + size + int(round(8 * scale)))
        crop_x0 = max(0, x0 - int(round(8 * scale)))
        crop_x1 = min(w_f, x0 + size + int(round(8 * scale)))
        
        crop_gray = cv2.cvtColor(frame[crop_y0:crop_y1, crop_x0:crop_x1], cv2.COLOR_BGR2GRAY)
        tmpl_u8 = (template * 255.0).astype(np.uint8)
        
        if crop_gray.shape[0] >= tmpl_u8.shape[0] and crop_gray.shape[1] >= tmpl_u8.shape[1]:
            res = cv2.matchTemplate(crop_gray, tmpl_u8, cv2.TM_CCOEFF_NORMED)
            min_v, max_v, _, max_loc = cv2.minMaxLoc(res)
            if max_v > 0.45: # High confidence match found
                x0 = crop_x0 + max_loc[0]
                y0 = crop_y0 + max_loc[1]
                
        return {
            'x0': x0,
            'y0': y0,
            'size': size,
            'scale': scale,
            'template': template,
            'edge_mask': edge_mask
        }

    def clean_frame(self, frame, geom, prev_J=None):
        """
        Cleans watermark from a single BGR frame using:
        1. Least-squares background diffusion estimation (ot)
        2. Reverse Alpha Blending (Je) with temporal smoothing
        3. Contour Laplace smoothing (ir) on star boundaries
        """
        x0 = geom['x0']
        y0 = geom['y0']
        size = geom['size']
        scale = geom['scale']
        template = geom['template']
        edge_mask = geom['edge_mask']
        h_f, w_f = frame.shape[:2]
        
        # Copy only the watermark work region plus padding
        pad = int(round(12 * scale))
        x_p0 = max(0, x0 - pad)
        y_p0 = max(0, y0 - pad)
        x_p1 = min(w_f, x0 + size + pad)
        y_p1 = min(h_f, y0 + size + pad)
        
        work_patch = frame[y_p0:y_p1, x_p0:x_p1].astype(np.float64)
        
        mask_bg = np.zeros((y_p1 - y_p0, x_p1 - x_p0), dtype=np.uint8)
        sy = y0 - y_p0
        sx = x0 - x_p0
        mask_bg[sy:sy+size, sx:sx+size] = (template > 0.02).astype(np.uint8)
        
        # 1. Estimate optimal alpha blend factor per channel
        blend_factors = []
        for c in range(3):
            p = work_patch[:, :, c] / 255.0
            bg_est = self._laplace_diffusion(p, mask_bg, iterations=40)
            
            w_obs = p[sy:sy+size, sx:sx+size]
            E_bg = bg_est[sy:sy+size, sx:sx+size]
            M_eff = template * (1.0 - E_bg)
            
            num = np.sum((w_obs - E_bg) * M_eff)
            den = np.sum(M_eff * M_eff)
            factor = num / den if den > 1e-6 else 0.0
            blend_factors.append(factor)
            
        curr_B = float(np.mean(blend_factors))
        curr_J = min(0.62, max(0.20, curr_B + 0.05))
        
        # Temporal smoothing: EMA prevents brightness breathing between frames
        if prev_J is not None:
            J = 0.80 * prev_J + 0.20 * curr_J
        else:
            J = curr_J
            
        # 2. Reverse Alpha Blending (Je)
        star_patch = work_patch[sy:sy+size, sx:sx+size].copy()
        m = np.clip(template * J, 0.0, 0.99)
        m_mask = m >= 0.002
        denom = 1.0 - m
        
        for c in range(3):
            orig_val = (star_patch[:, :, c] - m * 255.0) / denom
            star_patch[:, :, c] = np.where(m_mask, np.clip(orig_val, 0.0, 255.0), star_patch[:, :, c])
            
        work_patch[sy:sy+size, sx:sx+size] = star_patch
        
        # 3. Contour Laplace smoothing (ir) on the 1px Sobel boundary
        pad_edge = int(round(8 * scale))
        x_e0 = max(0, x0 - pad_edge)
        y_e0 = max(0, y0 - pad_edge)
        x_e1 = min(w_f, x0 + size + pad_edge)
        y_e1 = min(h_f, y0 + size + pad_edge)
        
        full_edge_mask = np.zeros((y_e1 - y_e0, x_e1 - x_e0), dtype=np.uint8)
        esy = y0 - y_e0
        esx = x0 - x_e0
        full_edge_mask[esy:esy+size, esx:esx+size] = edge_mask
        
        edge_work = frame[y_e0:y_e1, x_e0:x_e1].astype(np.float64)
        # Update edge_work with the reverse-alpha blended result
        diff_y0 = y0 - y_e0
        diff_x0 = x0 - x_e0
        edge_work[diff_y0:diff_y0+size, diff_x0:diff_x0+size] = star_patch
        
        for c in range(3):
            ep = edge_work[:, :, c] / 255.0
            diffused_edge = self._laplace_diffusion(ep, full_edge_mask, iterations=30)
            edge_work[:, :, c] = diffused_edge * 255.0
            
        # Put back into output frame (only this local region is modified, 99.8% of frame is untouched)
        out_frame = frame.copy()
        out_frame[y_e0:y_e1, x_e0:x_e1] = np.clip(np.round(edge_work), 0, 255).astype(np.uint8)
        return out_frame, J

    def process_video(self, input_path, output_path, crf=17):
        """
        Processes an entire video file, writing visually lossless MP4.
        Preserves 100% original dimensions, framerate, and audio track.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input video not found: {input_path}")
            
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {input_path}")
            
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"[*] Processing Video: {os.path.basename(input_path)}")
        print(f"    Resolution: {w}x{h}, FPS: {fps:.2f}, Frames: {total_frames}")
        
        # Read first frame to detect watermark geometry
        ret, first_frame = cap.read()
        if not ret:
            cap.release()
            raise ValueError("Failed to read first frame from video")
            
        geom = self.detect_watermark_geometry(first_frame)
        print(f"    Watermark detected at (x={geom['x0']}, y={geom['y0']}), size={geom['size']}x{geom['size']}")
        
        # Release and reopen video capture to avoid codec rewind bugs
        cap.release()
        cap = cv2.VideoCapture(input_path)
        
        # Prepare FFmpeg pipe for visually lossless export
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        temp_video = output_path + ".temp.mp4"
        
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f"{w}x{h}",
            '-pix_fmt', 'bgr24',
            '-r', str(fps),
            '-i', '-',
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-crf', str(crf),
            '-pix_fmt', 'yuv420p',
            temp_video
        ]
        
        # Avoid pipe deadlock: redirect stderr to DEVNULL or log file
        log_file = output_path + ".ffmpeg.log"
        with open(log_file, 'wb') as ffmpeg_err:
            proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=ffmpeg_err)
            
            prev_J = None
            frame_idx = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                clean_f, prev_J = self.clean_frame(frame, geom, prev_J)
                proc.stdin.write(clean_f.tobytes())
                
                frame_idx += 1
                if frame_idx % 15 == 0 or frame_idx == total_frames:
                    pct = (frame_idx / total_frames) * 100 if total_frames > 0 else 0
                    print(f"    Progress: {frame_idx}/{total_frames} frames ({pct:.1f}%)", flush=True)
                    
            print(f"    Progress: {frame_idx}/{total_frames} frames (100.0%)", flush=True)
            cap.release()
            proc.stdin.close()
            proc.wait()
            
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
            except Exception:
                pass
                
        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg encoding failed with return code {proc.returncode}")
            
        # Check if original video had audio stream; if so, mux audio into output
        has_audio = self._check_audio_stream(input_path)
        if has_audio:
            mux_cmd = [
                'ffmpeg', '-y',
                '-i', temp_video,
                '-i', input_path,
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-map', '0:v:0',
                '-map', '1:a:0?',
                output_path
            ]
            subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if os.path.exists(temp_video):
                os.remove(temp_video)
        else:
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_video, output_path)
            
        print(f"[+] SUCCESS: Cleaned video exported to {output_path} ({os.path.getsize(output_path) // 1024} KB)")
        return output_path

    @staticmethod
    def _check_audio_stream(video_path):
        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'a',
            '-show_entries', 'stream=codec_type',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return len(res.stdout.strip()) > 0
        except Exception:
            return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Remove Google Flow watermark from video cleanly")
    parser.add_argument('input', help="Path to input video file")
    parser.add_argument('-o', '--output', help="Path to output cleaned video file")
    parser.add_argument('--crf', type=int, default=17, help="FFmpeg CRF quality (default 17)")
    args = parser.parse_args()
    
    out_path = args.output
    if not out_path:
        base, ext = os.path.splitext(args.input)
        out_path = f"{base}_cleaned{ext}"
        
    remover = VideoWatermarkRemover()
    remover.process_video(args.input, out_path, crf=args.crf)

if __name__ == '__main__':
    main()
