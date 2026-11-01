import re
from typing import Dict, Any, Tuple, Optional

# Master 10-Outfit Collection from GEMINI.md
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

# Semantic visual action concepts mapped by narrative keywords (Pure English, NO Vietnamese quotes)
CONCEPT_VISUAL_MAP = [
    (["kiếm tiền đã khó", "câu hỏi", "tại sao"], 
     "standing alone in deep introspection, gazing upward at a giant glowing red neon question mark floating in the air with atmospheric haze and wet floor reflections",
     "brutalist concrete hall with towering columns and cold teal lighting"),
    (["giữ được tiền", "khó hơn gấp mười lần"],
     "holding an empty worn leather wallet upside down as faint dust particles drift out, bewildered and stressed facial expression",
     "dark moody city street at night with blurry bokeh of rain and distant traffic lights"),
    (["tiết kiệm", "tự hứa"],
     "sitting resolutely at a rustic wooden desk by an open window at dawn, placing a shiny gold coin beside a small porcelain piggy bank",
     "quiet minimalist study room with soft morning light slicing through shadows"),
    (["bốc hơi", "số dư"],
     "looking utterly shocked with wide cartoon eyes and dropped jaw in front of an automated banking terminal glowing with harsh neon blue",
     "rain-soaked dark alleyway with puddles reflecting moody neon streetlights"),
    (["hóa đơn", "bế tắc", "áp lực"],
     "sweating nervously, struggling to carry a massive leaning tower of heavy red document binders and unpaid bill envelopes",
     "dim high-end corporate glass office late at night, city skyline through rainy windows"),
    (["toán học", "bài toán"],
     "scratching head in exhaustion and confusion in front of a monumental black chalkboard completely covered with dizzying complex mathematical calculus formulas",
     "vast historic lecture amphitheater with atmospheric dust beams and dark academic lighting"),
    (["excel", "bảng tính"],
     "feeling trapped and tiny, sitting slumped inside a pitch-black digital server room surrounded by towering curved computer monitors displaying endless cascading spreadsheet grids",
     "high-tech server room with cold green chiaroscuro digital glare"),
    (["tâm lý học", "não bộ", "90%"],
     "looking up with wonder and deep thought at a giant translucent floating human brain sculpture glowing with golden neural networks and pulsing synaptic lights",
     "sleek modern brutalist art gallery with polished concrete floors and volumetric haze"),
    (["dopamine", "phần thưởng tức thì"],
     "with wide enchanted cartoon eyes, gazing into a dazzling luxury retail store display window radiating intense warm golden light and tempting merchandise",
     "dark rainy city sidewalk at night with vibrant wet street reflections"),
    (["mua sắm", "món đồ mới", "bữa ăn ngon"],
     "with a joyful cartoon smile, sitting at a candle-lit corner table of an upscale bistro restaurant enjoying a steaming gourmet meal and coffee",
     "warm amber tungsten restaurant interior with soft background bokeh blur"),
    (["không hề được thiết kế", "tiết kiệm bất động"],
     "resting chin on palm with bored unimpressed eyes, sitting on a simple metal stool in a stark cold minimalist room beside a heavy locked steel bank deposit box",
     "cold gray minimalist concrete room with hard industrial shadows"),
    (["tài khoản tiết kiệm", "heo đất"],
     "a solitary porcelain white piggy bank resting on an austere weathered stone pedestal in the center of an empty shadowy museum hall illuminated by a single vertical cold spotlight beam",
     "melancholy museum hall with atmospheric shadows"),
    (["ý chí", "thắt lưng buộc bụng"],
     "gritting teeth with sweat droplets flying, running furiously on a mechanical industrial treadmill in a vast warehouse, staying in the exact same spot",
     "vast dark industrial warehouse with dramatic high-contrast overhead spotlights"),
    (["kiệt sức", "thất bại"],
     "with sad tired eyes, sitting curled up on a dark gray couch looking out of a huge curved floor-to-ceiling window at a rainy twilight city skyline with rain trickling down glass",
     "dim cozy twilight apartment interior with soft moody ambient lighting"),
    (["ngừng chiến đấu", "chiến thắng"],
     "with a serene peaceful smile and eyes gently closed, taking a calm deep breath as warm golden morning sunbeams pour through a high geometric skylight, breaking all dark shadows",
     "sun-drenched architectural atrium with floating warm golden light beams"),
    (["hệ thống", "tự động vận hành", "thay vào đó"],
     "standing with quiet pride beside a monumental, intricately crafted golden clockwork mechanism with smooth rotating brass gears and polished bronze cogs",
     "grand architectural library with rich warm golden illumination and atmospheric dust particles"),
    (["hai chiếc hộp", "nguyên lý cốt lõi"],
     "standing behind a sleek wooden architect table, introducing two distinct glowing sculptural boxes: one minimalist dark obsidian box and one glowing golden vault chest",
     "clean geometric design studio with focused studio spotlighting"),
    (["gom toàn bộ", "mất kiểm soát", "tiêu xài"],
     "looking alarmed beside a chaotic overflowing glass container on an office desk where cash, coins, and receipts are spilling messily over the edges onto the floor",
     "tense moody workspace with red ambient warning light casting dramatic shadows"),
    (["phân luồng dòng tiền", "tách biệt"],
     "using a glowing golden stylus on a transparent glass whiteboard to draw a clean bifurcation diagram splitting a single stream of golden light into two clear separate neon flow paths",
     "high-tech minimalist creative studio with sleek neon accents"),
    (["chi tiêu sinh hoạt", "hàng ngày"],
     "picking up a sleek leather everyday wallet from a beautiful warm oak kitchen counter beside a steaming morning coffee mug and house keys",
     "warm golden morning sunlight flooding through contemporary kitchen windows"),
    (["thoải mái", "không tội lỗi"],
     "walking happily down a charming sunlit European cobblestone street carrying a minimalist boutique shopping bag, carefree broad smile",
     "golden hour sunset bathing historic architectural facades in warm amber hues"),
    (["tài khoản vô hình", "chiếc hộp thứ hai"],
     "pointing proudly to an intangible semi-transparent glowing crystalline safe floating in mid-air with emerald green digital numbers",
     "futuristic ultra-clean dark architectural sanctuary with emerald ambient accents"),
    (["tự động trích tiền", "đầu tư", "tích lũy"],
     "watching with satisfaction and crossed arms as a sophisticated automated mechanism with glowing brass tubes smoothly transfers shimmering gold coins into an expanding stack of polished ingots",
     "automated brass vault interior with warm golden lighting"),
    (["tự động hóa", "dòng tiền đã được"],
     "hands in windbreaker pockets, smiling peacefully and confident on a dark stone pier beside a rustic weathered lighthouse casting a powerful golden volumetric light beam into the stormy night sky",
     "stormy ocean pier at night with warm glowing lantern light on wet cobblestones"),
    (["không còn phải dùng đến ý chí", "cám dỗ"],
     "with a victorious, serene, and confident smile, standing tall atop a coastal cliff as dark storm clouds part to reveal a magnificent golden sunrise illuminating the calm ocean",
     "epic coastal cliff summit bathed in warm golden dawn rim light")
]

