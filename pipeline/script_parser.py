import re
from typing import List
from pipeline.models import SceneBeat
from pipeline.wardrobe import select_outfit_and_mood

def clean_script_text(text: str) -> str:
    """
    Strips out any bracketed emotion tags (e.g. [thở dài], [hắng giọng], [cười], [sigh], etc.)
    and normalizes excess whitespace.
    """
    cleaned = re.sub(r"\[(thở dài|hắng giọng|cười|ngạc nhiên|khóc|vui|buồn|lo lắng|sigh|gasp|laugh|chuckle)\]", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def parse_script_file(script_path: str, max_words_per_beat: int = 35) -> List[SceneBeat]:
    """
    Dynamically parses any script.txt into a list of SceneBeat objects.
    Supports inline video duration tags: [VIDEO:4s], [VIDEO:6s], [VIDEO:8s], [VIDEO:10s].
    Strictly sanitizes and removes all emotion tags for clean voice and text.
    Preserves deliberate line breaks as distinct scene beats.
    """
    with open(script_path, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    beats: List[SceneBeat] = []
    scene_counter = 1

    for line in raw_lines:
        # Check for explicit video tag: e.g. [VIDEO:6s]
        video_match = re.match(r"^\[VIDEO:(\d+)s?\]\s*(.*)", line, re.IGNORECASE)
        if video_match:
            fixed_dur = int(video_match.group(1))
            spoken_text = clean_script_text(video_match.group(2))
            outfit_id, outfit_info = select_outfit_and_mood(spoken_text, scene_counter)
            
            beat = SceneBeat(
                scene_id=scene_counter,
                spoken_text=spoken_text,
                is_video_slot=True,
                fixed_duration=fixed_dur,
                outfit_id=outfit_id,
                outfit_name=outfit_info["name"],
                camera_motion=outfit_info.get("camera_motion", "zoom_in")
            )
            beats.append(beat)
            scene_counter += 1
            continue

        clean_line = clean_script_text(line)
        # For normal text, check length
        words = clean_line.split()
        if len(words) <= max_words_per_beat:
            # Single beat
            outfit_id, outfit_info = select_outfit_and_mood(clean_line, scene_counter)
            beat = SceneBeat(
                scene_id=scene_counter,
                spoken_text=clean_line,
                is_video_slot=False,
                outfit_id=outfit_id,
                outfit_name=outfit_info["name"],
                camera_motion=outfit_info.get("camera_motion", "zoom_in")
            )
            beats.append(beat)
            scene_counter += 1
        else:
            # Split long sentence at natural punctuation or conjunctions
            # Look for split markers like: , ; : - nhưng để rồi và
            parts = re.split(r"([,;:\-–—]\s*|\s+(?:nhưng|để rồi|và|cho phép|còn|thay vì)\s+)", clean_line)
            
            # Recombine parts into chunks of <= max_words_per_beat
            chunks = []
            curr = ""
            for p in parts:
                if not p:
                    continue
                test_str = (curr + p).strip()
                if len(test_str.split()) <= max_words_per_beat or not curr:
                    curr = test_str
                else:
                    if curr:
                        chunks.append(curr.rstrip(" ,;:-"))
                    curr = p.lstrip(" ,;:-")
            if curr:
                chunks.append(curr.rstrip(" ,;:-"))

            for idx, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                clean_chunk = clean_script_text(chunk)
                outfit_id, outfit_info = select_outfit_and_mood(clean_chunk, scene_counter)
                beat = SceneBeat(
                    scene_id=scene_counter,
                    spoken_text=clean_chunk,
                    is_video_slot=False,
                    outfit_id=outfit_id,
                    outfit_name=outfit_info["name"],
                    camera_motion=outfit_info.get("camera_motion", "zoom_in")
                )
                beats.append(beat)
                scene_counter += 1

    return beats
