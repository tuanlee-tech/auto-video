import os
import json
import re
import subprocess
from typing import List, Dict, Any, Optional

def get_audio_duration(file_path: str) -> float:
    """Use ffprobe to get exact duration in seconds."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    try:
        out = subprocess.check_output(cmd, text=True).strip()
        return float(out)
    except Exception as e:
        print(f"Error reading audio duration for {file_path}: {e}")
        return 0.0

def parse_srt(srt_path: str) -> List[Dict[str, Any]]:
    """Parse an SRT file into a list of segments with start, end, text."""
    segments = []
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n\s*\n", content.strip())
    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if len(lines) >= 3:
            time_match = re.match(
                r"(\d{2}):(\d{2}):(\d{2})[,\.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,\.](\d{3})",
                lines[1]
            )
            if time_match:
                h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, time_match.groups())
                start_sec = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0
                end_sec = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0
                text = " ".join(lines[2:])
                segments.append({
                    "start": round(start_sec, 3),
                    "end": round(end_sec, 3),
                    "duration": round(end_sec - start_sec, 3),
                    "text": text
                })
    return segments

def detect_silence_segments(audio_path: str, noise_db: int = -35, min_silence_dur: float = 0.4) -> List[Dict[str, float]]:
    """
    Use ffmpeg silencedetect to find speech pauses and split single audio into speech segments.
    """
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-af", f"silencedetect=noise={noise_db}dB:d={min_silence_dur}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    lines = res.stderr.split("\n")
    
    silences = []
    curr_start = None
    for line in lines:
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([\d\.]+)", line)
            if m:
                curr_start = float(m.group(1))
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s*([\d\.]+)", line)
            if m and curr_start is not None:
                curr_end = float(m.group(1))
                silences.append((curr_start, curr_end))
                curr_start = None
                
    total_dur = get_audio_duration(audio_path)
    if not silences:
        return [{"start": 0.0, "end": total_dur, "duration": total_dur}]
        
    # Convert silences to speech intervals
    speech_intervals = []
    prev_end = 0.0
    for s_start, s_end in silences:
        if s_start > prev_end + 0.2:
            speech_intervals.append({
                "start": round(prev_end, 3),
                "end": round(s_start, 3),
                "duration": round(s_start - prev_end, 3)
            })
        prev_end = s_end
    if total_dur > prev_end + 0.2:
        speech_intervals.append({
            "start": round(prev_end, 3),
            "end": round(total_dur, 3),
            "duration": round(total_dur - prev_end, 3)
        })
    return speech_intervals

def align_audio_with_script(audio_path: str, script_text_path: str) -> List[Dict[str, Any]]:
    """
    Matches speech pauses with script sentences or lines.
    """
    with open(script_text_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Split script into logical sentences
    sentences = [s.strip() for s in re.split(r"(?<=[.!?\n])\s+", raw_text) if s.strip()]
    
    intervals = detect_silence_segments(audio_path)
    total_dur = get_audio_duration(audio_path)
    
    # If number of detected pauses roughly matches sentences:
    if len(intervals) == len(sentences) and len(sentences) > 0:
        results = []
        for i, sent in enumerate(sentences):
            results.append({
                "segment_id": i + 1,
                "start": intervals[i]["start"],
                "end": intervals[i]["end"],
                "duration": intervals[i]["duration"],
                "text": sent
            })
        return results
        
    # Fallback: distribute time proportionally by word count across intervals or total duration
    total_words = sum(len(s.split()) for s in sentences)
    if total_words == 0:
        return []
        
    results = []
    curr_time = 0.0
    for i, sent in enumerate(sentences):
        words_count = len(sent.split())
        prop_dur = (words_count / total_words) * total_dur
        end_time = min(total_dur, curr_time + prop_dur)
        results.append({
            "segment_id": i + 1,
            "start": round(curr_time, 3),
            "end": round(end_time, 3),
            "duration": round(end_time - curr_time, 3),
            "text": sent
        })
        curr_time = end_time
    return results

def build_timeline(
    audio_path: str,
    script_path: Optional[str] = None,
    srt_path: Optional[str] = None,
    output_json_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Main entry point for Step 2: Build a precise speech timeline.
    """
    if srt_path and os.path.exists(srt_path):
        segments = parse_srt(srt_path)
        for i, s in enumerate(segments):
            s["segment_id"] = i + 1
    elif script_path and os.path.exists(script_path):
        segments = align_audio_with_script(audio_path, script_path)
    else:
        # Just detect speech segments without text
        intervals = detect_silence_segments(audio_path)
        segments = []
        for i, inv in enumerate(intervals):
            segments.append({
                "segment_id": i + 1,
                "start": inv["start"],
                "end": inv["end"],
                "duration": inv["duration"],
                "text": f"Spoken segment {i+1}"
            })

    if output_json_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_json_path)), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
        print(f"[Aligner] Saved {len(segments)} timeline segments to {output_json_path}")
        
    return segments
