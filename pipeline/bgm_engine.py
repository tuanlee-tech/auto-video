import os
import shutil
import re
from typing import Dict, Any, List, Optional
from pipeline.models import SceneBeat, ProjectConfig

# Mood definitions and keyword dictionaries for Vietnamese financial/life scripts
MOOD_KEYWORDS = {
    "dark_suspense": [
        "nợ", "áp lực", "bế tắc", "hóa đơn", "mất phương hướng", "kiệt sức", "lo lắng", 
        "bẫy", "khủng hoảng", "cạn tiền", "túng quẫn", "chật vật", "lương", "chi tiêu",
        "thất bại", "nghèo", "rỗng túi", "sợ hãi", "bất an"
    ],
    "deep_contemplative": [
        "tại sao", "câu hỏi", "bản chất", "triết lý", "suy ngẫm", "sự thật", "tự hỏi", 
        "gốc rễ", "nghịch lý", "quan sát", "nhìn lại", "thâm căn", "ý nghĩa", "nhận thức"
    ],
    "hopeful_awakening": [
        "kỷ luật", "giải pháp", "thói quen", "công thức", "quản lý", "bước đầu", "kiểm soát", 
        "tái thiết kế", "hành động", "thay đổi", "thức tỉnh", "chiến lược", "tích lũy",
        "đầu tư", "kế hoạch", "bắt đầu", "chuyển mình"
    ],
    "peaceful_minimal": [
        "tự do", "bình yên", "an tâm", "hạnh phúc", "bền vững", "tối giản", "thành quả", 
        "thư thái", "nhẹ nhõm", "an toàn", "vững vàng", "tự chủ", "bình thản", "thảnh thơi"
    ]
}

MOOD_TRACK_MAP = {
    "dark_suspense": "dark_suspense.wav",
    "deep_contemplative": "deep_contemplative.wav",
    "hopeful_awakening": "hopeful_awakening.wav",
    "peaceful_minimal": "peaceful_minimal.wav"
}

def analyze_script_mood(beats: List[SceneBeat]) -> Dict[str, Any]:
    """
    Analyzes the emotional arc across the scenes of a script.
    Detects opening problem mood, closing solution mood, and transition scene.
    """
    if not beats:
        return {
            "primary_mood": "dark_suspense",
            "secondary_mood": "hopeful_awakening",
            "transition_scene_id": 1,
            "mode": "single",
            "track_1": "dark_suspense.wav",
            "track_2": "hopeful_awakening.wav"
        }

    total_scenes = len(beats)
    mid_point = total_scenes // 2

    # Score scenes individually
    scene_mood_scores = []
    for beat in beats:
        text = beat.spoken_text.lower()
        scores = {}
        for mood, keywords in MOOD_KEYWORDS.items():
            scores[mood] = sum(1 for kw in keywords if kw in text)
        scene_mood_scores.append(scores)

    # First half score (Problem / Contemplation)
    first_half_totals = {"dark_suspense": 0, "deep_contemplative": 0, "hopeful_awakening": 0, "peaceful_minimal": 0}
    for s in scene_mood_scores[:mid_point]:
        for m, count in s.items():
            first_half_totals[m] += count

    # Second half score (Solution / Peaceful)
    second_half_totals = {"dark_suspense": 0, "deep_contemplative": 0, "hopeful_awakening": 0, "peaceful_minimal": 0}
    for s in scene_mood_scores[mid_point:]:
        for m, count in s.items():
            second_half_totals[m] += count

    # Determine primary opening mood
    if first_half_totals["dark_suspense"] >= first_half_totals["deep_contemplative"]:
        primary_mood = "dark_suspense"
    else:
        primary_mood = "deep_contemplative"

    # Determine secondary closing mood
    if second_half_totals["peaceful_minimal"] > second_half_totals["hopeful_awakening"]:
        secondary_mood = "peaceful_minimal"
    else:
        secondary_mood = "hopeful_awakening"

    # Find the transition scene (first scene in second half that mentions awakening/solution)
    transition_scene_id = mid_point + 1
    for i, beat in enumerate(beats[mid_point - 2:], start=mid_point - 1):
        text = beat.spoken_text.lower()
        if any(kw in text for kw in MOOD_KEYWORDS["hopeful_awakening"] + MOOD_KEYWORDS["peaceful_minimal"]):
            transition_scene_id = beat.scene_id
            break

    # Generate AI Music Prompts (for Google MusicFX or MusicGen)
    prompt_opening = (
        f"Cinematic documentary background music, {primary_mood.replace('_', ' ')} atmosphere, "
        "minimalist dark ambient synth drone, subtle deep sub-bass pulse, cold tension, "
        "80 bpm, no vocals, high quality film score"
    )
    prompt_resolution = (
        f"Cinematic documentary background music, {secondary_mood.replace('_', ' ')} atmosphere, "
        "warm acoustic piano and inspiring ambient swell, gentle sunlight, emotional resolution, "
        "hopeful cinematic strings, no vocals, high quality film score"
    )

    track_1 = MOOD_TRACK_MAP.get(primary_mood, "dark_suspense.wav")
    track_2 = MOOD_TRACK_MAP.get(secondary_mood, "hopeful_awakening.wav")

    return {
        "mode": "dual" if total_scenes >= 8 else "single",
        "primary_mood": primary_mood,
        "secondary_mood": secondary_mood,
        "transition_scene_id": transition_scene_id,
        "track_1": track_1,
        "track_2": track_2,
        "prompt_opening": prompt_opening,
        "prompt_resolution": prompt_resolution
    }

