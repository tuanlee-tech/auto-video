import re
from typing import Dict, Any, Tuple, Optional
from pipeline.models import SceneBeat

# ==============================================================================
# 1. MASTER 10-OUTFIT COLLECTION FOR HERO STICKMAN (25-30% of scenes)
# ==============================================================================
WARDROBE_COLLECTION = {
    1: {
        "name": "Philosophical Trench Coat",
        "description": "dark tailored trench coat and burgundy turtleneck",
        "keywords": ["tại sao", "câu hỏi", "suy nghĩ", "triết học", "nguyên lý", "bản chất", "tâm lý", "não bộ", "nhận thức", "tư duy"],
        "default_setting": "a vast, moody brutalist concrete hallway with towering pillars, atmospheric mist, cold desaturated teal-gray lighting, dramatic shadows",
        "camera_motion": "zoom_in"
    },
    2: {
        "name": "Wall Street Business Suit",
        "description": "sharp black business suit with tie, carrying a briefcase",
        "keywords": ["đầu tư", "chứng khoán", "tài chính", "thị trường", "tài sản", "lợi nhuận", "kinh doanh", "cổ phiếu"],
        "default_setting": "a sleek modern financial banking hall or futuristic vault with clean architectural lines, volumetric lighting",
        "camera_motion": "pan_right"
    },
    3: {
        "name": "Tech Startup Blazer",
        "description": "modern dark blazer and white crewneck t-shirt",
        "keywords": ["hệ thống", "khởi nghiệp", "sáng tạo", "phân luồng", "tự động hóa", "chiến lược", "sơ đồ", "quy tắc", "giải pháp"],
        "default_setting": "a high-tech minimalist design studio with transparent glass whiteboard showing glowing diagrams",
        "camera_motion": "zoom_out"
    },
    4: {
        "name": "Overworked Dress Shirt",
        "description": "overworked wrinkled white dress shirt with loosened tie",
        "keywords": ["áp lực", "hóa đơn", "nợ", "kiệt sức", "tăng ca", "deadline", "bế tắc", "lo lắng", "chi tiêu quá mức", "tiêu xài", "bốc hơi"],
        "default_setting": "a dim high-end corporate glass office late at night, city skyline through rainy windows, fluorescent strip lighting casting hard shadows",
        "camera_motion": "pan_left"
    },
    5: {
        "name": "Stormproof Windbreaker",
        "description": "navy hooded outdoor windbreaker jacket, backpack on shoulders",
        "keywords": ["giông bão", "kiên trì", "mục tiêu", "vượt qua", "hải đăng", "thử thách", "chống lại", "ý chí", "đứng vững", "cám dỗ"],
        "default_setting": "a dark stone pier beside a rustic weathered lighthouse casting a powerful golden beam into a stormy night ocean",
        "camera_motion": "zoom_in"
    },
    6: {
        "name": "Minimalist Casual",
        "description": "casual minimalist blue t-shirt and dark chinos",
        "keywords": ["hàng ngày", "sinh hoạt", "tiêu dùng", "mua sắm", "lối sống", "bình thường", "chi tiêu", "ví tiền"],
        "default_setting": "a warm, sunlit European street or modern minimalist cafe with natural golden morning light",
        "camera_motion": "pan_right"
    },
    7: {
        "name": "Scholar Cardigan",
        "description": "cozy knitted cardigan and reading glasses, holding an open book",
        "keywords": ["sách", "học hỏi", "kiến thức", "nghiên cứu", "đọc", "phân tích", "bài học", "hiểu biết", "toán học", "bảng tính"],
        "default_setting": "a warm wooden library with floor-to-ceiling bookshelves and soft ambient desk lamp glow",
        "camera_motion": "zoom_in"
    },
    8: {
        "name": "Athletic Discipline",
        "description": "black athletic gym sportswear and running hoodie",
        "keywords": ["kỷ luật", "rèn luyện", "thói quen", "thể thao", "dậy sớm", "dopamine detox", "kiểm soát", "nỗ lực", "thắt lưng buộc bụng"],
        "default_setting": "a high-contrast industrial gym or running path at early dawn with dramatic rim lighting",
        "camera_motion": "pan_left"
    },
    9: {
        "name": "Cozy Home Sweater",
        "description": "oversized warm brown knit sweater, holding a steaming coffee mug",
        "keywords": ["bình yên", "an tâm", "thoải mái", "tự do tài chính", "thong dong", "buổi sáng", "thư giãn", "tiết kiệm"],
        "default_setting": "a cozy modern sun-drenched living room with warm wooden furniture and potted plants",
        "camera_motion": "zoom_out"
    },
    10: {
        "name": "Vulnerable Orange Blanket",
        "description": "wrapped comfortably in a warm folded orange knit blanket",
        "keywords": ["hoang mang", "thất bại", "yếu đuối", "cô đơn", "chữa lành", "đồng cảm", "bất lực", "buồn bã"],
        "default_setting": "sitting curled on a sofa by a huge floor-to-ceiling window watching rain droplets trickle down at twilight",
        "camera_motion": "pan_left"
    }
}

