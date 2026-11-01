import os
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class PipelineConfig:
    # Video Output Specs
    resolution_name: str = "1080p"  # "1080p" or "4k"
    width: int = 1920
    height: int = 1080
    fps: int = 30
    
    # Visual Timing & Transitions
    min_scene_duration: float = 3.0   # Minimum duration for 1 B-roll cut (seconds)
    max_scene_duration: float = 6.0   # If a spoken segment exceeds this, split into multiple B-roll cuts
    transition_type: str = "fade"     # Cross-dissolve
    transition_duration: float = 0.8  # Transition overlap duration (seconds)
    enable_ken_burns: bool = True     # Subtle slow zoom for static images
    ken_burns_zoom: float = 1.04      # Zoom from 1.0 to 1.04
    
    # Audio Specs
    bgm_volume_ducked: float = 0.08   # BGM volume during speech (-22dB)
    bgm_volume_normal: float = 0.25   # BGM volume when no speech
    
    # Character & Visual Branding Defaults
    character_name: str = "stickman"
    character_brand_text: str = "SWOL"  # Or your custom channel acronym
    character_shirt_color: str = "blue"
    bg_color_hex: str = "#F6F2E8"      # Warm cream paper background
    
    # Base Style Prompt for Google Flow (Cinematic Hybrid Style)
    master_style_prefix: str = (
        "A striking cinematic hybrid illustration: A 2D minimalist stickman character with a smooth white round head, "
        "clean bold black outlines, expressive facial features, no hair. "
    )
    master_style_suffix: str = (
        ", cinematic atmospheric 3D environment, dramatic lighting, rich depth of field, storytelling aesthetic, 16:9 landscape, high resolution, 4k."
    )

    def set_resolution(self, res: str):
        if res.lower() == "4k":
            self.resolution_name = "4k"
            self.width = 3840
            self.height = 2160
        else:
            self.resolution_name = "1080p"
            self.width = 1920
            self.height = 1080

DEFAULT_CONFIG = PipelineConfig()
