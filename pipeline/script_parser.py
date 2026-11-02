import re
from typing import List, Tuple, Dict, Any
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

def classify_scene_type(
    text: str,
    scene_idx: int,
    total_expected: int,
    is_video_slot: bool = False
) -> str:
    """
    Classifies a scene into one of four distinct production types:
    - 'hero': Persona storytelling with @stickman (15-25% of video)
    - 'infographic': Sleek data visual, brain scan, or banking UI diagram (45-55%)
    - 'metaphor': Cinematic 3D visual metaphor without stickman (25-35%)
    - 'environment': Wide atmospheric establishing shot without stickman (5-10%)
    """
    t = text.lower()

    # 1. Absolute Hero anchors (intro, outro, key emotional connection)
    hero_anchors = [
        "bạn có bao giờ", "chúng ta ai cũng", "bạn mở ứng dụng", "bạn tự nhủ", 
        "bắt đầu từ tháng sau", "tự trách", "chào mừng bạn", "tôi sẽ cùng bạn", 
        "tôi sẽ chia sẻ", "hãy lắng nghe kỹ", "nhìn lại toàn bộ", "hãy tiếp tục", 
        "keep it simple", "bản thân mình", "con người bạn"
    ]
    if scene_idx == 1 or scene_idx >= total_expected - 1:
        return "hero"
    if any(k in t for k in hero_anchors):
        return "hero"
    if is_video_slot and any(w in t for w in ["bạn", "chúng ta", "tôi"]):
        return "hero"

    # 2. Keywords for Infographic (Technical, brain, financial mechanics)
    info_kws = [
        "phương trình", "sơ đồ", "quy tắc hai chiếc hộp", "hai chiếc hộp",
        "80%", "20%", "vỏ não", "hạch hạnh nhân", "cộng hưởng từ",
        "thần kinh", "chỉ số", "phần trăm", "ứng dụng ngân hàng", "ngân hàng số",
        "tự động trích", "phân luồng", "hạn mức", "dopamine", "nghiên cứu",
        "công trình nghiên cứu", "tâm lý học của sự khan hiếm", "bản năng sinh học",
        "quy luật chi tiêu", "parkinson"
    ]
    if any(k in t for k in info_kws):
        return "infographic"

    # 3. Keywords for Metaphor (Concrete objects, symbolic analogies)
    meta_kws = [
        "con heo đất", "bốc hơi", "đồng hồ cát", "cạm bẫy", "chi tiêu phình to",
        "giông bão", "ngọn hải đăng", "cát chảy", "két sắt", "bánh răng",
        "dòng chảy", "nguyên thủy", "thức ăn", "tuyên chiến", "bẫy vô tận",
        "chế độ tầm nhìn đường hầm", "con số đứng yên", "ma sát", "đóng băng"
    ]
    if any(k in t for k in meta_kws):
        return "metaphor"

    # 4. Keywords for Environment (Atmospheric locations)
    env_kws = [
        "đêm mưa", "văn phòng", "thành phố", "siêu thị", "quán cà phê",
        "bình minh", "đường phố", "cuối tháng"
    ]
    if any(k in t for k in env_kws):
        return "environment"

    # Default balance: Alternate between metaphor and infographic
    return "metaphor" if scene_idx % 2 == 0 else "infographic"

def parse_script_file(script_path: str, target_words_per_beat: int = 70) -> List[SceneBeat]:
    """
    Parses script.txt into a cinematic rhythm of ~55-80 words per scene (12-18 seconds).
    Decouples character from scene: 
    - 25-30% Hero scenes featuring @stickman
    - 70-75% rich B-roll (Metaphor, Infographic, Environment) focusing 100% on script concept with zero stickman.
    Preserves exact [VIDEO:Xs] slots as dedicated video beats.
    """
    with open(script_path, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    raw_beats_data = []
    current_chunk = []
    current_words = 0

    for line in raw_lines:
        video_match = re.match(r"^\[VIDEO:(\d+)s?\]\s*(.*)", line, re.IGNORECASE)
        if video_match:
            # Flush accumulated text before starting dedicated video beat
            if current_chunk:
                raw_beats_data.append({
                    "text": clean_script_text(" ".join(current_chunk)),
                    "is_video": False,
                    "fixed_dur": None
                })
                current_chunk = []
                current_words = 0

            # Dedicated video slot
            fixed_dur = int(video_match.group(1))
            spoken_text = clean_script_text(video_match.group(2))
            raw_beats_data.append({
                "text": spoken_text,
                "is_video": True,
                "fixed_dur": fixed_dur
            })
            continue

        clean_line = clean_script_text(line)
        words = clean_line.split()

        if current_words + len(words) >= target_words_per_beat and current_chunk:
            raw_beats_data.append({
                "text": clean_script_text(" ".join(current_chunk)),
                "is_video": False,
                "fixed_dur": None
            })
            current_chunk = [clean_line]
            current_words = len(words)
        else:
            current_chunk.append(clean_line)
            current_words += len(words)

    if current_chunk:
        raw_beats_data.append({
            "text": clean_script_text(" ".join(current_chunk)),
            "is_video": False,
            "fixed_dur": None
        })

    total_scenes = len(raw_beats_data)
    beats: List[SceneBeat] = []

    for idx, item in enumerate(raw_beats_data):
        scene_id = idx + 1
        spoken_text = item["text"]
        is_video = item["is_video"]
        fixed_dur = item["fixed_dur"]

        scene_type = classify_scene_type(
            spoken_text,
            scene_id,
            total_scenes,
            is_video_slot=is_video
        )

        outfit_id, outfit_info = select_outfit_and_mood(spoken_text, scene_id)

        # Dynamic camera motion based on scene type
        if scene_type == "infographic":
            cam_motion = "zoom_in"
        elif scene_type == "environment":
            cam_motion = "pan_left" if scene_id % 2 == 0 else "pan_right"
        elif scene_type == "metaphor":
            cam_motion = "zoom_out" if scene_id % 2 == 0 else "zoom_in"
        else:
            cam_motion = outfit_info.get("camera_motion", "zoom_in")

        beat = SceneBeat(
            scene_id=scene_id,
            spoken_text=spoken_text,
            is_video_slot=is_video,
            fixed_duration=fixed_dur,
            scene_type=scene_type,
            outfit_id=outfit_id,
            outfit_name=outfit_info["name"] if scene_type == "hero" else "Concept B-Roll",
            camera_motion=cam_motion
        )
        beats.append(beat)

    print(f"[ScriptParser] Grouped script into {len(beats)} cinematic scenes (~12-18s per scene).")
    hero_count = sum(1 for b in beats if b.scene_type == "hero")
    broll_count = len(beats) - hero_count
    print(f"               Hero Stickman scenes: {hero_count} ({hero_count/len(beats)*100:.1f}%) | Concept B-Roll scenes: {broll_count} ({broll_count/len(beats)*100:.1f}%)")
    return beats