# ==============================================================================
# 2. SEMANTIC B-ROLL CATALOG (70-75% of scenes: Zero Stickman)
# ==============================================================================
SEMANTIC_BROLL_CATALOG = [
    # Neuroscience & Psychology
    (
        ["vỏ não", "não bộ", "thần kinh", "cộng hưởng từ", "hạch hạnh nhân", "khối óc"],
        "infographic",
        "A sophisticated 3D scientific visualization of a transparent human brain model floating in dark space: glowing neural pathways in the prefrontal cortex and amygdala pulsing with amber and electric cyan synaptic currents. Sleek dark holographic aesthetic, shallow depth of field, high-contrast chiaroscuro studio lighting",
        "dark high-tech neuroscience laboratory background"
    ),
    (
        ["dopamine", "hưng phấn", "cám dỗ", "thông báo", "màn hình"],
        "infographic",
        "A close-up cinematic shot of an ultra-modern smartphone on a textured slate desk: vibrant glowing red and amber notification badges illuminating the dark environment, visualizing dopamine reward pulses with delicate luminous particle trails. Cinematic chiaroscuro lighting, subtle reflections",
        "moody minimalist workspace late at night"
    ),
    (
        ["khan hiếm", "tầm nhìn đường hầm", "thiếu thốn", "nỗi sợ"],
        "metaphor",
        "A dramatic visual metaphor of narrow tunnel vision: a sharp, narrow cone of cold spotlight penetrating an abyss of absolute darkness to illuminate a single small coin on a cracked stone pedestal, while surrounding vast opportunities remain veiled in heavy mist. Chiaroscuro shadows, cinematic contrast",
        "vast dark cavernous space with atmospheric fog"
    ),
    (
        ["iq", "13 điểm", "suy giảm", "đồng hồ", "đêm trắng"],
        "infographic",
        "A sleek minimalist 3D metric HUD: an elegant luminous circular gauge sharply dropping into an amber caution zone, next to an illuminated digital alarm clock glowing at 3:45 AM on a sleek bedside table. Desaturated teal shadows, soft amber focal lighting",
        "quiet bedroom atmosphere in early morning darkness"
    ),
    (
        ["nguyên thủy", "tổ tiên", "lửa", "hang đá", "săn bắn"],
        "metaphor",
        "A primeval atmospheric cinematic scene: an ancient glowing campfire burning quietly on the stone floor of a prehistoric cave, casting flickering warm orange light and dancing shadows on rough textured rock walls, with glowing embers rising into the cool darkness. Volumetric light, cinematic realism",
        "ancient natural cavern opening to starry night sky"
    ),
    # Two-Box Cash Flow & Banking Automation
    (
        ["quy tắc hai chiếc hộp", "hai chiếc hộp", "phân luồng", "80%", "20%"],
        "infographic",
        "A sleek 3D architectural financial mechanism: Two distinct transparent glowing crystal containers resting on dark polished granite. The primary container has a steady vibrant green conduit for everyday living; the secondary locked crystalline vault continuously accumulates glowing solid gold bullion. A single stream of golden light splits cleanly into two separate flow paths. 3D isometric layout, ultra-clean design",
        "futuristic minimalist financial sanctum"
    ),
    (
        ["ứng dụng ngân hàng", "ngân hàng số", "tự động trích", "lệnh chuyển tiền", "mùng 5"],
        "infographic",
        "A macro cinematic shot of a sleek bezel-less smartphone resting on an oak surface: the screen displays a beautiful dark-mode banking app interface with a toggled glowing emerald switch for automated monthly salary transfer, subtle glowing progress charts, elegant financial UI design",
        "warm contemporary home office with soft ambient lamp glow"
    ),
    (
        ["phương trình", "đảo ngược phương trình", "thu nhập trừ", "công thức"],
        "infographic",
        "A high-contrast cinematic typography visualization of an inverted financial equation: 'INCOME - AUTOMATED WEALTH = LIVING EXPENSES' rendered in clean luminous gold and white sans-serif lettering on a textured dark graphite wall, glowing gently with subtle volumetric light rays",
        "modern brutalist architectural studio"
    ),
    (
        ["con heo đất", "tiết kiệm kham khổ", "sai lầm", "đổ vỡ"],
        "metaphor",
        "A dramatic cinematic still life: a classic ceramic piggy bank shattered on a dark textured slate surface, with scattered coins slowly dissolving into faint golden mist and vapor under a single harsh cold tungsten spotlight, chiaroscuro shadows",
        "moody dark studio table with dramatic side lighting"
    ),
    (
        ["đồng hồ cát", "thời gian", "tích lũy", "lãi kép", "năm tháng"],
        "metaphor",
        "A macro cinematic shot of an ornate vintage brass hourglass resting on an aged dark oak table: shimmering golden sand flows continuously through the narrow glass neck, accumulating into a majestic mound of golden wealth at the base. Warm amber tungsten lighting, soft bokeh highlights",
        "antique wooden scholar study with soft volumetric haze"
    ),
    (
        ["chi tiêu phình to", "bong bóng", "tiêu sạch", "bốc hơi"],
        "metaphor",
        "A powerful visual metaphor for expanding expenditure: a delicate, giant iridescent soap bubble stretching and expanding under rising pressure until it reaches bursting point over a dark reflective water pool. Cold moody teal and magenta reflections, high-speed photography aesthetic",
        "dark studio with water surface reflections"
    ),
    (
        ["ma sát", "48 giờ", "đóng băng", "thẻ ngân hàng", "cảm xúc"],
        "metaphor",
        "A striking cinematic shot: a modern matte black banking credit card completely frozen solid inside a clear cube of crystalline ice, resting on a dark slate tabletop with condensation droplets trickling down under dramatic cold rim lighting",
        "minimalist dark studio setting with crisp blue rim light"
    ),
    (
        ["con số vận hành tối thiểu", "chi phí thiết yếu", "sống tối thiểu", "nền tảng"],
        "infographic",
        "A crisp 3D minimalist financial dashboard: a solid glowing horizontal bedrock baseline clearly dividing essential living expenditures below from discretionary lifestyle inflation above, clean glowing emerald markers and isometric financial architecture",
        "sleek dark glass aesthetic with subtle grid reflections"
    ),
    (
        ["tự do", "không tội lỗi", "thoải mái", "thanh thản", "cà phê"],
        "metaphor",
        "A tranquil cinematic still life: a steaming ceramic cup of freshly brewed black coffee and an open leather journal resting on a warm oak table beside a sunlit window, with gentle morning sunlight casting long warm shadows across the room. Serene golden hour atmosphere, peace of mind",
        "sun-drenched minimalist Scandinavian living room"
    ),
    (
        ["hệ thống tự động", "cỗ máy", "bánh răng", "vận hành"],
        "metaphor",
        "A magnificent precision clockwork automaton: interlocking polished brass and stainless steel gears rotating smoothly in perfect silent synchronization, transferring glowing gold spheres through tempered glass tracks with effortless kinetic efficiency. Warm cinematic volumetric lighting",
        "intricate horological vault interior"
    ),
    (
        ["giông bão", "ngọn hải đăng", "vượt qua", "kiên định", "đứng vững"],
        "metaphor",
        "A cinematic wide shot of a rugged weathered stone lighthouse standing resolute on a dark ocean cliff, casting a brilliant volumetric golden searchlight beam through torrential rain and crashing stormy waves into the dark night sky. Epic cinematic atmosphere, high contrast",
        "stormy nocturnal ocean seascape with crashing surf"
    ),
    (
        ["hành trình", "chân lý", "bình minh", "kết thúc", "tự chủ"],
        "metaphor",
        "A breathtaking cinematic wide panorama: dramatic storm clouds parting over a calm open sea as a brilliant golden sunrise floods the tranquil horizon with warm amber and peach radiance, casting shimmering reflections on the water. Epic scale, cinematic depth, quiet triumph",
        "infinite calm ocean horizon at dawn"
    ),
    (
        ["văn phòng", "hóa đơn", "cuối tháng", "lương"],
        "environment",
        "A cinematic establishing view of a dim contemporary office desk at midnight: an illuminated calculator, neatly stacked invoices, and an empty coffee cup beside a floor-to-ceiling glass window showing wet city skyline reflections in the rain. Cold desaturated teal-gray tones, lonely urban atmosphere",
        "high-rise corporate tower at night"
    )
]

