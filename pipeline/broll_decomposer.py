import os
import json
import csv
from typing import List, Dict, Any, Optional
from pipeline.config import PipelineConfig, DEFAULT_CONFIG

# Common visual metaphors for personal finance & psychology topics
KEYWORD_VISUAL_MAP = [
    (["tiền", "money", "dollar", "thu nhập", "income", "cash"],
     "Stick figure character happily holding a stack of clean dollar bills, thought bubble showing rising cash coins"),
    (["tiết kiệm", "saving", "piggy bank", "heo đất", "dự phòng"],
     "Stick figure character gently placing a shiny gold coin into a smiling piggy bank on a simple wooden desk"),
    (["nợ", "debt", "lo lắng", "stress", "áp lực", "bills", "hóa đơn"],
     "Stick figure character sweating with worried face, looking at an enormous stack of unpaid bills and a heavy chain ball labeled DEBT"),
    (["não", "tâm lý", "psychology", "tư duy", "mindset", "suy nghĩ"],
     "Stick figure character with finger on chin thinking deeply, thought bubble above head showing glowing lightbulb and active golden gears"),
    (["đầu tư", "invest", "cổ phiếu", "stock", "tăng trưởng", "growth"],
     "Stick figure character pointing with confidence at a large wall whiteboard displaying an upward green trend graph"),
    (["hệ thống", "system", "kế hoạch", "plan", "ngân sách", "budget"],
     "Stick figure character proudly presenting an organized 3-part blueprint board labeled INCOME, SAVINGS, EXPENSES"),
    (["chi tiêu", "expenses", "mua sắm", "shopping", "cám dỗ"],
     "Stick figure character looking tempted at shopping bags and electronic gadgets on a store shelf, scratching head"),
    (["mục tiêu", "goal", "tự do", "freedom", "thành công", "success"],
     "Stick figure character standing on top of a mountain summit giving a joyful thumbs up, sun shining in background"),
    (["bẫy", "sai lầm", "mistake", "thất bại", "confusion"],
     "Stick figure character standing at a crossroads fork with question marks floating all around, looking puzzled")
]

def map_text_to_visual(text: str, default_action: str = "standing thoughtfully") -> str:
    """Finds matching visual metaphor from text, or returns default."""
    text_lower = text.lower()
    for keywords, visual in KEYWORD_VISUAL_MAP:
        if any(kw in text_lower for kw in keywords):
            return visual
    return f"Stick figure character {default_action}, simple line gesture, clear educational explainer"

def decompose_timeline_to_brolls(
    timeline: List[Dict[str, Any]],
    config: PipelineConfig = DEFAULT_CONFIG,
    custom_brand: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Splits long spoken segments into 3-5s dynamic B-roll visual cuts.
    Constructs full prompts using the Master Style.
    """
    char_tag = f"@{config.character_name} " if config.character_name else ""
    prefix = f"{char_tag}A striking cinematic hybrid illustration: "
    suffix = ", cinematic atmospheric 3D environment, dramatic lighting, rich depth of field, 16:9 landscape, high resolution, 4k."
    
    brolls = []
    cut_counter = 1
    
    for seg in timeline:
        start_t = seg["start"]
        end_t = seg["end"]
        duration = seg["duration"]
        text = seg.get("text", "")
        
        # Determine number of B-roll cuts based on duration
        if duration <= config.max_scene_duration:
            num_cuts = 1
        elif duration <= config.max_scene_duration * 1.8:
            num_cuts = 2
        else:
            num_cuts = max(2, int(duration // config.min_scene_duration))
            
        cut_duration = duration / num_cuts
        
        for sub_idx in range(num_cuts):
            c_start = round(start_t + sub_idx * cut_duration, 3)
            c_end = round(start_t + (sub_idx + 1) * cut_duration, 3)
            
            # Action variation for multiple cuts
            if num_cuts == 1:
                action_core = map_text_to_visual(text)
                shot_type = "medium_shot"
            elif sub_idx == 0:
                action_core = map_text_to_visual(text, default_action="explaining a concept with hands open")
                shot_type = "wide_shot"
            elif sub_idx == 1:
                action_core = "Close up of the character showing an expressive emotional reaction, eyes wide, smiling or pondering"
                shot_type = "close_up"
            else:
                action_core = "Detailed clean doodle diagram illustrating the key idea with clear arrows and icons"
                shot_type = "detail_shot"
                
            full_prompt = f"{prefix}{action_core}{suffix}"
            
            brolls.append({
                "cut_id": cut_counter,
                "scene_id": f"{cut_counter:04d}",
                "timestamp_start": c_start,
                "timestamp_end": c_end,
                "duration": round(c_end - c_start, 3),
                "spoken_text": text,
                "shot_type": shot_type,
                "visual_action": action_core,
                "full_prompt": full_prompt,
                "expected_image_name": f"{cut_counter:04d}.png"
            })
            cut_counter += 1
            
    return brolls

def export_brolls_to_csv_and_json(
    brolls: List[Dict[str, Any]],
    output_json_path: str,
    output_csv_path: str
):
    """
    Exports B-roll data to JSON and CSV.
    CSV format is ready to be loaded into Auto Flow Studio Extension table.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_json_path)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(brolls, f, ensure_ascii=False, indent=2)
        
    with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Row", "Cut_ID", "Duration", "Spoken_Context", "Prompt"])
        for b in brolls:
            writer.writerow([
                b["scene_id"],
                b["cut_id"],
                b["duration"],
                b["spoken_text"],
                b["full_prompt"]
            ])
            
    print(f"[B-Roll Decomposer] Generated {len(brolls)} dynamic B-roll visual cuts.")
    print(f" -> Saved JSON: {output_json_path}")
    print(f" -> Saved CSV for Auto Flow Studio: {output_csv_path}")