def setup_project_bgm(
    project_dir: str,
    beats: List[SceneBeat],
    common_bgm_dir: str = "channels/common_assets/bgm",
    channel_bgm_dir: Optional[str] = None,
    custom_track_1: Optional[str] = None,
    custom_track_2: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sets up the BGM for a project:
    1. Analyzes mood.
    2. Resolves audio files from project_dir/bgm, channel_bgm_dir, or common_bgm_dir.
    3. Copies the required tracks into project_dir/bgm.
    4. Writes bgm_prompts.txt for AI generation reference.
    5. Returns bgm configuration dictionary for manifest.
    """
    target_bgm_dir = os.path.join(project_dir, "bgm")
    os.makedirs(target_bgm_dir, exist_ok=True)

    mood_analysis = analyze_script_mood(beats)

    track_1_name = custom_track_1 or mood_analysis["track_1"]
    track_2_name = custom_track_2 or mood_analysis["track_2"]

    # Candidate search paths
    search_dirs = [target_bgm_dir]
    if channel_bgm_dir and os.path.isdir(channel_bgm_dir):
        search_dirs.append(channel_bgm_dir)
    if os.path.isdir(common_bgm_dir):
        search_dirs.append(common_bgm_dir)

    def locate_and_copy(filename: str) -> Optional[str]:
        # If already in target_bgm_dir
        in_target = os.path.join(target_bgm_dir, filename)
        if os.path.exists(in_target):
            return filename
        for sdir in search_dirs:
            candidate = os.path.join(sdir, filename)
            if os.path.exists(candidate):
                shutil.copy2(candidate, in_target)
                return filename
        return None

    resolved_t1 = locate_and_copy(track_1_name)
    resolved_t2 = locate_and_copy(track_2_name)

    # Save prompt reference file
    prompts_file = os.path.join(project_dir, "prompts", "bgm_prompts.txt")
    os.makedirs(os.path.dirname(prompts_file), exist_ok=True)
    with open(prompts_file, "w", encoding="utf-8") as f:
        f.write("# AUTO VIDEO STUDIO - AI BGM GENERATION PROMPTS (MusicFX / MusicGen)\n\n")
        f.write(f"[PART 1 - OPENING & TENSION] (Mood: {mood_analysis['primary_mood']}):\n")
        f.write(f"{mood_analysis['prompt_opening']}\n\n")
        f.write(f"[PART 2 - RESOLUTION & AWAKENING] (Mood: {mood_analysis['secondary_mood']}):\n")
        f.write(f"{mood_analysis['prompt_resolution']}\n\n")
        f.write(f"Transition Scene: Scene {mood_analysis['transition_scene_id']}\n")

    bgm_config = {
        "mode": mood_analysis["mode"],
        "track_1": resolved_t1,
        "track_2": resolved_t2,
        "transition_scene_id": mood_analysis["transition_scene_id"],
        "volume_ducked": 0.14,
        "volume_normal": 0.32,
        "fade_in_frames": 60,
        "fade_out_frames": 120,
        "primary_mood": mood_analysis["primary_mood"],
        "secondary_mood": mood_analysis["secondary_mood"],
        "prompt_opening": mood_analysis["prompt_opening"],
        "prompt_resolution": mood_analysis["prompt_resolution"]
    }

    print(f"[BGMEngine] Configured BGM ({bgm_config['mode']}):")
    print(f"  Part 1 (Scenes 1 -> {bgm_config['transition_scene_id'] - 1}): {resolved_t1} [{bgm_config['primary_mood']}]")
    if bgm_config["mode"] == "dual":
        print(f"  Part 2 (Scenes {bgm_config['transition_scene_id']} -> End): {resolved_t2} [{bgm_config['secondary_mood']}]")
    print(f"  AI Prompts written to: {prompts_file}")

    return bgm_config