def clean_spoken_text(text: str) -> str:
    """Strips bracketed emotion tags like [thở dài], [cười] for clean processing."""
    return re.sub(r"\[.*?\]", "", text).strip()

def select_outfit_and_mood(text: str, index: int = 1) -> Tuple[int, Dict[str, Any]]:
    """Analyzes spoken text and selects matching outfit and mood."""
    clean_text = clean_spoken_text(text).lower()
    
    best_id = None
    max_score = 0
    
    for oid, data in WARDROBE_COLLECTION.items():
        score = sum(1 for kw in data["keywords"] if kw in clean_text)
        if score > max_score:
            max_score = score
            best_id = oid
            
    if best_id is None:
        fallbacks = [1, 6, 3, 2, 9]
        best_id = fallbacks[(index - 1) % len(fallbacks)]
        
    return best_id, WARDROBE_COLLECTION[best_id]

def get_scene_visual_concept(text: str, scene_id: int) -> Tuple[str, str]:
    """Finds semantic English visual action and setting without any Vietnamese text."""
    clean = clean_spoken_text(text).lower()
    
    for keywords, action, setting in CONCEPT_VISUAL_MAP:
        if any(kw in clean for kw in keywords):
            return action, setting
            
    # Default visual action based on scene id if no keyword matched
    default_actions = [
        ("standing in quiet reflection, observing glowing conceptual symbols with focused contemplation", "moody architectural space with dramatic volumetric lighting"),
        ("initiating decisive action with focused posture, gesturing toward illuminated conceptual pathways", "sleek minimalist interior with atmospheric depth of field"),
        ("walking forward with serene confidence toward a warm golden horizon", "cinematic open architectural vista at golden hour")
    ]
    return default_actions[(scene_id - 1) % len(default_actions)]