def clean_spoken_text(text: str) -> str:
    """Strips bracketed emotion tags like [thở dài], [cười] for clean processing."""
    return re.sub(r"\[.*?\]", "", text).strip()

def select_outfit_and_mood(text: str, index: int = 1) -> Tuple[int, Dict[str, Any]]:
    """Analyzes spoken text and selects matching outfit and mood for Hero scenes."""
    clean_text = clean_spoken_text(text).lower()
    best_id = None
    max_score = 0

    for oid, data in WARDROBE_COLLECTION.items():
        score = sum(1 for kw in data["keywords"] if kw in clean_text)
        if score > max_score:
            max_score = score
            best_id = oid

    if best_id is None:
        fallbacks = [1, 3, 2, 8, 9, 6]
        best_id = fallbacks[(index - 1) % len(fallbacks)]

    return best_id, WARDROBE_COLLECTION[best_id]

def get_broll_concept(text: str, scene_id: int) -> Tuple[str, str, str]:
    """
    Finds the most accurate semantic B-roll visual concept and setting.
    Returns: (type, visual_description, setting)
    """
    clean = clean_spoken_text(text).lower()

    for keywords, btype, visual_desc, setting in SEMANTIC_BROLL_CATALOG:
        if any(kw in clean for kw in keywords):
            return btype, visual_desc, setting

    # Fallback B-roll if no specific keyword matched
    generic_fallbacks = [
        ("metaphor", "An intricate kinetic mechanism of polished brass gears and glowing glass conduits routing steady streams of golden light into organized containers", "dark modern architectural sanctuary"),
        ("infographic", "A sleek 3D holographic data visual showing glowing interconnected financial nodes and upward compounding curves in cyan and gold", "minimalist dark technical studio"),
        ("metaphor", "A macro cinematic shot of a vintage brass hourglass with golden sand trickling smoothly into an expanding mound of solid gold bullion", "warm wooden library with atmospheric lighting"),
        ("environment", "A tranquil wide cinematic vista of a quiet modern city at dawn with golden morning light illuminating contemporary glass facades", "peaceful urban landscape at sunrise")
    ]
    return generic_fallbacks[(scene_id - 1) % len(generic_fallbacks)]

