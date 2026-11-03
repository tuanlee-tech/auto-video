import os
from typing import List
from pipeline.models import SceneBeat, ProjectConfig
from pipeline.wardrobe import (
    build_single_scene_prompt,
    build_storyboard_motion_prompt,
    build_aiv_video_prompt,
    select_outfit_and_mood
)
from pipeline.prompts_catalog import SCENE_PROMPTS_DATA

def generate_project_prompts(
    beats: List[SceneBeat],
    config: ProjectConfig,
    prompts_dir: str,
    enable_aiv: bool = False,
    aiv_scene_count: int = 5
) -> List[SceneBeat]:
    """
    Generates streamlined prompt files strictly formatted for Auto Flow Studio extension:
    - prompts_img_list.txt: Full single 16:9 cinematic image prompts for ALL scenes, OR
      4-panel storyboard motion sequence grids for AIV slots (first N scenes when enable_aiv=True).
    - Decoupled Character System:
      * Hero scenes (~15-25%): prompts start with @stickman.
      * Concept/Metaphor/Infographic scenes (~75-85%): pure cinematic B-roll without stickman.
    - When enable_aiv=False: 100% full images, no 4-panel storyboard grids, no AIV video list.
    - When enable_aiv=True:
      * Initial scenes (1 to aiv_scene_count): 4-panel motion grids in prompts_img_list.txt AND prompt_aiv_list.txt.
      * Remaining scenes (aiv_scene_count + 1 to end): Single complete 16:9 cinematic images.
    """
    os.makedirs(prompts_dir, exist_ok=True)

    # Permanently remove obsolete/legacy files if they exist
    obsolete_files = ["flow_prompts.csv", "storyboards.json", "prompts_list.txt"]
    for ob in obsolete_files:
        p = os.path.join(prompts_dir, ob)
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    img_prompts_path = os.path.join(prompts_dir, "prompts_img_list.txt").replace("\\", "/")
    aiv_prompts_path = os.path.join(prompts_dir, "prompt_aiv_list.txt").replace("\\", "/")

    img_prompt_blocks = []
    aiv_prompt_blocks = []

    for beat in beats:
        # Check if master curated catalog has dedicated director prompts for this scene
        catalog_entry = SCENE_PROMPTS_DATA.get(beat.scene_id)
        if catalog_entry:
            beat.scene_type = catalog_entry.get("scene_type", beat.scene_type)
            if catalog_entry.get("outfit_id"):
                beat.outfit_id = catalog_entry["outfit_id"]
        elif beat.scene_type == "hero":
            oid, oinfo = select_outfit_and_mood(beat.spoken_text, beat.scene_id)
            beat.outfit_id = oid
            beat.outfit_name = oinfo["name"]

        # Determine if this scene is an AIV slot
        is_aiv_slot = enable_aiv and (beat.scene_id <= aiv_scene_count)

        if is_aiv_slot:
            beat.is_video_slot = True
            # Choose optimal fixed duration for Omni Flash 1.1 (4s, 6s, 8s, 10s) based on speech
            if not beat.fixed_duration:
                speech_dur = getattr(beat, "duration_sec", 6.0) or 6.0
                if catalog_entry and catalog_entry.get("fixed_duration"):
                    beat.fixed_duration = catalog_entry["fixed_duration"]
                elif speech_dur >= 10.0:
                    beat.fixed_duration = 10
                elif speech_dur >= 7.0:
                    beat.fixed_duration = 8
                elif speech_dur >= 4.0:
                    beat.fixed_duration = 6
                else:
                    beat.fixed_duration = 4
            target_dur = beat.fixed_duration

            if catalog_entry and catalog_entry.get("img_prompt"):
                storyboard_img_prompt = catalog_entry["img_prompt"]
            else:
                storyboard_img_prompt = build_storyboard_motion_prompt(
                    beat=beat,
                    target_duration=target_dur
                )
            beat.prompt = storyboard_img_prompt
            beat.storyboard_prompt = storyboard_img_prompt
            img_prompt_blocks.append(storyboard_img_prompt.strip())

            if catalog_entry and catalog_entry.get("aiv_prompt"):
                aiv_video_prompt = catalog_entry["aiv_prompt"]
            else:
                aiv_video_prompt = build_aiv_video_prompt(
                    beat=beat,
                    target_duration=target_dur
                )
            aiv_prompt_blocks.append(f"[{beat.scene_id:03d}] ({target_dur}s AIV):\n{aiv_video_prompt.strip()}")
        else:
            # Full Image Mode: Single, complete 16:9 cinematic image
            beat.is_video_slot = False
            beat.fixed_duration = None
            beat.storyboard_prompt = None
            beat.asset_type = "image"
            if catalog_entry and catalog_entry.get("img_prompt"):
                single_img_prompt = catalog_entry["img_prompt"]
            else:
                single_img_prompt = build_single_scene_prompt(beat=beat)
            beat.prompt = single_img_prompt
            img_prompt_blocks.append(single_img_prompt.strip())

    # Write prompts_img_list.txt: 1 paragraph per scene, separated by double newline
    with open(img_prompts_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(img_prompt_blocks) + "\n")

    # If AIV is enabled and we have AIV blocks, write prompt_aiv_list.txt; otherwise remove it
    if enable_aiv and aiv_prompt_blocks:
        with open(aiv_prompts_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(aiv_prompt_blocks) + "\n")
    else:
        if os.path.exists(aiv_prompts_path):
            try:
                os.remove(aiv_prompts_path)
            except Exception:
                pass

    hero_count = sum(1 for b in beats if b.scene_type == "hero")
    broll_count = len(beats) - hero_count
    aiv_count = len(aiv_prompt_blocks)
    img_only_count = len(img_prompt_blocks) - aiv_count
    print(f"[PromptEngine] Cleanly exported prompt lists ({len(beats)} total scenes):")
    print(f"               File: {img_prompts_path}")
    if aiv_count > 0:
        print(f"               File: {aiv_prompts_path} ({aiv_count} AIV video prompts)")
        print(f"               Structure: Scenes 1-{aiv_count} are 4-Panel AIV Storyboard Grids; Scenes {aiv_count+1}-{len(beats)} are Single 16:9 Cinematic Images")
    else:
        print(f"               Structure: All {len(beats)} scenes are 100% Full Single 16:9 Images (No AIV)")
    print(f"               Hero Stickman scenes: {hero_count} ({hero_count/len(beats)*100:.1f}%) | Pure Concept B-Roll scenes: {broll_count} ({broll_count/len(beats)*100:.1f}%)")
    return beats
