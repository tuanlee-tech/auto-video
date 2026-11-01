import os
import sys
import argparse
sys.stdout.reconfigure(encoding="utf-8")

from pipeline.project_manager import ProjectManager

def main():
    parser = argparse.ArgumentParser(
        description="Auto Video Studio: Multi-Channel Dynamic Production Pipeline (VieNeu-TTS + Auto Flow + Remotion 60FPS)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available Pipeline Commands")

    # Command: channels
    subparsers.add_parser("channels", help="List all available channel profiles")

    # Command: init
    p_init = subparsers.add_parser("init", help="Initialize a new project workspace under a channel")
    p_init.add_argument("--project", "-p", required=True, help="Project name (e.g. video_01, crypto_101)")
    p_init.add_argument("--channel", "-c", default="thoi-quen-thinh-vuong", help="Channel profile ID")
    p_init.add_argument("--voice", help="Override default voice preset")
    p_init.add_argument("--fps", type=int, default=60, help="Output framerate (default 60)")

    # Command: parse
    p_parse = subparsers.add_parser("parse", help="Parse script.txt into narrative beats")
    p_parse.add_argument("--project", "-p", required=True, help="Project name")
    p_parse.add_argument("--channel", "-c", help="Channel profile ID (optional)")

    # Command: voice
    p_voice = subparsers.add_parser("voice", help="Generate segmented zero-drift TTS audio")
    p_voice.add_argument("--project", "-p", required=True, help="Project name")
    p_voice.add_argument("--channel", "-c", help="Channel profile ID (optional)")

    # Command: transcribe
    p_transcribe = subparsers.add_parser("transcribe", help="Extract millisecond word timestamps using faster-whisper")
    p_transcribe.add_argument("--project", "-p", required=True, help="Project name")
    p_transcribe.add_argument("--channel", "-c", help="Channel profile ID (optional)")
    p_transcribe.add_argument("--model", "-m", default="base", help="Whisper model (tiny, base, small, medium)")

    # Command: prompts
    p_prompts = subparsers.add_parser("prompts", help="Generate cinematic prompts & 4-panel storyboard grids")
    p_prompts.add_argument("--project", "-p", required=True, help="Project name")
    p_prompts.add_argument("--channel", "-c", help="Channel profile ID (optional)")

    # Command: match
    p_match = subparsers.add_parser("match", help="Dynamically match downloaded images & videos to scenes")
    p_match.add_argument("--project", "-p", required=True, help="Project name")
    p_match.add_argument("--channel", "-c", help="Channel profile ID (optional)")

    # Command: clean
    p_clean = subparsers.add_parser("clean", help="Clean Google Flow watermarks from all videos in project")
    p_clean.add_argument("--project", "-p", required=True, help="Project name")
    p_clean.add_argument("--channel", "-c", help="Channel profile ID (optional)")

    # Command: bgm
    p_bgm = subparsers.add_parser("bgm", help="Automatically analyze mood and setup background music")
    p_bgm.add_argument("--project", "-p", required=True, help="Project name")
    p_bgm.add_argument("--channel", "-c", help="Channel profile ID (optional)")
    p_bgm.add_argument("--track1", help="Custom opening track filename")
    p_bgm.add_argument("--track2", help="Custom resolution track filename")

    # Command: render
    p_render = subparsers.add_parser("render", help="Render video using Remotion 60FPS Engine")
    p_render.add_argument("--project", "-p", required=True, help="Project name")
    p_render.add_argument("--channel", "-c", help="Channel profile ID (optional)")
    p_render.add_argument("--fps", type=int, help="Framerate (default from channel config)")
    p_render.add_argument("--out", "-o", help="Custom output MP4 path")

    # Command: thumbnail
    p_thumb = subparsers.add_parser("thumbnail", help="Render YouTube thumbnail, logo & banner in Simple Ways of Life style")
    p_thumb.add_argument("--project", "-p", required=True, help="Project name")
    p_thumb.add_argument("--channel", "-c", help="Channel profile ID (optional)")
    p_thumb.add_argument("--type", choices=["all", "thumbnail", "logo", "banner"], default="all", help="Asset type (default: all)")

    # Command: all
    p_all = subparsers.add_parser("all", help="Execute complete pipeline end-to-end")
    p_all.add_argument("--project", "-p", required=True, help="Project name")
    p_all.add_argument("--channel", "-c", help="Channel profile ID (optional)")
    p_all.add_argument("--fps", type=int, help="Framerate (default from channel config)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    pm = ProjectManager()

    if args.command == "channels":
        print("=== AVAILABLE CHANNEL PROFILES ===")
        channels = pm.list_channels()
        for ch in channels:
            cfg = pm.load_channel_config(ch)
            if cfg:
                print(f"• [{cfg.channel_id}] {cfg.name} ({cfg.aspect_ratio}, {cfg.fps}fps, Voice: {cfg.default_voice})")
            else:
                print(f"• [{ch}] (No config file)")

    elif args.command == "init":
        pm.init_project(args.project, channel_id=args.channel, voice_name=args.voice, fps=args.fps)

    elif args.command == "parse":
        pm.step_parse_script(args.project, args.channel)

    elif args.command == "voice":
        pm.step_generate_voice(args.project, args.channel)

    elif args.command == "transcribe":
        pm.step_extract_timings(args.project, args.channel, model_name=args.model)

    elif args.command == "prompts":
        pm.step_generate_prompts(args.project, args.channel)

    elif args.command == "match":
        pm.step_resolve_assets(args.project, args.channel)

    elif args.command == "clean":
        pm.step_clean_videos(args.project, args.channel)

    elif args.command == "bgm":
        pm.step_setup_bgm(args.project, args.channel, custom_track_1=args.track1, custom_track_2=args.track2)

    elif args.command == "render":
        pm.render_video(args.project, channel_id=args.channel, fps=args.fps, output_mp4=args.out)

    elif args.command == "thumbnail":
        pm.render_branding_assets(args.project, channel_id=args.channel, asset_type=args.type)

    elif args.command == "all":
        print(f"=== [1/6] PARSING SCRIPT: {args.project} ===")
        pm.step_parse_script(args.project, args.channel)

        print(f"\n=== [2/6] GENERATING SEGMENTED TTS ===")
        pm.step_generate_voice(args.project, args.channel)

        print(f"\n=== [3/6] EXTRACTING WORD-LEVEL TIMESTAMPS (WHISPER) ===")
        pm.step_extract_timings(args.project, args.channel)

        print(f"\n=== [4/6] GENERATING PROMPTS & STORYBOARD GRIDS ===")
        pm.step_generate_prompts(args.project, args.channel)

        print(f"\n=== [5/6] RESOLVING ASSETS ===")
        pm.step_resolve_assets(args.project, args.channel)

        print(f"\n=== [6/6] RENDERING REMOTION VIDEO ===")
        pm.render_video(args.project, channel_id=args.channel, fps=args.fps)

if __name__ == "__main__":
    main()