# ==============================================================================
# 3. PROMPT GENERATION ENGINES
# ==============================================================================

def build_hero_prompt(text: str, outfit_id: int, scene_id: int = 1) -> str:
    """
    Generates Hero Character prompt featuring @stickman in specific outfit.
    Used for 25-30% of scenes (intro, outro, emotional milestones).
    """
    outfit = WARDROBE_COLLECTION.get(outfit_id, WARDROBE_COLLECTION[1])
    
    # Hero action based on emotional tone
    clean = clean_spoken_text(text).lower()
    if any(k in clean for k in ["tại sao", "câu hỏi", "suy nghĩ"]):
        action = "standing in quiet introspection, gazing thoughtfully upward with focused contemplation"
    elif any(k in clean for k in ["áp lực", "hóa đơn", "kiệt sức", "tự trách"]):
        action = "sitting slumped beside a desk with hands holding his face in deep regret and stress"
    elif any(k in clean for k in ["hệ thống", "quy tắc", "giải pháp", "tôi sẽ"]):
        action = "standing with calm confidence, gesturing with an open hand toward illuminated conceptual diagrams"
    elif any(k in clean for k in ["kết thúc", "hành trình", "bình minh", "tự chủ", "keep it simple"]):
        action = "standing tall with a peaceful, confident smile looking out toward an open golden horizon"
    else:
        action = "standing with relaxed confidence, looking directly toward the viewer with an inviting gesture"

    prompt = (
        f"@stickman wearing his {outfit['description']}, {action}. "
        f"Set in {outfit['default_setting']}. "
        f"Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
        f"16:9 landscape aspect ratio, cinematic depth of field, chiaroscuro lighting, "
        f"clean cinematic render, no watermarks, no logos, no text, no speech bubbles, no subtitles."
    )
    return prompt

