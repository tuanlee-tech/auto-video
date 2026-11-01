import os
import re
from typing import List, Optional
from pipeline.models import SceneBeat

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv"}

def resolve_project_assets(
    beats: List[SceneBeat],
    images_dir: str,
    videos_dir: Optional[str] = None
) -> List[SceneBeat]:
    """
    Dynamically scans project directories for matching visual assets.
    Matches prefixes: 1_, 01_, 001_, scene_1_, scene_001_, etc.
    Prioritizes video files over static images if both exist for a beat.
    """
    img_files = []
    if os.path.isdir(images_dir):
        img_files = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]

    vid_files = []
    if videos_dir and os.path.isdir(videos_dir):
        vid_files = [f for f in os.listdir(videos_dir) if os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS]

    matched_count = 0
    video_count = 0

    for beat in beats:
        target_id = beat.scene_id
        matched_file = None
        matched_path = None
        asset_type = "image"

        # 1. First check if a video clip exists
        for vf in vid_files:
            prefix = vf.split("_")[0].replace("scene", "")
            if prefix.isdigit() and int(prefix) == target_id:
                matched_file = vf
                matched_path = os.path.join(videos_dir, vf).replace("\\", "/")
                asset_type = "video"
                video_count += 1
                break

        # 2. If no video, check images
        if not matched_file:
            for imf in img_files:
                prefix = imf.split("_")[0].replace("scene", "")
                if prefix.isdigit() and int(prefix) == target_id:
                    matched_file = imf
                    matched_path = os.path.join(images_dir, imf).replace("\\", "/")
                    asset_type = "image"
                    break

        if matched_file:
            beat.asset_file = matched_file
            beat.asset_path = matched_path
            beat.asset_type = asset_type
            matched_count += 1
        else:
            beat.asset_file = None
            beat.asset_path = None
            beat.asset_type = "image"

    print(f"[AssetResolver] Resolved {matched_count}/{len(beats)} visual assets ({video_count} video clips, {matched_count - video_count} images).")
    return beats
