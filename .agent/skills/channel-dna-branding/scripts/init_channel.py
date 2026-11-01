"""
Helper script to initialize a standardized channel profile directory for Auto Video Studio.
Usage:
    python init_channel.py --channel_id channel_02_psychology --name "Tâm Lý Ứng Dụng"
"""

import os
import sys
import json
import argparse

def init_channel(channel_id, name, slogan="Hành động nhỏ, Tự chủ lớn", voice="Hải Đăng"):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "channels", channel_id))
    os.makedirs(os.path.join(base_dir, "branding"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "characters"), exist_ok=True)

    config = {
        "channel_id": channel_id,
        "name": f"{name} (@stickman)",
        "slogan": slogan,
        "secondary_slogan": "Xây dựng hệ thống, Chinh phục tự do",
        "description": f"Kênh chia sẻ kiến thức khoa học và hành động vi mô: {name}",
        "aspect_ratio": "16:9",
        "width": 1920,
        "height": 1080,
        "fps": 60,
        "default_voice": voice,
        "character_tag": "@stickman",
        "character_reference_image": "characters/stickman_master.png",
        "wardrobe_rule": "10-Outfit Collection (GEMINI.md)",
        "art_style": "Simple Ways of Life: 2D Cel-shaded doodle stickman, bold black ink outlines, clean white paper canvas background, yellow highlighter text accents, high contrast",
        "lighting_style": "Cinematic Hybrid",
        "content_pillars": [
            "Trụ cột 1: Thói quen vi mô",
            "Trụ cột 2: Khoa học hành vi",
            "Trụ cột 3: Lối sống tự chủ"
        ],
        "outro_catchphrase": "Hành động nhỏ, nhất quán hàng ngày để tạo dựng tự do cuộc sống. Keep learning, keep growing, and keep it simple."
    }

    cfg_path = os.path.join(base_dir, "channel_config.json")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"[+] Channel directory initialized successfully at: {base_dir}")
    print(f"    Config saved to: {cfg_path}")
    return base_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize new channel profile")
    parser.add_argument("--channel_id", "-c", required=True, help="Channel identifier folder name")
    parser.add_argument("--name", "-n", required=True, help="Official channel display name")
    parser.add_argument("--slogan", "-s", default="Hành động nhỏ, Tự chủ lớn", help="Channel slogan")
    parser.add_argument("--voice", "-v", default="Hải Đăng", help="Default TTS voice")
    args = parser.parse_args()

    init_channel(args.channel_id, args.name, args.slogan, args.voice)