def build_broll_prompt(text: str, scene_type: str, scene_id: int = 1) -> str:
    """
    Generates rich concept B-roll prompt with ZERO stickman.
    Focuses 100% on the object, diagram, visual metaphor, or environment.
    """
    _, visual_desc, setting = get_broll_concept(text, scene_id)

    prompt = (
        f"{visual_desc}. "
        f"Set in {setting}. "
        f"16:9 landscape aspect ratio, cinematic depth of field, chiaroscuro lighting, volumetric atmosphere, "
        f"photorealistic 3D render, ultra-clean aesthetic, "
        f"no human figures, no characters, no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
    )
    return prompt

def build_single_scene_prompt(beat: SceneBeat) -> str:
    """
    Unified router for image prompts:
    - If scene_type == 'hero' -> Hero Stickman Prompt
    - If scene_type != 'hero' -> Pure Concept B-roll Prompt (NO STICKMAN)
    """
    if beat.scene_type == "hero":
        return build_hero_prompt(beat.spoken_text, beat.outfit_id, beat.scene_id)
    else:
        return build_broll_prompt(beat.spoken_text, beat.scene_type, beat.scene_id)

def build_storyboard_motion_prompt(beat: SceneBeat, target_duration: int = 6) -> str:
    """
    Generates a 4-panel storyboard motion sequence grid (2x2) for AI video slots.
    If Hero -> Stickman motion progression.
    If B-roll -> Cinematic mechanism / metaphor motion progression.
    """
    if beat.scene_type == "hero":
        outfit = WARDROBE_COLLECTION.get(beat.outfit_id, WARDROBE_COLLECTION[1])
        prompt = (
            f"A professional 4-panel storyboard motion sequence grid (2x2 layout, 4 sequential frames) "
            f"showing continuous visual cinematic movement for @stickman wearing his {outfit['description']} "
            f"illustrating a {target_duration}-second progression. "
            f"Set in {outfit['default_setting']}. "
            f"Panel 1 (Top-Left): Establishing wide shot, initial atmospheric buildup. "
            f"Panel 2 (Top-Right): Slow camera push-in as @stickman initiates decisive physical action. "
            f"Panel 3 (Bottom-Left): Dynamic climactic motion with striking visual lighting transformation. "
            f"Panel 4 (Bottom-Right): Serene cinematic conclusion with lingering visual resonance. "
            f"Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            f"cinematic lighting, 16:9 aspect ratio. "
            f"CRITICAL REQUIREMENTS: Expressive visual motion, character may have natural mouth gestures and speaking expressions with no audible dialogue, silent vocal track (subtle ambient sound effects or SFX acceptable), no background music, no musical soundtrack, no watermarks, no logos, no text overlays, no subtitles."
        )
    else:
        _, visual_desc, setting = get_broll_concept(beat.spoken_text, beat.scene_id)
        prompt = (
            f"A professional 4-panel storyboard motion sequence grid (2x2 layout, 4 sequential frames) "
            f"showing continuous cinematic mechanical and atmospheric motion for a visual concept: {visual_desc}. "
            f"Set in {setting}. "
            f"Panel 1 (Top-Left): Establishing wide shot, initial atmospheric buildup. "
            f"Panel 2 (Top-Right): Slow camera push-in as internal mechanisms activate and streams begin flowing. "
            f"Panel 3 (Bottom-Left): Dynamic climactic transformation with luminous energy routing smoothly. "
            f"Panel 4 (Bottom-Right): Serene cinematic resolution with stable glowing equilibrium. "
            f"Photorealistic 3D render, volumetric cinematic lighting, 16:9 aspect ratio, NO human characters. "
            f"CRITICAL REQUIREMENTS: Smooth physical and particle motion, subtle ambient sound effects or SFX acceptable, no audible vocal track, no background music, no musical soundtrack, no watermarks, no logos, no text overlays, no subtitles."
        )
    return prompt

