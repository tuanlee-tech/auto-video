import os
import sys
import shutil
import json
import subprocess
from typing import Optional, List, Dict, Any

from pipeline.models import SceneBeat, ProjectConfig, ChannelConfig
from pipeline.script_parser import parse_script_file
from pipeline.voice_engine import generate_master_voice
from pipeline.prompt_engine import generate_project_prompts
from pipeline.asset_resolver import resolve_project_assets

class ProjectManager:
    """
    Multi-Channel, Completely Dynamic Project Manager for Auto Video Studio.
    Operates seamlessly across multiple channel profiles:
    channels/<channel_id>/ -> workspace/<channel_id>/<project_name>/
    """
    def __init__(
        self,
        base_workspace: str = "e:/auto-video/workspace",
        base_channels: str = "e:/auto-video/channels"
    ):
        self.base_workspace = os.path.abspath(base_workspace).replace("\\", "/")
        self.base_channels = os.path.abspath(base_channels).replace("\\", "/")
        self.remotion_studio_dir = os.path.abspath("e:/auto-video/remotion-studio").replace("\\", "/")

    def list_channels(self) -> List[str]:
        if not os.path.exists(self.base_channels):
            return []
        return [d for d in os.listdir(self.base_channels) if os.path.isdir(os.path.join(self.base_channels, d))]

    def load_channel_config(self, channel_id: str) -> Optional[ChannelConfig]:
        cfg_path = os.path.join(self.base_channels, channel_id, "channel_config.json")
        if os.path.exists(cfg_path):
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            from dataclasses import fields
            valid_keys = {f.name for f in fields(ChannelConfig)}
            filtered = {k: v for k, v in data.items() if k in valid_keys}
            return ChannelConfig(**filtered)
        return None

    def get_project_dir(self, project_name: str, channel_id: Optional[str] = None) -> str:
        # If channel is specified, direct path
        if channel_id:
            return os.path.join(self.base_workspace, channel_id, project_name).replace("\\", "/")

        # Otherwise search across channel workspaces
        if os.path.exists(self.base_workspace):
            for item in os.listdir(self.base_workspace):
                subpath = os.path.join(self.base_workspace, item)
                if os.path.isdir(subpath):
                    # Check if project_name is inside item
                    candidate = os.path.join(subpath, project_name)
                    if os.path.exists(candidate):
                        return candidate.replace("\\", "/")
                    if item == project_name:
                        return subpath.replace("\\", "/")

        # Default fallback to channel_01_finance_stickman
        return os.path.join(self.base_workspace, "channel_01_finance_stickman", project_name).replace("\\", "/")

    def init_project(
        self,
        project_name: str,
        channel_id: str = "channel_01_finance_stickman",
        script_content: Optional[str] = None,
        voice_name: Optional[str] = None,
        fps: int = 60
    ) -> ProjectConfig:
        ch_cfg = self.load_channel_config(channel_id)
        chosen_voice = voice_name or (ch_cfg.default_voice if ch_cfg else "Hải Đăng")
        width = ch_cfg.width if ch_cfg else 1920
        height = ch_cfg.height if ch_cfg else 1080
        aspect_ratio = ch_cfg.aspect_ratio if ch_cfg else "16:9"

        pdir = self.get_project_dir(project_name, channel_id)
        os.makedirs(os.path.join(pdir, "audio"), exist_ok=True)
        os.makedirs(os.path.join(pdir, "images"), exist_ok=True)
        os.makedirs(os.path.join(pdir, "videos"), exist_ok=True)
        os.makedirs(os.path.join(pdir, "prompts"), exist_ok=True)
        os.makedirs(os.path.join(pdir, "bgm"), exist_ok=True)
        os.makedirs(os.path.join(pdir, "out"), exist_ok=True)

        config_path = os.path.join(pdir, "project_config.json")
        cfg = ProjectConfig(
            project_name=project_name,
            channel_id=channel_id,
            project_dir=pdir,
            voice_name=chosen_voice,
            fps=fps,
            width=width,
            height=height,
            aspect_ratio=aspect_ratio
        )
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg.to_dict(), f, ensure_ascii=False, indent=2)

        script_path = os.path.join(pdir, "script.txt")
        if script_content and not os.path.exists(script_path):
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_content)

        print(f"[ProjectManager] Initialized project '{project_name}' (Channel: {channel_id}) at: {pdir}")
        return cfg

    def load_config(self, project_name: str, channel_id: Optional[str] = None) -> ProjectConfig:
        pdir = self.get_project_dir(project_name, channel_id)
        config_path = os.path.join(pdir, "project_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            from dataclasses import fields
            valid_keys = {f.name for f in fields(ProjectConfig)}
            filtered = {k: v for k, v in data.items() if k in valid_keys}
            cfg = ProjectConfig(**filtered)
            cfg.project_dir = pdir
            return cfg
        return ProjectConfig(project_name=project_name, project_dir=pdir)

    def load_manifest(self, project_name: str, channel_id: Optional[str] = None) -> List[SceneBeat]:
        pdir = self.get_project_dir(project_name, channel_id)
        manifest_path = os.path.join(pdir, "manifest.json")
        if not os.path.exists(manifest_path):
            return []
        with open(manifest_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        
        beats = []
        from dataclasses import fields
        valid_beat_keys = {f.name for f in fields(SceneBeat)}
        for item in raw.get("scenes", []):
            filtered = {k: v for k, v in item.items() if k in valid_beat_keys}
            beats.append(SceneBeat(**filtered))
        return beats

    def save_manifest(
        self,
        project_name: str,
        beats: List[SceneBeat],
        config: Optional[ProjectConfig] = None,
        channel_id: Optional[str] = None
    ) -> str:
        pdir = self.get_project_dir(project_name, channel_id)
        cfg = config or self.load_config(project_name, channel_id)
        manifest_path = os.path.join(pdir, "manifest.json")

        # Check if existing manifest has bgm
        bgm_dict = None
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                    bgm_dict = old_data.get("bgm")
            except Exception:
                pass

        if not bgm_dict:
            bgm_dict = {
                "mode": cfg.bgm_mode,
                "track_1": cfg.bgm_track_1 or cfg.bgm_file,
                "track_2": cfg.bgm_track_2,
                "transition_scene_id": cfg.bgm_transition_scene_id,
                "volume_ducked": cfg.bgm_volume_ducked,
                "volume_normal": cfg.bgm_volume_normal,
                "fade_in_frames": 60,
                "fade_out_frames": 120
            }

        payload = {
            "project_name": project_name,
            "channel_id": cfg.channel_id,
            "fps": cfg.fps,
            "width": cfg.width,
            "height": cfg.height,
            "aspect_ratio": cfg.aspect_ratio,
            "audio_file": "master_narration.wav",
            "bgm_file": cfg.bgm_file or bgm_dict.get("track_1"),
            "bgm_volume_ducked": cfg.bgm_volume_ducked,
            "bgm_volume_normal": cfg.bgm_volume_normal,
            "bgm": bgm_dict,
            "scenes": [b.to_dict() for b in beats]
        }

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        return manifest_path

    def step_parse_script(self, project_name: str, channel_id: Optional[str] = None) -> List[SceneBeat]:
        pdir = self.get_project_dir(project_name, channel_id)
        script_path = os.path.join(pdir, "script.txt")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Missing script.txt in {pdir}")

        cfg = self.load_config(project_name, channel_id)
        beats = parse_script_file(script_path)
        self.save_manifest(project_name, beats, cfg, channel_id)
        print(f"[ProjectManager] Parsed {len(beats)} narrative beats from {script_path}")
        return beats

    def step_generate_voice(self, project_name: str, channel_id: Optional[str] = None) -> List[SceneBeat]:
        pdir = self.get_project_dir(project_name, channel_id)
        script_path = os.path.join(pdir, "script.txt")
        if os.path.exists(script_path):
            beats = self.step_parse_script(project_name, channel_id)
        else:
            beats = self.load_manifest(project_name, channel_id)

        cfg = self.load_config(project_name, channel_id)
        audio_dir = os.path.join(cfg.project_dir, "audio")
        beats = generate_master_voice(beats, cfg, audio_dir)
        self.save_manifest(project_name, beats, cfg, channel_id)
        return beats

    def step_extract_timings(
        self,
        project_name: str,
        channel_id: Optional[str] = None,
        model_name: str = "base"
    ) -> List[SceneBeat]:
        beats = self.load_manifest(project_name, channel_id)
        if not beats:
            beats = self.step_parse_script(project_name, channel_id)

        cfg = self.load_config(project_name, channel_id)
        audio_dir = os.path.join(cfg.project_dir, "audio")
        timings_dir = os.path.join(cfg.project_dir, "timings")
        master_audio_path = os.path.join(audio_dir, "master_narration.wav")
        
        from pipeline.whisper_engine import extract_master_timings_and_align
        beats = extract_master_timings_and_align(beats, cfg, master_audio_path, timings_dir, model_name=model_name)
        self.save_manifest(project_name, beats, cfg, channel_id)
        return beats

    def step_generate_prompts(self, project_name: str, channel_id: Optional[str] = None) -> List[SceneBeat]:
        beats = self.load_manifest(project_name, channel_id)
        if not beats:
            beats = self.step_parse_script(project_name, channel_id)

        has_timings = any(getattr(b, "start_ms", None) is not None and b.start_ms > 0 for b in beats)
        if not has_timings:
            print("[ProjectManager] Note: Faster-Whisper word timings have not been extracted yet. In accordance with the Voice-First philosophy, please ensure 'transcribe' runs to map exact scene durations.")

        cfg = self.load_config(project_name, channel_id)
        prompts_dir = os.path.join(cfg.project_dir, "prompts")
        beats = generate_project_prompts(beats, cfg, prompts_dir)
        self.save_manifest(project_name, beats, cfg, channel_id)
        return beats

    def step_resolve_assets(self, project_name: str, channel_id: Optional[str] = None) -> List[SceneBeat]:
        beats = self.load_manifest(project_name, channel_id)
        if not beats:
            beats = self.step_parse_script(project_name, channel_id)

        cfg = self.load_config(project_name, channel_id)
        images_dir = os.path.join(cfg.project_dir, "images")
        videos_dir = os.path.join(cfg.project_dir, "videos")

        beats = resolve_project_assets(beats, images_dir, videos_dir)
        self.save_manifest(project_name, beats, cfg, channel_id)
        return beats

    def step_setup_bgm(
        self,
        project_name: str,
        channel_id: Optional[str] = None,
        custom_track_1: Optional[str] = None,
        custom_track_2: Optional[str] = None
    ) -> Dict[str, Any]:
        beats = self.load_manifest(project_name, channel_id)
        if not beats:
            beats = self.step_parse_script(project_name, channel_id)

        cfg = self.load_config(project_name, channel_id)
        ch_dir = os.path.join(self.base_channels, cfg.channel_id, "bgm")
        common_dir = os.path.join(self.base_channels, "common_assets", "bgm")

        from pipeline.bgm_engine import setup_project_bgm
        bgm_info = setup_project_bgm(
            project_dir=cfg.project_dir,
            beats=beats,
            common_bgm_dir=common_dir,
            channel_bgm_dir=ch_dir,
            custom_track_1=custom_track_1,
            custom_track_2=custom_track_2
        )

        cfg.bgm_file = bgm_info.get("track_1")
        cfg.bgm_mode = bgm_info.get("mode", "dual")
        cfg.bgm_track_1 = bgm_info.get("track_1")
        cfg.bgm_track_2 = bgm_info.get("track_2")
        cfg.bgm_transition_scene_id = bgm_info.get("transition_scene_id")
        cfg.bgm_volume_ducked = bgm_info.get("volume_ducked", 0.08)
        cfg.bgm_volume_normal = bgm_info.get("volume_normal", 0.22)

        # Update config and manifest
        pdir = cfg.project_dir
        with open(os.path.join(pdir, "project_config.json"), "w", encoding="utf-8") as f:
            json.dump(cfg.to_dict(), f, ensure_ascii=False, indent=2)

        self.save_manifest(project_name, beats, cfg, channel_id)
        return bgm_info

    def step_clean_videos(self, project_name: str, channel_id: Optional[str] = None) -> List[str]:
        """
        Cleans Google Flow watermarks from all MP4 videos in project_dir/videos/
        using Reverse Alpha Blending & Contour Laplace Diffusion.
        Preserves 100% original dimensions, framerates, and audio tracks.
        """
        from pipeline.video_watermark_remover import VideoWatermarkRemover
        cfg = self.load_config(project_name, channel_id)
        video_dir = os.path.join(cfg.project_dir, "videos")
        if not os.path.exists(video_dir):
            print(f"[ProjectManager] No video directory at: {video_dir}")
            return []
            
        video_files = [
            f for f in os.listdir(video_dir)
            if f.lower().endswith(".mp4") 
            and not f.endswith("_cleaned.mp4") 
            and not f.endswith("_raw_backup.mp4")
            and not f.endswith(".temp.mp4")
            and not os.path.exists(os.path.join(video_dir, f"{os.path.splitext(f)[0]}_raw_backup.mp4"))
        ]
        if not video_files:
            print(f"[ProjectManager] No raw videos found to clean in {video_dir}")
            return []
            
        remover = VideoWatermarkRemover()
        cleaned_files = []
        for v in video_files:
            in_path = os.path.join(video_dir, v)
            out_path = os.path.join(video_dir, f"{os.path.splitext(v)[0]}_cleaned.mp4")
            print(f"\n[ProjectManager] Cleaning watermark in {v}...")
            remover.process_video(in_path, out_path)
            
            # Safe backup of original raw file (overwrite backup if exists)
            backup_path = os.path.join(video_dir, f"{os.path.splitext(v)[0]}_raw_backup.mp4")
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(in_path, backup_path)
            os.rename(out_path, in_path)
            cleaned_files.append(in_path)
            print(f"[ProjectManager] Cleaned video replaced: {v}")
            
        print(f"\n[ProjectManager] All {len(cleaned_files)} videos cleaned cleanly with zero watermark!")
        return cleaned_files

    def sync_assets_to_remotion(self, project_name: str, channel_id: Optional[str] = None) -> str:
        cfg = self.load_config(project_name, channel_id)
        target_public = os.path.join(self.remotion_studio_dir, "public", "project_assets")
        
        target_audio = os.path.join(target_public, "audio")
        target_images = os.path.join(target_public, "images")
        target_videos = os.path.join(target_public, "videos")
        target_timings = os.path.join(target_public, "timings")
        target_bgm = os.path.join(target_public, "bgm")

        os.makedirs(target_audio, exist_ok=True)
        os.makedirs(target_images, exist_ok=True)
        os.makedirs(target_videos, exist_ok=True)
        os.makedirs(target_timings, exist_ok=True)
        os.makedirs(target_bgm, exist_ok=True)

        # Clear old assets from previous project render
        for folder in [target_audio, target_images, target_videos, target_timings, target_bgm]:
            for f in os.listdir(folder):
                try:
                    os.remove(os.path.join(folder, f))
                except Exception:
                    pass

        src_audio = os.path.join(cfg.project_dir, "audio")
        src_images = os.path.join(cfg.project_dir, "images")
        src_videos = os.path.join(cfg.project_dir, "videos")
        src_timings = os.path.join(cfg.project_dir, "timings")
        src_bgm = os.path.join(cfg.project_dir, "bgm")

        if os.path.exists(src_audio):
            for f in os.listdir(src_audio):
                p = os.path.join(src_audio, f)
                if os.path.isfile(p):
                    shutil.copy2(p, os.path.join(target_audio, f))

        if os.path.exists(src_images):
            for f in os.listdir(src_images):
                p = os.path.join(src_images, f)
                if os.path.isfile(p):
                    shutil.copy2(p, os.path.join(target_images, f))

        if os.path.exists(src_videos):
            for f in os.listdir(src_videos):
                p = os.path.join(src_videos, f)
                if os.path.isfile(p):
                    shutil.copy2(p, os.path.join(target_videos, f))

        if os.path.exists(src_timings):
            for f in os.listdir(src_timings):
                p = os.path.join(src_timings, f)
                if os.path.isfile(p):
                    shutil.copy2(p, os.path.join(target_timings, f))

        if os.path.exists(src_bgm):
            for f in os.listdir(src_bgm):
                p = os.path.join(src_bgm, f)
                if os.path.isfile(p):
                    shutil.copy2(p, os.path.join(target_bgm, f))

        # Copy manifest
        manifest_path = os.path.join(cfg.project_dir, "manifest.json")
        dest_manifest = os.path.join(target_public, "manifest.json")
        if os.path.exists(manifest_path):
            shutil.copy2(manifest_path, dest_manifest)

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_json = json.load(f)

        props_file = os.path.join(self.remotion_studio_dir, "current_props.json")
        with open(props_file, "w", encoding="utf-8") as f:
            json.dump({"manifest": manifest_json}, f, ensure_ascii=False, indent=2)

        print(f"[ProjectManager] Synced project assets to: {target_public}")
        return props_file

    def render_branding_assets(self, project_name: str, channel_id: Optional[str] = None, asset_type: str = "all") -> Dict[str, str]:
        """
        Renders YouTube thumbnail, channel logo, and channel banner
        in Simple Ways of Life 60FPS aesthetic via Remotion Still Engine.
        """
        cfg = self.load_config(project_name, channel_id)
        out_dir = os.path.join(cfg.project_dir, "out")
        os.makedirs(out_dir, exist_ok=True)
        branding_dir = os.path.join(self.base_channels, cfg.channel_id, "branding")
        os.makedirs(branding_dir, exist_ok=True)

        npx_cmd = "npx.cmd" if sys.platform == "win32" else "npx"
        rendered = {}

        if asset_type in ["all", "thumbnail"]:
            thumb_out = os.path.join(out_dir, "thumbnail_1080p.png").replace("\\", "/")
            cmd = [npx_cmd, "remotion", "still", "src/index.ts", "Thumbnail", thumb_out, "--overwrite"]
            print(f"[ProjectManager] Rendering Thumbnail -> {thumb_out}...")
            subprocess.run(cmd, cwd=self.remotion_studio_dir, check=True)
            rendered["thumbnail"] = thumb_out

        if asset_type in ["all", "logo"]:
            logo_out = os.path.join(branding_dir, "channel_logo_800p.png").replace("\\", "/")
            cmd = [npx_cmd, "remotion", "still", "src/index.ts", "ChannelLogo", logo_out, "--overwrite"]
            print(f"[ProjectManager] Rendering Channel Logo -> {logo_out}...")
            subprocess.run(cmd, cwd=self.remotion_studio_dir, check=True)
            shutil.copy2(logo_out, os.path.join(out_dir, "channel_logo_800p.png"))
            rendered["logo"] = logo_out

        if asset_type in ["all", "banner"]:
            banner_out = os.path.join(branding_dir, "channel_banner_2560p.png").replace("\\", "/")
            cmd = [npx_cmd, "remotion", "still", "src/index.ts", "ChannelBanner", banner_out, "--overwrite"]
            print(f"[ProjectManager] Rendering Channel Banner -> {banner_out}...")
            subprocess.run(cmd, cwd=self.remotion_studio_dir, check=True)
            shutil.copy2(banner_out, os.path.join(out_dir, "channel_banner_2560p.png"))
            rendered["banner"] = banner_out

        print(f"[ProjectManager] Successfully generated branding assets: {list(rendered.keys())}")
        return rendered

    def render_video(
        self,
        project_name: str,
        channel_id: Optional[str] = None,
        fps: Optional[int] = None,
        output_mp4: Optional[str] = None
    ) -> str:
        cfg = self.load_config(project_name, channel_id)
        if fps:
            cfg.fps = fps

        pdir = cfg.project_dir
        out_file = output_mp4 or os.path.join(pdir, "out", f"final_{cfg.fps}fps.mp4").replace("\\", "/")
        os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)

        self.step_resolve_assets(project_name, channel_id)
        self.step_setup_bgm(project_name, channel_id)
        props_file = self.sync_assets_to_remotion(project_name, channel_id)

        cmd = [
            "npx.cmd" if sys.platform == "win32" else "npx",
            "remotion",
            "render",
            "src/index.ts",
            "MainComposition",
            out_file,
            f"--props={props_file}",
            "--overwrite"
        ]

        print(f"\n[ProjectManager] Starting Remotion {cfg.fps}FPS Render -> {out_file}...")
        print(f"Executing: {' '.join(cmd)}\n")

        ret = subprocess.run(cmd, cwd=self.remotion_studio_dir)
        if ret.returncode != 0:
            raise RuntimeError(f"Remotion render failed with exit code {ret.returncode}")

        print(f"\n[ProjectManager] Video render completed successfully: {out_file}")
        return out_file
