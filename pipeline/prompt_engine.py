import os
from typing import List
from pipeline.models import SceneBeat, ProjectConfig
from pipeline.wardrobe import (
    build_single_scene_prompt,
    build_storyboard_motion_prompt,
    build_aiv_video_prompt
)

def generate_project_prompts(
    beats: List[SceneBeat],
    config: ProjectConfig,
    prompts_dir: str
) -> List[SceneBeat]:
    """
    Generates streamlined prompt files strictly formatted for Auto Flow Studio extension:
    - prompts_img_list.txt: All scenes (including 4-panel storyboard grids for AIV slots).
    - prompt_aiv_list.txt: AIV scenes only, used when referencing the storyboard image in Video tab.
    - Clean paragraph per scene, separated by newlines, with NO headers or tags.
    - Permanently cleans up and stops generating flow_prompts.csv and storyboards.json.
    """
    os.makedirs(prompts_dir, exist_ok=True)

    # 1. Permanently remove obsolete files if they exist
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
        # Determine image prompt: If AIV slot, use 4-panel storyboard grid to generate storyboard image first
        if beat.is_video_slot:
            target_dur = beat.fixed_duration or 6
            storyboard_img_prompt = build_storyboard_motion_prompt(
                text=beat.spoken_text,
                outfit_id=beat.outfit_id,
                target_duration=target_dur,
                scene_id=beat.scene_id
            )
            beat.prompt = storyboard_img_prompt
            beat.storyboard_prompt = storyboard_img_prompt
            img_prompt_blocks.append(storyboard_img_prompt.strip())

            # Video prompt for Video Tab (references the generated storyboard image)
            aiv_video_prompt = build_aiv_video_prompt(
                text=beat.spoken_text,
                outfit_id=beat.outfit_id,
                target_duration=target_dur,
                scene_id=beat.scene_id
            )
            aiv_prompt_blocks.append(f"[{beat.scene_id:03d}] ({target_dur}s AIV):\n{aiv_video_prompt.strip()}")
        else:
            single_img_prompt = build_single_scene_prompt(
                text=beat.spoken_text,
                outfit_id=beat.outfit_id,
                scene_id=beat.scene_id
            )
            beat.prompt = single_img_prompt
            img_prompt_blocks.append(single_img_prompt.strip())

    # Write prompts_img_list.txt: 1 paragraph per scene, separated by double newline
    with open(img_prompts_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(img_prompt_blocks) + "\n")

    # Write prompt_aiv_list.txt: 1 paragraph per AIV scene, separated by double newline
    with open(aiv_prompts_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(aiv_prompt_blocks) + "\n")

    print(f"[PromptEngine] Cleanly exported prompt lists for extension:\n  - {img_prompts_path} ({len(img_prompt_blocks)} image scenes)\n  - {aiv_prompts_path} ({len(aiv_prompt_blocks)} AIV scenes)")
    return beats
