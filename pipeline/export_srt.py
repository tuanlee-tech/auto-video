import os
import json
import sys

def ms_to_srt(ms: int) -> str:
    hours = ms // 3600000
    minutes = (ms % 3600000) // 60000
    seconds = (ms % 60000) // 1000
    millis = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

def export_srt(manifest_path: str, out_srt_path: str):
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    scenes = data.get("scenes", [])
    os.makedirs(os.path.dirname(out_srt_path), exist_ok=True)
    
    lines = []
    for s in scenes:
        sid = s.get("scene_id")
        start_ms = s.get("start_ms", 0)
        end_ms = s.get("end_ms", 0)
        text = s.get("spoken_text", "").strip()
        lines.append(f"{sid}\n{ms_to_srt(start_ms)} --> {ms_to_srt(end_ms)}\n{text}\n")
        
    with open(out_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"[+] Cleanly exported {len(scenes)} SRT subtitles to {out_srt_path}")

if __name__ == "__main__":
    m_path = "e:/auto-video/workspace/thoi-quen-thinh-vuong/video_01/manifest.json"
    o_path = "e:/auto-video/workspace/thoi-quen-thinh-vuong/video_01/out/subtitles_vi.srt"
    export_srt(m_path, o_path)