def build_aiv_video_prompt(beat: SceneBeat, target_duration: int = 6) -> str:
    """
    Generates video prompt for AI Video tab (Veo / Omni Flash),
    referencing the 4-panel storyboard image grid.
    Forces SINGLE full-screen viewport with NO split screen.
    """
    if beat.scene_type == "hero":
        outfit = WARDROBE_COLLECTION.get(beat.outfit_id, WARDROBE_COLLECTION[1])
        prompt = (
            f"Single full-screen continuous cinematic camera shot (NO split-screen, NO 4-panel grid, NO collage, NO frame borders). "
            f"The 4 panels in the reference image are strictly a conceptual storyboard keyframe guide illustrating motion progression across time. "
            f"Synthesize the action into ONE seamless, full-frame {target_duration}-second camera sequence: "
            f"begin with the initial scene setup from Panel 1, smoothly push in as @stickman wearing his {outfit['description']} initiates physical motion from Panel 2, "
            f"dynamically transition through the climactic action from Panel 3, "
            f"and fluidly resolve into the final posture from Panel 4. "
            f"Set in {outfit['default_setting']}. Photorealistic 3D environment, cinematic depth of field, chiaroscuro lighting, consistent 2D minimalist character with white round head and bold ink outlines, single unified 16:9 viewport. "
            f"CRITICAL REQUIREMENTS: Single camera viewport only, full-screen frame, absolutely no split-screen, no 2x2 grid layout, no multiple panels, no collage, no borders, no sub-frames, expressive visual motion, character may have natural mouth gestures and speaking expressions with no audible dialogue, silent vocal track (subtle ambient sound effects or SFX acceptable), no background music, no musical soundtrack, no watermarks, no logos, no text overlays, no subtitles."
        )
    else:
        _, visual_desc, setting = get_broll_concept(beat.spoken_text, beat.scene_id)
        prompt = (
            f"Single full-screen continuous cinematic camera shot (NO split-screen, NO 4-panel grid, NO collage, NO frame borders). "
            f"The 4 panels in the reference image are strictly a conceptual keyframe guide illustrating dynamic mechanical progression across time. "
            f"Synthesize the action into ONE seamless, full-frame {target_duration}-second camera sequence: "
            f"begin with the establishing shot from Panel 1: {visual_desc}, "
            f"smoothly glide the camera closer as glowing mechanisms and fluid conduits activate in Panel 2, "
            f"dynamically showcase the peak mechanical efficiency in Panel 3, "
            f"and settle smoothly into the peaceful equilibrium of Panel 4. "
            f"Set in {setting}. Photorealistic 3D render, depth of field, volumetric cinematic lighting, NO human characters, single unified 16:9 viewport. "
            f"CRITICAL REQUIREMENTS: Single camera viewport only, full-screen frame, absolutely no split-screen, no 2x2 grid layout, no multiple panels, no collage, no borders, no sub-frames, subtle ambient sound effects or SFX acceptable, no audible vocal track, no background music, no musical soundtrack, no watermarks, no logos, no text overlays, no subtitles."
        )
    return prompt
