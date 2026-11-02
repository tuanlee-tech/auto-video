import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

@dataclass
class SceneBeat:
    scene_id: int
    spoken_text: str
    audio_file: str = ""
    audio_path: str = ""
    duration_sec: float = 0.0
    duration_frames: int = 0
    is_video_slot: bool = False
    fixed_duration: Optional[int] = None  # 4, 6, 8, 10 seconds for Omni Flash 1.1
    scene_type: str = "hero"  # "hero", "metaphor", "infographic", "environment"
    outfit_id: int = 1
    outfit_name: str = ""
    prompt: str = ""
    storyboard_prompt: Optional[str] = None
    asset_file: Optional[str] = None
    asset_path: Optional[str] = None
    asset_type: str = "image"  # "image" or "video"
    video_start_offset_sec: float = 0.0
    camera_motion: str = "zoom_in"  # "zoom_in", "zoom_out", "pan_left", "pan_right"
    timing_file: Optional[str] = None
    words: List[Dict[str, Any]] = field(default_factory=list)
    start_ms: int = 0
    end_ms: int = 0
    from_frame: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ChannelConfig:
    channel_id: str = "channel_01_finance_stickman"
    name: str = "Thói Quen Thịnh Vượng (@stickman)"
    slogan: str = "Hành động nhỏ, Tự chủ lớn"
    description: str = ""
    aspect_ratio: str = "16:9"
    width: int = 1920
    height: int = 1080
    fps: int = 60
    default_voice: str = "Hải Đăng"
    character_tag: str = "@stickman"
    character_reference_image: str = ""
    lighting_style: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ProjectConfig:
    project_name: str = "default"
    channel_id: str = "channel_01_finance_stickman"
    project_dir: str = ""
    voice_name: str = "Hải Đăng"
    fps: int = 60
    width: int = 1920
    height: int = 1080
    aspect_ratio: str = "16:9"
    min_beat_duration: float = 2.5
    max_beat_duration: float = 5.5
    bgm_file: Optional[str] = None
    bgm_mode: str = "dual"
    bgm_track_1: Optional[str] = None
    bgm_track_2: Optional[str] = None
    bgm_transition_scene_id: Optional[int] = None
    bgm_volume_ducked: float = 0.14
    bgm_volume_normal: float = 0.32
    character_name: str = "stickman"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