def build_single_scene_prompt(
    text: str,
    outfit_id: int,
    scene_id: int = 1
) -> str:
    """
    Generates standard 16:9 single image cinematic prompt with @stickman tag.
    CRITICAL: Contains ZERO Vietnamese text, quotes, or speech strings to prevent AI text leakage.
    """
    outfit = WARDROBE_COLLECTION.get(outfit_id, WARDROBE_COLLECTION[1])
    action, setting = get_scene_visual_concept(text, scene_id)
    
    prompt = (
        f"@stickman wearing his {outfit['description']}, {action}. "
        f"Set in {setting}. 16:9 landscape, cinematic depth of field, chiaroscuro lighting, "
        f"clean cinematic render, no watermarks, no logos, no text, no speech bubbles, no subtitles."
    )
    return prompt

def build_storyboard_motion_prompt(
    text: str,
    outfit_id: int,
    target_duration: int = 6,
    scene_id: int = 1
) -> str:
    """
    Generates a 4-panel storyboard motion grid prompt (2x2)
    describing continuous visual motion across 4 phases.
    CRITICAL: Contains ZERO Vietnamese quotes or text strings to prevent AI text leakage.
    """
    outfit = WARDROBE_COLLECTION.get(outfit_id, WARDROBE_COLLECTION[1])
    action, setting = get_scene_visual_concept(text, scene_id)
    
    prompt = (
        f"A professional 4-panel storyboard motion sequence grid (2x2 layout, 4 sequential frames) "
        f"showing continuous visual cinematic movement for @stickman wearing his {outfit['description']} "
        f"illustrating a {target_duration}-second cinematic progression: {action}. "
        f"Set in {setting}. "
        f"Panel 1 (Top-Left): Establishing wide shot, initial atmospheric buildup. "
        f"Panel 2 (Top-Right): Slow camera push-in as @stickman initiates decisive physical action. "
        f"Panel 3 (Bottom-Left): Dynamic climactic motion with striking visual lighting transformation. "
        f"Panel 4 (Bottom-Right): Serene cinematic conclusion with lingering visual resonance. "
        f"Consistent 2D minimalist character with white round head and bold ink outlines set against "
        f"photorealistic 3D environment, cinematic lighting, 16:9 aspect ratio. "
        f"CRITICAL REQUIREMENTS: Expressive visual motion, character may have natural mouth gestures and speaking expressions with no audible dialogue, silent vocal track (subtle ambient sound effects or SFX acceptable), no background music, no musical soundtrack, no watermarks, no logos, no text overlays, no subtitles."
    )
    return prompt

def build_aiv_video_prompt(
    text: str,
    outfit_id: int,
    target_duration: int = 6,
    scene_id: int = 1
) -> str:
    """
    Generates a video generation prompt for the AI Video tab (Veo / Omni Flash),
    referencing the 4-panel storyboard image grid.
    Explicitly instructs the AI that the 4 panels are motion reference guides only,
    and forces a SINGLE full-screen cinematic camera shot with NO split-screen or grid.
    Single contiguous paragraph, no internal linebreaks.
    """
    outfit = WARDROBE_COLLECTION.get(outfit_id, WARDROBE_COLLECTION[1])
    action, setting = get_scene_visual_concept(text, scene_id)
    
    prompt = (
        f"Single full-screen continuous cinematic camera shot (NO split-screen, NO 4-panel grid, NO collage, NO frame borders). "
        f"The 4 panels in the reference image are strictly a conceptual storyboard keyframe guide illustrating motion progression across time. "
        f"Synthesize the action into ONE seamless, full-frame {target_duration}-second camera sequence: "
        f"begin with the initial scene setup from Panel 1, smoothly push in as @stickman wearing his {outfit['description']} initiates the physical motion from Panel 2, "
        f"dynamically transition through the climactic action from Panel 3: {action}, "
        f"and fluidly resolve into the final posture from Panel 4. "
        f"Set in {setting}. Photorealistic 3D environment, cinematic depth of field, chiaroscuro lighting, consistent 2D minimalist character with white round head and bold ink outlines, single unified 16:9 viewport. "
        f"CRITICAL REQUIREMENTS: Single camera viewport only, full-screen frame, absolutely no split-screen, no 2x2 grid layout, no multiple panels, no collage, no borders, no sub-frames, expressive visual motion, character may have natural mouth gestures and speaking expressions with no audible dialogue, silent vocal track (subtle ambient sound effects or SFX acceptable), no background music, no musical soundtrack, no watermarks, no logos, no text overlays, no subtitles."
    )
    return prompt
