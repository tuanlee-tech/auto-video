import os
import re
import json
import soundfile as sf
from typing import List, Dict, Any, Optional
from pipeline.models import SceneBeat, ProjectConfig

def clean_token(token: str) -> str:
    return re.sub(r"[^\w]", "", token.lower())

def extract_master_timings_and_align(
    beats: List[SceneBeat],
    config: ProjectConfig,
    audio_path: str,
    timings_dir: str,
    model_name: str = "base"
) -> List[SceneBeat]:
    """
    Transcribes master_narration.wav using faster-whisper with word-level timestamps:
    - Segments the continuous audio into precise scene boundaries for all SceneBeats.
    - Exports <cảnh>_timing.json for each scene beat with relative millisecond offsets.
    - Exports master_timing.json with full project timeline.
    - Dynamically computes scene duration_sec, duration_frames, and from_frame.
    """
    from faster_whisper import WhisperModel

    os.makedirs(timings_dir, exist_ok=True)
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Master audio not found: {audio_path}")

    # Read audio info
    audio_info = sf.info(audio_path)
    total_audio_ms = int(round(audio_info.duration * 1000))

    print(f"[WhisperEngine] Initializing faster-whisper (Model: {model_name}, Device: CPU, Compute: int8)...")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")

    print(f"[WhisperEngine] Transcribing Master Audio ({audio_info.duration:.2f}s) with word timestamps...")
    segments, _ = model.transcribe(
        audio_path,
        language="vi",
        word_timestamps=True,
        beam_size=5
    )

    all_whisper_words = []
    for segment in segments:
        if segment.words:
            for w in segment.words:
                all_whisper_words.append({
                    "word": w.word.strip(),
                    "start_ms": int(round(w.start * 1000)),
                    "end_ms": int(round(w.end * 1000))
                })

    print(f"[WhisperEngine] Detected {len(all_whisper_words)} spoken words across master track.")

    # Collect script words per beat
    script_beats_words = []
    total_script_words = 0
    for beat in beats:
        tokens = [w for w in beat.spoken_text.split() if w.strip()]
        script_beats_words.append(tokens)
        total_script_words += len(tokens)

    # Monotonic alignment of Whisper words to each scene beat
    whisper_ptr = 0
    total_whisper_words = len(all_whisper_words)

    # Pre-calculate start and end indices for each beat in all_whisper_words
    beat_word_slices = []
    for beat_idx, tokens in enumerate(script_beats_words):
        num_tokens = len(tokens)
        if total_script_words > 0:
            target_whisper_count = max(1, int(round((num_tokens / total_script_words) * total_whisper_words)))
        else:
            target_whisper_count = num_tokens

        start_w_idx = whisper_ptr
        end_w_idx = min(start_w_idx + target_whisper_count, total_whisper_words)
        
        # If last beat, take all remaining words
        if beat_idx == len(beats) - 1:
            end_w_idx = total_whisper_words

        beat_word_slices.append((start_w_idx, end_w_idx))
        whisper_ptr = end_w_idx

    # Assign boundaries and build timings
    current_frame_accum = 0

    for i, beat in enumerate(beats):
        tokens = script_beats_words[i]
        start_w_idx, end_w_idx = beat_word_slices[i]
        w_slice = all_whisper_words[start_w_idx:end_w_idx]

        # Determine absolute start_ms and end_ms for this scene
        if w_slice:
            abs_start_ms = w_slice[0]["start_ms"]
            # Look ahead to next beat's start to make seamless boundary
            if i < len(beats) - 1:
                next_start_w = beat_word_slices[i + 1][0]
                if next_start_w < total_whisper_words:
                    abs_end_ms = all_whisper_words[next_start_w]["start_ms"]
                else:
                    abs_end_ms = w_slice[-1]["end_ms"] + 150
            else:
                abs_end_ms = total_audio_ms
        else:
            abs_start_ms = int(round((i / len(beats)) * total_audio_ms))
            abs_end_ms = int(round(((i + 1) / len(beats)) * total_audio_ms))

        abs_end_ms = max(abs_start_ms + 400, abs_end_ms)
        scene_dur_ms = abs_end_ms - abs_start_ms
        scene_dur_sec = round(scene_dur_ms / 1000.0, 3)
        scene_dur_frames = int(round(scene_dur_sec * config.fps))

        # Build relative word timings for Remotion KineticSubtitles
        aligned_words = []
        n_tokens = len(tokens)
        n_w = len(w_slice)

        if n_tokens == n_w and n_tokens > 0:
            for j in range(n_tokens):
                rel_start = max(0, w_slice[j]["start_ms"] - abs_start_ms)
                rel_end = max(rel_start + 80, w_slice[j]["end_ms"] - abs_start_ms)
                aligned_words.append({
                    "word": tokens[j],
                    "start_ms": rel_start,
                    "end_ms": rel_end
                })
        else:
            # Monotonic character-weighted interpolation within this scene
            speech_span = scene_dur_ms
            weights = [max(2, len(clean_token(w))) for w in tokens]
            tot_wt = sum(weights) or 1
            accum = 0
            for j, w in enumerate(tokens):
                w_start = int(round((accum / tot_wt) * speech_span))
                accum += weights[j]
                w_end = int(round((accum / tot_wt) * speech_span))
                aligned_words.append({
                    "word": w,
                    "start_ms": w_start,
                    "end_ms": max(w_start + 80, w_end)
                })

        timing_filename = f"scene_{beat.scene_id:03d}_timing.json"
        timing_path = os.path.join(timings_dir, timing_filename).replace("\\", "/")

        timing_data = {
            "audio_file": "master_narration.wav",
            "scene_id": beat.scene_id,
            "abs_start_ms": abs_start_ms,
            "abs_end_ms": abs_end_ms,
            "duration_ms": scene_dur_ms,
            "word_count": len(aligned_words),
            "model": model_name,
            "engine": "faster-whisper",
            "words": aligned_words,
            "aligned_with_script": True
        }

        with open(timing_path, "w", encoding="utf-8") as f:
            json.dump(timing_data, f, ensure_ascii=False, indent=2)

        # Update Beat attributes
        beat.timing_file = timing_filename
        beat.words = aligned_words
        beat.start_ms = abs_start_ms
        beat.end_ms = abs_end_ms
        beat.from_frame = current_frame_accum
        beat.duration_sec = scene_dur_sec
        beat.duration_frames = scene_dur_frames

        current_frame_accum += scene_dur_frames

        print(f"[{beat.scene_id:02d}/{len(beats)}] Scene {beat.scene_id:03d} -> {scene_dur_sec:.2f}s ({scene_dur_frames} frames) [{abs_start_ms}ms -> {abs_end_ms}ms]")

    # Save master timeline
    master_timing_path = os.path.join(timings_dir, "master_timing.json").replace("\\", "/")
    master_summary = {
        "audio_file": "master_narration.wav",
        "total_duration_ms": total_audio_ms,
        "total_frames": current_frame_accum,
        "fps": config.fps,
        "scene_count": len(beats),
        "scenes": [
            {
                "scene_id": b.scene_id,
                "abs_start_ms": b.start_ms,
                "abs_end_ms": b.end_ms,
                "duration_sec": b.duration_sec,
                "duration_frames": b.duration_frames,
                "word_count": len(b.words)
            }
            for b in beats
        ]
    }
    with open(master_timing_path, "w", encoding="utf-8") as f:
        json.dump(master_summary, f, ensure_ascii=False, indent=2)

    print(f"[WhisperEngine] Timeline extraction complete. Master timing: {master_timing_path}")
    return beats
