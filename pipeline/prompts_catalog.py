"""
Master Cinematic Shot List & Prompts Catalog for Video 01: 'Thói Quen Quản Lý Dòng Tiền & Tự Động Hóa'
Channel: Thói Quen Thịnh Vượng (@thoi-quen-thinh-vuong)

Rules enforced:
1. 100% Unique Visuals: Zero repeated templates (no duplicate brains, cards in ice, or generic cities).
2. Proper Cinematic Framing: Wide establishing environments, expansive 3D isometric blueprints,
   medium shots with environmental storytelling—NO isolated macro close-ups unless explicitly dramatic.
3. Decoupled Character System:
   - Hero scenes (~13-15%): Features @stickman with exact matching outfit and meaningful pose.
   - Concept B-Roll (~85-87%): Pure concept/metaphor/infographic with ZERO stickman.
4. First 5 scenes (AIV slots):
   - prompts_img_list: 4-panel storyboard motion sequence grid (2x2).
   - prompt_aiv_list: Single full-screen continuous camera sequence (no split-screen, no dialogue audio, no BGM).
5. Scenes 6 to 94: Single, complete 16:9 cinematic image prompts.
"""

from typing import Dict, Any

SCENE_PROMPTS_DATA: Dict[int, Dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # ACT I: HOOK & PARADOX OF WILLPOWER (Scenes 1 - 22)
    # -------------------------------------------------------------------------
    1: {
        "scene_type": "hero",
        "outfit_id": 1,
        "is_video_slot": True,
        "fixed_duration": 6,
        "framing": "wide atmospheric shot",
        "img_prompt": (
            "A professional 4-panel storyboard motion sequence grid (2x2 layout, 4 sequential frames) "
            "showing continuous cinematic movement for @stickman wearing his dark tailored trench coat and burgundy turtleneck, "
            "illustrating a 6-second philosophical inquiry. "
            "Set in a vast, moody brutalist concrete plaza at twilight with towering pillars and gentle rain reflections. "
            "Panel 1 (Top-Left): Establishing wide shot of @stickman standing under a warm lamppost in quiet introspection. "
            "Panel 2 (Top-Right): Slow camera push-in as @stickman gestures with an open hand, engaging with a profound dilemma. "
            "Panel 3 (Bottom-Left): Low angle shot highlighting contemplative facial expression as rain mist drifts past. "
            "Panel 4 (Bottom-Right): Camera settles as @stickman gazes directly into the lens with deep questioning resolve. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, chiaroscuro lighting, silent vocal track with natural mouth gestures, no dialogue audio, "
            "no background music, no watermarks, no text overlays, no subtitles."
        ),
        "aiv_prompt": (
            "Single full-screen continuous cinematic camera shot (NO split-screen, NO 4-panel grid, NO collage, NO frame borders). "
            "The 4 panels in the reference image are strictly a conceptual keyframe guide illustrating motion progression. "
            "Synthesize into ONE seamless 6-second sequence: begin with the establishing wide shot in Panel 1 of @stickman in his dark tailored trench coat, "
            "smoothly push in as he gestures thoughtfully with an open hand from Panel 2, transit through the low-angle contemplative lighting in Panel 3, "
            "and settle into a steady gaze toward the camera from Panel 4. "
            "Vast brutalist concrete plaza at dusk, wet pavement reflections, volumetric fog, photorealistic 3D environment, "
            "clean 2D minimalist character, single 16:9 viewport. "
            "CRITICAL: Single camera viewport only, absolutely no split-screen, natural lip gestures, silent vocal track, no dialogue audio, no BGM, no watermarks."
        )
    },

    2: {
        "scene_type": "hero",
        "outfit_id": 4,
        "is_video_slot": True,
        "fixed_duration": 10,
        "framing": "medium-wide environmental shot",
        "img_prompt": (
            "A professional 4-panel storyboard motion sequence grid (2x2 layout, 4 sequential frames) "
            "showing continuous cinematic movement for @stickman wearing his overworked wrinkled white dress shirt with loosened tie, "
            "illustrating a 10-second progression of month-end financial shock. "
            "Set in a high-rise office cubicle late at night, city skyline through rainy windows, dim fluorescent desk lamp. "
            "Panel 1 (Top-Left): Wide view of the darkened office floor with @stickman sitting at his cluttered desk surrounded by documents. "
            "Panel 2 (Top-Right): Camera pushes in as @stickman unlocks his smartphone, face illuminated by cold blue screen light. "
            "Panel 3 (Bottom-Left): Reaction shot showing sudden emotional tightness in chest, shoulders slumping as banking balance is viewed. "
            "Panel 4 (Bottom-Right): @stickman slowly leans back, clenching his hand in determined resolve to cut all spending next month. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, cinematic lighting, silent vocal track with natural expressions, no dialogue audio, "
            "no background music, no watermarks, no text overlays, no subtitles."
        ),
        "aiv_prompt": (
            "Single full-screen continuous cinematic camera shot (NO split-screen, NO 4-panel grid, NO collage, NO frame borders). "
            "Synthesize the 4 reference panels into ONE continuous 10-second camera sequence: "
            "begin with the wide view of the darkened late-night office floor in Panel 1, smoothly push in on @stickman wearing his overworked wrinkled dress shirt in Panel 2, "
            "capture the genuine subtle slump of disappointment and chest-tightness upon checking his phone in Panel 3, "
            "and smoothly resolve as he makes a quiet determined vow to change in Panel 4. "
            "Photorealistic 3D corporate office, rainy window backdrop, single unified 16:9 viewport. "
            "CRITICAL: Single camera viewport only, absolutely no split-screen, natural mouth gestures, silent vocal track, no dialogue audio, no BGM, no watermarks."
        )
    },

    3: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "is_video_slot": True,
        "fixed_duration": 6,
        "framing": "wide cinematic still life",
        "img_prompt": (
            "A professional 4-panel storyboard motion sequence grid (2x2 layout, 4 sequential frames) "
            "showing continuous cinematic mechanical and physical movement of strict financial austerity. "
            "Set in an austere dark wooden study with deep chiaroscuro side lighting from a tall window. "
            "Panel 1 (Top-Left): Wide establishing view of a dark oak desk with an open leather expense journal, vintage fountain pen, and simple ceramic cup. "
            "Panel 2 (Top-Right): Slow camera glide as the brass fountain pen automatically draws crisp lines crossing out discretionary budget items. "
            "Panel 3 (Bottom-Left): Ink glistens as an ornate vintage brass paperweight is placed firmly onto the ledger page. "
            "Panel 4 (Bottom-Right): Camera settles into a serene wide perspective of absolute discipline, cold coffee cup sitting untouched. "
            "Photorealistic 3D render, volumetric cinematic lighting, 16:9 aspect ratio, NO human characters, NO stickman. "
            "CRITICAL: Pure concept B-roll, subtle environmental SFX acceptable, no audible vocal track, no background music, no watermarks, no text overlays."
        ),
        "aiv_prompt": (
            "Single full-screen continuous cinematic camera shot (NO split-screen, NO 4-panel grid, NO collage, NO frame borders). "
            "Synthesize into ONE seamless 6-second camera sequence: "
            "begin with the wide establishing view of the oak desk in Panel 1, smoothly track closer as the fountain pen draws firm deliberate lines crossing out entries in Panel 2, "
            "show the paperweight settling onto the page in Panel 3, and smoothly pull back to a disciplined wide tableau in Panel 4. "
            "Dark oak study, dramatic window light, dust motes in volumetric rays, photorealistic 3D render, single 16:9 viewport. "
            "CRITICAL: Single camera viewport only, absolutely no split-screen, no human figures, silent vocal track, no BGM, no watermarks."
        )
    },

    4: {
        "scene_type": "environment",
        "outfit_id": 0,
        "is_video_slot": True,
        "fixed_duration": 6,
        "framing": "cinematic wide vista",
        "img_prompt": (
            "A professional 4-panel storyboard motion sequence grid (2x2 layout, 4 sequential frames) "
            "showing continuous cinematic atmospheric transition representing the turning point 'What happens next?'. "
            "Set in a vast panoramic view of a modern metropolis transition from twilight into deep night. "
            "Panel 1 (Top-Left): Wide view of city skyscrapers at twilight with cool slate-blue atmospheric haze. "
            "Panel 2 (Top-Right): Slow camera forward track as city streetlights and amber commercial signs begin blinking alive. "
            "Panel 3 (Bottom-Left): Vibrant streams of car headlights flowing through elevated highway overpasses like pulsing veins. "
            "Panel 4 (Bottom-Right): Camera rises to reveal the immense scale of the urban labyrinth under an ominous gathering cloud cover. "
            "Photorealistic 3D render, cinematic depth of field, volumetric atmosphere, 16:9 aspect ratio, NO human characters, NO stickman. "
            "CRITICAL: Pure concept B-roll, subtle urban ambient rumble, no audible voice, no background music, no watermarks, no text overlays."
        ),
        "aiv_prompt": (
            "Single full-screen continuous cinematic camera shot (NO split-screen, NO 4-panel grid, NO collage, NO frame borders). "
            "Synthesize into ONE seamless 6-second sequence: "
            "begin with the wide twilight city overview in Panel 1, smoothly push forward as glowing neon lights and streetlamps ignite in Panel 2, "
            "sweep over the pulsing highway traffic in Panel 3, and tilt up into the dramatic urban night sky in Panel 4. "
            "Expansive modern metropolis, cinematic lighting, photorealistic 3D render, single 16:9 viewport. "
            "CRITICAL: Single camera viewport only, absolutely no split-screen, no characters, silent vocal track, no BGM, no watermarks."
        )
    },

    5: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "is_video_slot": True,
        "fixed_duration": 10,
        "framing": "wide dynamic metaphor",
        "img_prompt": (
            "A professional 4-panel storyboard motion sequence grid (2x2 layout, 4 sequential frames) "
            "showing continuous cinematic movement illustrating impulsive dopamine spending and evaporating wealth. "
            "Set in an expansive high-end commercial lounge with dark polished marble floor and neon ambient glow. "
            "Panel 1 (Top-Left): Establishing wide shot of a sleek matte black payment terminal beside luxury shopping boxes and gourmet dining dishes. "
            "Panel 2 (Top-Right): Terminal screen flashes a bright emerald 'PAYMENT SUCCESSFUL' shockwave of luminous green energy. "
            "Panel 3 (Bottom-Left): A stack of crisp golden banknotes rapidly dissolves into shimmering golden smoke and glowing embers. "
            "Panel 4 (Bottom-Right): The golden smoke swirls upward and dissipates completely into cold dark air, leaving the marble counter barren. "
            "Photorealistic 3D render, dramatic lighting, 16:9 aspect ratio, NO human figures, NO stickman. "
            "CRITICAL: Pure concept B-roll, subtle whoosh SFX acceptable, no audible vocal track, no background music, no watermarks, no text overlays."
        ),
        "aiv_prompt": (
            "Single full-screen continuous cinematic camera shot (NO split-screen, NO 4-panel grid, NO collage, NO frame borders). "
            "Synthesize into ONE seamless 10-second camera sequence: "
            "begin with the wide establishing view of the luxury retail counter in Panel 1, push in as the payment terminal emits an emerald confirmation pulse in Panel 2, "
            "dynamically track the golden currency banknotes disintegrating into golden vapor in Panel 3, and smoothly pull back as the smoke dissolves into thin air in Panel 4. "
            "Polished dark marble, volumetric cinematic lighting, photorealistic 3D render, single 16:9 viewport. "
            "CRITICAL: Single camera viewport only, absolutely no split-screen, no characters, silent vocal track, no BGM, no watermarks."
        )
    },

    # --- SCENES 6 TO 94 ARE ALL FULL 16:9 SINGLE IMAGES ---
    6: {
        "scene_type": "hero",
        "outfit_id": 10,
        "framing": "medium-wide shot",
        "img_prompt": (
            "@stickman wrapped comfortably in a warm folded orange knit blanket, sitting on the floor of a minimalist room "
            "with knees pulled close, looking toward the floor with a vulnerable, reflective expression of self-doubt. "
            "Set in a quiet modern apartment at twilight, soft rain trickling down the floor-to-ceiling glass window, "
            "warm ambient floor lamp casting gentle shadows. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, cinematic depth of field, chiaroscuro lighting, emotional storytelling, "
            "clean render, no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
        )
    },

    7: {
        "scene_type": "hero",
        "outfit_id": 1,
        "framing": "medium shot",
        "img_prompt": (
            "@stickman wearing his dark tailored trench coat and burgundy turtleneck, turning toward the viewer with a calm, "
            "enlightened expression, holding up one hand in an open gesture of scientific revelation. "
            "Set in a grand, sun-drenched brutalist architectural gallery with soaring skylights casting long diagonal sunbeams. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, cinematic depth of field, warm golden hour illumination, clean render, "
            "no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
        )
    },

    8: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide surreal contrast",
        "img_prompt": (
            "A breathtaking wide visual contrast of human evolution and finance: An expansive ancient stone cave wall carved with "
            "prehistoric hunting petroglyphs and charcoal drawings, seamlessly overlapping into a translucent futuristic glass panel "
            "displaying modern financial charts and balance sheets. "
            "Warm primitive firelight on the left blending into cool teal holographic light on the right across textured limestone. "
            "16:9 landscape aspect ratio, cinematic depth of field, volumetric atmospheric dust, photorealistic 3D render, "
            "ultra-clean aesthetic, no human figures, no characters, no stickman, no watermarks, no logos, no text overlays."
        )
    },

    9: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "epic wide landscape",
        "img_prompt": (
            "A powerful wide cinematic metaphor of forced willpower battling nature: A colossal ancient granite monolith "
            "standing immovable against a furious raging mountain river, with foaming white water crashing violently over black boulders. "
            "Dramatic storm clouds overhead with a single golden shaft of sunlight breaking through the tempest. "
            "16:9 landscape aspect ratio, epic cinematic scale, volumetric spray, chiaroscuro lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    10: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide high-tech environment",
        "img_prompt": (
            "An expansive wide shot of a state-of-the-art cognitive neuroscience research auditorium: In the center of a darkened amphitheater, "
            "a large floating holographic architectural model reveals the human brain's dual decision pathways in glowing amber and cyan. "
            "Rows of sleek curved wooden desks with illuminated research terminals stretch into the soft background blur. "
            "16:9 landscape aspect ratio, cinematic depth of field, volumetric lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    11: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide isometric 3D blueprint",
        "img_prompt": (
            "A magnificent wide isometric 3D architectural blueprint of an automated financial ecosystem: "
            "An incoming stream of vibrant green energy enters a central processing hub and cleanly divides into 5 distinct illuminated conduits, "
            "routing smoothly toward automated vaults, living reservoirs, and compounding vaults on a dark polished granite foundation. "
            "16:9 landscape aspect ratio, pristine architectural rendering, glowing data paths, volumetric amber lighting, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    12: {
        "scene_type": "hero",
        "outfit_id": 3,
        "framing": "medium-wide studio shot",
        "img_prompt": (
            "@stickman wearing his modern dark blazer and white crewneck t-shirt, standing with confident posture in a contemporary creative studio, "
            "warmly gesturing toward the viewer as a host welcoming the audience. "
            "Set in a bright minimalist architectural loft with exposed brick, warm timber beams, lush potted fiddle-leaf figs, "
            "and soft morning sunlight streaming through massive industrial warehouse windows. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, cinematic depth of field, warm inviting lighting, clean render, "
            "no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
        )
    },

    13: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide clinical research bay",
        "img_prompt": (
            "A wide cinematic perspective inside an advanced neuroimaging medical suite: A massive modern fMRI scanner machine "
            "in a sterile, dimly lit dark-blue chamber, with multiple high-resolution medical displays showing real-time 3D cross-sections "
            "of the human cerebral cortex with active neural clusters illuminated in gold. "
            "16:9 landscape aspect ratio, cinematic depth of field, clinical chiaroscuro lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    14: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide historic academic hall",
        "img_prompt": (
            "A majestic wide shot of a world-renowned university economics archive: Soaring double-height wooden bookshelves "
            "filled with thousands of leather-bound volumes, brass rolling ladders, and a massive chalkboard covered in intricate behavioral "
            "decision-tree equations illuminated by green banker desk lamps. "
            "16:9 landscape aspect ratio, rich atmospheric dust motes, volumetric amber rays from high arched windows, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    15: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide atmospheric perspective",
        "img_prompt": (
            "An extraordinary wide visual metaphor of cognitive tunnel vision: A long, straight asphalt highway cutting through a dark dense forest at midnight. "
            "A single piercing cone of high-beam vehicle light illuminates the narrow road ahead, while the vast surrounding pine wilderness "
            "and starry sky remain swallowed in deep impenetrable mist and shadow. "
            "16:9 landscape aspect ratio, dramatic chiaroscuro contrast, volumetric headlights, atmospheric fog, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    16: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide environmental storytelling",
        "img_prompt": (
            "A wide cinematic shot of an exhausted late-night workroom at 3:45 AM: An open laptop glowing coldly on a cluttered oak desk, "
            "surrounded by crumpled balance spreadsheets, half-empty espresso cups, and a digital LED desk clock glowing '03:45' in amber, "
            "overlooking dark city high-rises outside the glass wall. "
            "16:9 landscape aspect ratio, deep night atmosphere, desaturated teal shadows, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    17: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide 3D anatomical visualization",
        "img_prompt": (
            "A wide dramatic visualization of primal fear circuitry: In a dark void, a stylized geometric 3D human head silhouette "
            "shows the almond-shaped amygdala pulsing with an intense glowing crimson red alarm beacon, casting harsh red light "
            "along neural pathways while the rational prefrontal cortex remains dormant in dark charcoal gray. "
            "16:9 landscape aspect ratio, cinematic lighting contrast, volumetric red haze, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    18: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide commercial environment",
        "img_prompt": (
            "A dazzling wide shot of an upscale commercial shopping boulevard at night: Gleaming marble walkways reflecting neon signs, "
            "grand display windows filled with luxury merchandise, glowing promotional sale banners, and intoxicating consumer temptation "
            "under a warm ambient architectural canopy. "
            "16:9 landscape aspect ratio, cinematic depth of field, vibrant neon reflections, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    19: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "panoramic primeval landscape",
        "img_prompt": (
            "An awe-inspiring panoramic wide vista of the prehistoric African savannah at twilight: An ancient glowing campfire burns "
            "on a rocky outcrop beneath a colossal ancient baobab tree, with an endless starry Milky Way arching across the purple night sky "
            "and vast shadowy plains stretching to the horizon. "
            "16:9 landscape aspect ratio, epic cinematic scope, flickering firelight, volumetric night mist, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    20: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "epic wide symbolic monument",
        "img_prompt": (
            "A monumental wide shot of an ancient colossal stone wall carved from deep volcanic bedrock, standing resolute and unyielding "
            "against crashing stormy waves on a rugged shoreline. Over thousands of years, the bedrock remains intact while ocean foam shatters harmlessly. "
            "16:9 landscape aspect ratio, epic natural scale, stormy teal atmosphere, volumetric spray, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    21: {
        "scene_type": "hero",
        "outfit_id": 3,
        "framing": "medium-wide architectural shot",
        "img_prompt": (
            "@stickman wearing his modern dark blazer and white crewneck t-shirt, standing beside a massive transparent glass drafting table "
            "in an open-concept architectural studio, looking forward with confident purpose while tapping a digital stylus on the glass. "
            "Set in a sunlit industrial loft with polished concrete floors and large factory grid windows overlooking a bustling modern city. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, cinematic depth of field, soft golden morning light, clean render, "
            "no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
        )
    },

    22: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "grand wide milestone corridor",
        "img_prompt": (
            "A breathtaking wide perspective of a grand minimalist architectural hall: Five massive illuminated monolithic pillars of warm white limestone "
            "stand in a perfect sequential row along a polished dark granite floor, each pillar glowing with an internal golden numeral from 1 to 5, "
            "leading toward a luminous horizon at the far end of the pavilion. "
            "16:9 landscape aspect ratio, monumental architectural perspective, volumetric lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    # -------------------------------------------------------------------------
    # ACT II: PRINCIPLE 1 — PAY YOURSELF FIRST & PARKISONS LAW (Scenes 23 - 35)
    # -------------------------------------------------------------------------
    23: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide typographic architectural installation",
        "img_prompt": (
            "A striking wide architectural installation of an inverted financial equation: Massive luminous brass and white letters "
            "mounted on a textured brutalist slate wall reading 'INCOME  -  AUTOMATED WEALTH  =  LIVING EXPENSES'. "
            "Warm directional spotlights cast sharp elegant drop shadows across the stone floor of the contemporary gallery. "
            "16:9 landscape aspect ratio, clean architectural typography, volumetric dust motes, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    24: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide boardroom scene",
        "img_prompt": (
            "A wide cinematic shot of a dark executive conference room: On a massive dark slate wall, the traditional doomed equation "
            "'INCOME - EXPENSES = SAVINGS' is written in faint, crumbling chalk, with a single focused overhead spotlight illuminating "
            "empty leather swivel chairs, a forgotten cup of cold coffee, and discarded financial calculators. "
            "16:9 landscape aspect ratio, moody chiaroscuro contrast, desaturated slate tones, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    25: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide domestic interior",
        "img_prompt": (
            "A wide atmospheric view of a contemporary apartment kitchen table at twilight: Neatly stacked envelopes of monthly rent, "
            "utility bills, grocery receipts, and restaurant receipts spread across the oak surface, beside an open empty leather wallet, "
            "illuminated by warm pendant lighting with a quiet city skyline outside the window. "
            "16:9 landscape aspect ratio, cinematic depth of field, domestic realism, warm tungsten ambiance, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    26: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide visual metaphor",
        "img_prompt": (
            "A dramatic wide visual metaphor of Parkinson's Law of expanding expenditure: A giant, flexible transparent glass flask "
            "resting on a dark pedestal, stretching and swelling outwards as dark indigo liquid continuously expands to fill every cubic centimeter "
            "of available volume, threatening to spill over the brim under atmospheric studio lighting. "
            "16:9 landscape aspect ratio, cinematic depth of field, water surface reflections, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    27: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide cozy studio apartment",
        "img_prompt": (
            "A wide establishing shot of a modest, tidy studio apartment representing a basic 10-million income lifestyle: "
            "Simple clean wooden furniture, a small neat bookshelf, basic groceries on a compact kitchen counter, and soft morning sunlight "
            "filtering through sheer white curtains onto warm parquet flooring. "
            "16:9 landscape aspect ratio, natural golden hour lighting, peaceful domestic simplicity, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    28: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide luxury penthouse view",
        "img_prompt": (
            "A wide establishing shot of a luxury high-rise penthouse representing lifestyle inflation: Designer Italian sofa, "
            "expensive curved OLED television, high-end espresso machine, premium gadgets on marble tables, and sweeping floor-to-ceiling "
            "city skyline views, yet lingering under a cool, desaturated twilight ambiance of underlying financial strain. "
            "16:9 landscape aspect ratio, cinematic luxury interior, moody evening reflections, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    29: {
        "scene_type": "hero",
        "outfit_id": 2,
        "framing": "medium-wide architectural shot",
        "img_prompt": (
            "@stickman wearing his sharp black business suit with tie, carrying a leather portfolio under one arm, standing firmly "
            "before the towering bronze vault doors of an imposing financial institution, pointing forward with unwavering clarity. "
            "Set in a majestic neoclassical banking hall with grand fluted marble columns and volumetric shafts of golden sunlight. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, cinematic depth of field, grand scale, authoritative posture, clean render, "
            "no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
        )
    },

    30: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide neuro-imaging auditorium",
        "img_prompt": (
            "A wide shot of an advanced cognitive neuroscience lab with an open medical fMRI scanner in the center: "
            "Giant wall-mounted monitors display vivid neural imaging graphs comparing brain activity when thinking of the current self "
            "versus thinking of the self 20 years into the future, rendered in brilliant amber and cyan volumetric data. "
            "16:9 landscape aspect ratio, clinical scientific lighting, high-tech dark environment, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    31: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide cinematic street crosswalk",
        "img_prompt": (
            "A poetic wide cinematic shot of a rainy downtown crosswalk at twilight: A lone silhouetted figure stands stationary "
            "under an umbrella in the center of the crosswalk, while dozens of ghostly blurred pedestrians stream past in rapid motion, "
            "visualizing the psychological feeling of seeing one's future self as an unknown stranger in the crowd. "
            "16:9 landscape aspect ratio, cinematic motion blur, wet asphalt reflections, moody neon palette, photorealistic 3D render, "
            "no distinct human faces, no characters, no stickman, no watermarks, no logos, no text overlays."
        )
    },

    32: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide surreal architectural space",
        "img_prompt": (
            "A profound wide surreal architectural composition: A vast empty minimalist hall of dark polished granite. At the near end, "
            "a glowing crystal pedestal holds a gleaming golden coin; at the far distant end across a chasm of soft misty fog, an identical pedestal "
            "awaits, visualizing the emotional disconnect between present impulse and future reward. "
            "16:9 landscape aspect ratio, cinematic chiaroscuro, volumetric haze, atmospheric depth, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    33: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide modern workspace",
        "img_prompt": (
            "A wide cinematic shot of a clean modern Scandinavian desk: A sleek tablet resting on an oak stand displays a banking app interface "
            "with a prominent glowing emerald toggle switch labeled 'Automated Recurring Transfer: ACTIVE', beside an architect's desk lamp "
            "and a small succulent plant, overlooking morning daylight. "
            "16:9 landscape aspect ratio, warm natural lighting, ultra-clean UI aesthetics, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    34: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide 3D isometric mechanism",
        "img_prompt": (
            "A sleek wide isometric 3D visualization of automated salary allocation: On the 5th of the month, a primary golden digital stream "
            "enters a high-tech splitter node; exactly 20% diverts cleanly into an impenetrable subterranean crystal vault with glowing locks, "
            "while 80% flows smoothly into an everyday expenditure reservoir. "
            "16:9 landscape aspect ratio, precision isometric diagram, volumetric lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    35: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide tranquil dining interior",
        "img_prompt": (
            "A wide establishing shot of a sun-filled minimalist dining room representing content living on an 80% budget: "
            "A rustic wooden dining table set with fresh wholesome home-cooked breakfast, steaming tea, and open balcony doors "
            "looking out to lush green trees under gentle morning sunlight, evoking complete peace and absence of lack. "
            "16:9 landscape aspect ratio, serene golden hour illumination, organic architectural textures, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    }
,
    # -------------------------------------------------------------------------
    # ACT III: PRINCIPLE 2 — 48-HOUR PAUSE & FRICTION (Scenes 36 - 51)
    # -------------------------------------------------------------------------
    36: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide monumental architectural installation",
        "img_prompt": (
            "A monumental wide architectural installation representing psychological friction: An imposing brutalist stone gateway "
            "equipped with heavy interlocking brass gears and a massive 48-hour mechanical countdown dial glowing softly in amber, "
            "standing as a protective barrier in front of an open rushing pathway. "
            "16:9 landscape aspect ratio, cinematic chiaroscuro, volumetric dust rays, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    37: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide futuristic commercial landscape",
        "img_prompt": (
            "A dazzling wide shot of an ultra-modern digital shopping metropolis at night: Soaring architectural facades covered in "
            "flashing holographic retail advertisements, giant floating discount banners, and neon ambient light reflecting on wet plaza tiles, "
            "visualizing an all-encompassing landscape designed to capture consumer spending. "
            "16:9 landscape aspect ratio, vibrant cyberpunk-inspired lighting, cinematic depth of field, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    38: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "vast industrial logistics interior",
        "img_prompt": (
            "A vast wide perspective inside a colossal automated e-commerce fulfillment warehouse: Endless towering shelving units stretching "
            "into the far horizon, illuminated by cold linear LED beams, with thousands of automated robotic sorting pods moving packages "
            "at breakneck speed to eliminate all friction between consumer desire and delivery. "
            "16:9 landscape aspect ratio, monumental industrial scale, volumetric lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    39: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide digital interface matrix",
        "img_prompt": (
            "A wide cinematic perspective of multiple floating digital UI screens in a dark studio: Bright crimson urgent countdown timers "
            "reading '00:14:59 REMAINING', flashing 'ONLY 2 ITEMS LEFT IN STOCK' badges, and glowing green '1-Click Buy' buttons, "
            "visualizing the psychological architecture of digital urgency. "
            "16:9 landscape aspect ratio, high-contrast dark holographic interface, subtle glowing particle trails, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    40: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide cinematic storefront at midnight",
        "img_prompt": (
            "A wide cinematic shot of a luxury retail boutique display window at midnight: The glowing glass vitrine radiates warm golden "
            "and magenta light onto the dark, rain-soaked pavement outside, showcasing seductive designer goods under focused theatrical spotlights "
            "in an otherwise silent city street. "
            "16:9 landscape aspect ratio, rich chiaroscuro shadows, reflective wet asphalt, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    41: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide 3D neural circuit visualization",
        "img_prompt": (
            "A wide 3D infographic of a human decision matrix: An intricate transparent neural network floating in dark space. "
            "The emotional limbic reward center pulses with an overwhelming flood of radiant amber and magenta energy, "
            "while the rational prefrontal cortex pathways are dimmed by 50% into a faint, cool blue trace. "
            "16:9 landscape aspect ratio, cinematic medical visualization, volumetric glow, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    42: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide cinematic split composition",
        "img_prompt": (
            "A powerful wide cinematic composition visually contrasting the 3-second impulse tap with 3 months of labor: "
            "On the left, an elegant glowing digital payment button hovering under soft ambient light; on the right, an expansive industrial "
            "manufacturing workshop where mechanical tools and worktables stretch under harsh fluorescent lights, symbolizing months of hard toil. "
            "16:9 landscape aspect ratio, cinematic lighting contrast, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    43: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide gallery installation",
        "img_prompt": (
            "A wide serene perspective inside a minimalist architectural gallery: A solitary dark slate pedestal stands in the center of an empty hall, "
            "holding an elegant frosted glass display case illuminated by a single warm overhead spotlight, inscribed with a brass plaque reading '48-HOUR EVALUATION'. "
            "16:9 landscape aspect ratio, peaceful spatial balance, volumetric light rays, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    44: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide organized desktop workspace",
        "img_prompt": (
            "A wide cinematic shot of an organized designer workstation: A sleek digital tablet resting on a walnut easel displays a structured "
            "'48-Hour Wishlist' table with timestamp countdowns, item photos, and priority tags, alongside a cup of freshly brewed tea "
            "and an open sketchbook under gentle afternoon sun. "
            "16:9 landscape aspect ratio, natural golden hour ambiance, clean minimalist UI design, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    45: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide scientific presentation board",
        "img_prompt": (
            "A wide shot of a modern behavioral research laboratory: A large transparent glass smartboard displays an illuminated graph "
            "showing a sharp visual spike of dopamine arousal peaking within 24 hours, followed by a smooth exponential decay returning "
            "to a peaceful baseline after 48 hours, illuminated by soft laboratory ambient lighting. "
            "16:9 landscape aspect ratio, clinical scientific clarity, volumetric glow, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    46: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide peaceful morning balcony",
        "img_prompt": (
            "A wide tranquil view of an outdoor apartment terrace overlooking a calm sunrise over green trees: A small cafe table holds "
            "a steaming ceramic mug and a tablet displaying a shopping cart with the 'DELETE' button highlighted in soft emerald, "
            "evoking clarity, emotional liberation, and total absence of regret. "
            "16:9 landscape aspect ratio, serene morning sunlight, organic wood and stone textures, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    47: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide clean minimalist desk setup",
        "img_prompt": (
            "A wide shot of a minimalist workstation: A modern bezel-less smartphone resting on an oak charging stand displays an open "
            "settings screen showing 'Saved Payment Methods: Cleared / Zero Saved Cards', surrounded by a clean uncluttered wooden surface, "
            "a small brass ruler, and natural indoor greenery under soft window light. "
            "16:9 landscape aspect ratio, peaceful minimalist aesthetic, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    48: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide warm evening living room",
        "img_prompt": (
            "A wide establishing shot of a warm domestic living room at twilight: A wooden console table near the doorway holds a leather valet tray "
            "with keys and a closed wallet, while soft ambient light from a floor lamp illuminates herringbone parquet floors and comfortable armchairs, "
            "conveying the intentional physical distance that creates healthy reflection. "
            "16:9 landscape aspect ratio, rich warm tungsten illumination, cinematic depth of field, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    49: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide analytical home office",
        "img_prompt": (
            "A wide cinematic shot of a scholar desk: An open notebook displays a neat mathematical formula in fountain pen: "
            "'ITEM PRICE ÷ HOURLY REAL WAGE = LABOR HOURS', resting beside a brass calculator displaying '40.0 HOURS', "
            "with soft natural light illuminating the paper grain and a dark wooden study backdrop. "
            "16:9 landscape aspect ratio, intellectual atmosphere, chiaroscuro lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    50: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide corporate office floor",
        "img_prompt": (
            "A wide cinematic perspective across an expansive corporate open-plan office in late afternoon: Long rows of empty workstations "
            "and ergonomic chairs leading toward floor-to-ceiling glass windows overlooking a busy city, with warm golden rays slicing through "
            "venetian blinds, embodying the true value of 40 hours of dedicated human labor. "
            "16:9 landscape aspect ratio, cinematic architectural perspective, atmospheric dust motes, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    51: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide poetic natural landscape",
        "img_prompt": (
            "A poetic wide landscape of clarity and liberation: A fresh mountain breeze sweeps across an open stone terrace, "
            "blowing away brittle paper price tags and receipts into a vast pine forest valley below under crisp, radiant blue morning skies. "
            "16:9 landscape aspect ratio, epic natural depth of field, bright morning atmosphere, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    # -------------------------------------------------------------------------
    # ACT IV: PRINCIPLE 3 — MINIMUM OPERATING NUMBER & BUFFER (Scenes 52 - 64)
    # -------------------------------------------------------------------------
    52: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide architectural foundation",
        "img_prompt": (
            "A monumental wide shot of an unbreakable architectural foundation: Massive solid granite bedrock footings supporting "
            "a contemporary minimalist concrete villa above. The foundational rock is exposed, raw, and unshakeable, symbolizing absolute baseline security. "
            "16:9 landscape aspect ratio, brutalist architectural power, volumetric mist, chiaroscuro lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    53: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide moody shoreline",
        "img_prompt": (
            "A wide atmospheric vista representing financial ambiguity and vague fear: A vast, empty rocky coastline at dawn completely shrouded "
            "in dense, disorienting gray fog, where the boundary between sea and sky is invisible, evoking an aimless feeling of uncertainty. "
            "16:9 landscape aspect ratio, desaturated teal and slate palette, volumetric ocean mist, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    54: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide grand chess hall",
        "img_prompt": (
            "A wide surreal metaphor of strategic paralysis: In a vast, empty gothic library with marble checkered flooring, a massive stone chessboard "
            "sits frozen under cold shafts of moonlight, with carved crystal chess pieces suspended motionless mid-game in dusty air. "
            "16:9 landscape aspect ratio, cinematic chiaroscuro, volumetric moonbeams, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    55: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide sunlit drafting table",
        "img_prompt": (
            "A wide shot of an architect study: A large drafting table bathed in warm morning light holds an open grid notebook "
            "with precise handwritten categories and numbers totaled into a highlighted bold box reading 'MINIMUM OPERATING NUMBER', "
            "beside a brass compass, mechanical pencil, and clear crystal paperweight. "
            "16:9 landscape aspect ratio, warm natural wood textures, serene intellectual focus, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    56: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide 3D isometric capsule",
        "img_prompt": (
            "A wide sleek isometric 3D architectural diagram of a life-support capsule: A transparent geometric pavilion resting on dark slate, "
            "supported by 5 glowing structural corner pillars labeled Shelter, Food, Utilities, Healthcare, and Debt Obligations, "
            "pulsing with steady emerald equilibrium indicators. "
            "16:9 landscape aspect ratio, clean isometric rendering, volumetric lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    57: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide domestic sanctuary",
        "img_prompt": (
            "A wide establishing shot of a peaceful, well-ordered home interior: A clean Scandinavian kitchen with fresh local vegetables "
            "on the island, a neatly folded utility binder on the side table, and a glimpse of a small reliable vehicle parked in the driveway outside. "
            "16:9 landscape aspect ratio, natural daylight, warm organic textures, wholesome domestic dignity, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    58: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide high-contrast slate tabletop",
        "img_prompt": (
            "A wide cinematic composition dividing necessity from non-essential luxury: A long slate surface split down the middle by a crisp light line. "
            "On the left, under warm focused light, sit staple food, home keys, and essential medicine; on the right, in deep cool shadow, "
            "sit champagne glasses, luxury retail tags, and entertainment tickets, completely stripped away. "
            "16:9 landscape aspect ratio, striking chiaroscuro contrast, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    59: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide luminous library archive",
        "img_prompt": (
            "A wide shot of a modern private study: In the center of a dark wood desk, an illuminated parchment card displays '12,000,000 VND / MONTH' "
            "written in crisp, luminous gold lettering, radiating warm soft light that banishes all the surrounding darkness from the room. "
            "16:9 landscape aspect ratio, cinematic lighting transformation, volumetric warmth, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    60: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide epic bridge landscape",
        "img_prompt": (
            "An epic wide landscape of psychological breakthrough: The frightening wall of thick black mist rolls back completely, "
            "revealing a solid, well-lit stone bridge crossing safely over a shallow gorge toward a sunlit green meadow with clear signposts. "
            "16:9 landscape aspect ratio, epic cinematic transition, warm golden sunrise, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    61: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide subterranean treasury vault",
        "img_prompt": (
            "A wide shot inside a high-security modern private vault: Rows of transparent security lockboxes along dark granite walls, "
            "housing neat stacks of emergency reserves and gold bullion totaling 6 months of baseline operating funds, illuminated by calm emerald safety beacons. "
            "16:9 landscape aspect ratio, pristine architectural security, volumetric rays, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    62: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide crystalline safe installation",
        "img_prompt": (
            "A wide cinematic shot of a zero-risk capital sanctuary: A solid crystalline security container resting on an immovable black basalt pedestal, "
            "surrounded by a calm pool of clear still water in a serene modern atrium, completely isolated from outside financial market turbulence. "
            "16:9 landscape aspect ratio, tranquil architectural atmosphere, soft cyan rim lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    63: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "panoramic coastal cliff summit",
        "img_prompt": (
            "A breathtaking panoramic wide vista of absolute psychological peace: A solitary lighthouse standing on a high grassy headland "
            "overlooking an immense calm ocean bathed in warm golden afternoon sunlight, evoking unshakeable dignity and true peace of mind. "
            "16:9 landscape aspect ratio, majestic natural scale, warm golden hour atmosphere, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    64: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide executive glass pavilion",
        "img_prompt": (
            "A wide cinematic shot of a modern glass pavilion overlooking pine-covered mountains: A polished timber conference table holds "
            "a single clear leather binder with a 10-year growth plan, reflecting soft daylight from massive windows, conveying calm strategic mastery. "
            "16:9 landscape aspect ratio, serene architectural elegance, natural ambient lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    # -------------------------------------------------------------------------
    # ACT V: PRINCIPLE 4 — TWO BOXES SYSTEM (Scenes 65 - 76)
    # -------------------------------------------------------------------------
    65: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide 3D architectural dual pavilions",
        "img_prompt": (
            "A magnificent wide 3D architectural rendering of the Two-Box system: Two distinct floating crystalline structures side by side. "
            "On the left, an impenetrable locked vault of smoky crystal accumulating solid gold ingots; on the right, an open luminous glass pavilion "
            "with gentle water features representing 100% guilt-free lifestyle spending. "
            "16:9 landscape aspect ratio, futuristic minimalist architecture, volumetric lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    66: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide moody cafe interior",
        "img_prompt": (
            "A wide establishing shot of a charming European bistro at twilight: Polished brass fixtures, warm pendant lamps, and marble tables "
            "with delicious dishes and coffee, while in the corner an empty table holds an unfolded receipt under dim cool light, "
            "symbolizing the toxic guilt of unstructured spending. "
            "16:9 landscape aspect ratio, rich atmospheric depth, warm and cool lighting contrast, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    67: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide architectural stone crossroads",
        "img_prompt": (
            "A wide architectural perspective of an ancient stone courtyard: A clear channel of fresh water divides cleanly into two separate stone aqueducts, "
            "each flowing smoothly toward its own dedicated reservoir without any cross-contamination or conflict, ending the psychological guilt loop. "
            "16:9 landscape aspect ratio, classical stone masonry, volumetric sunlight, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    68: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide underground vault mechanism",
        "img_prompt": (
            "A wide perspective inside a high-tech subterranean reserve: Box 1 'The Invisible Accumulation Vault' sits heavily fortified "
            "behind reinforced titanium and tempered glass, receiving a steady automated 20% stream of digital wealth that silently accumulates "
            "in the darkness without human intervention. "
            "16:9 landscape aspect ratio, industrial precision rendering, cool teal and amber highlights, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    69: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide minimalist bedside interior",
        "img_prompt": (
            "A wide tranquil view of a modern bedroom at dawn: A wooden bedside table holds an alarm clock and a smartphone displaying a clean, "
            "distraction-free home screen with no banking or trading apps installed, while morning sun illuminates crisp white linens, "
            "conveying the blissful freedom of an out-of-sight secondary account. "
            "16:9 landscape aspect ratio, natural morning glow, peaceful domestic minimalism, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    70: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide panoramic compounding forest",
        "img_prompt": (
            "An expansive wide landscape symbolizing compounding wealth: A vast hillside terraced with thriving, ancient green oak trees "
            "growing silently and steadily under gentle golden rain and warm sunbeams, while roots anchor deeply into fertile soil. "
            "16:9 landscape aspect ratio, epic natural panorama, volumetric light rays, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    71: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide sun-drenched terrace lounge",
        "img_prompt": (
            "A wide inviting view of Box 2 'The Absolute Freedom Container': A bright sunroom opening to a lush garden terrace, "
            "with comfortable linen armchairs, a table holding books, art magazines, and fresh citrus fruits under radiant afternoon light. "
            "16:9 landscape aspect ratio, joyous lifestyle aesthetic, organic warm materials, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    72: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide luxury rooftop dining venue",
        "img_prompt": (
            "A wide cinematic establishing shot of a high-end rooftop restaurant at night: Elegantly set tables with sparkling glassware, "
            "gourmet culinary dishes, and glowing candles, overlooking panoramic sparkling city skyline lights, representing 100% guilt-free celebration. "
            "16:9 landscape aspect ratio, cinematic luxury ambiance, soft bokeh city lights, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    73: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide scenic running path at sunrise",
        "img_prompt": (
            "A wide dynamic perspective along a scenic coastal park running path at sunrise: Crisp fresh morning dew on grass, "
            "a pair of top-tier running shoes resting beside a clean sports bottle on a wooden bench, with golden morning light illuminating the misty track. "
            "16:9 landscape aspect ratio, energetic morning atmosphere, volumetric sun rays, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    74: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide historic town public library",
        "img_prompt": (
            "A wide establishing shot of a classic American rural stone library at golden hour: Stately classical limestone facade with grand arched windows, "
            "surrounded by autumn maple trees with amber leaves, evoking the humble dignity and generational impact of quiet accumulators. "
            "16:9 landscape aspect ratio, nostalgic golden hour illumination, cinematic architectural realism, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    75: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide sunlit historic memorial hall",
        "img_prompt": (
            "A wide cinematic view inside a grand sunlit library wing: Tall mahogany bookcases, brass reading lamps, and an elegant memorial bronze plaque "
            "inscribed with an eight-million-dollar philanthropic endowment, bathed in majestic shafts of warm dust-moted sunlight. "
            "16:9 landscape aspect ratio, timeless architectural beauty, volumetric light rays, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    76: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "panoramic centennial oak meadow",
        "img_prompt": (
            "A breathtaking panoramic wide shot of a magnificent 100-year-old solitary oak tree standing in the center of a rolling golden meadow, "
            "its massive sprawling canopy offering deep shade while gentle afternoon clouds drift across a peaceful blue sky, symbolizing steadfast wealth retention. "
            "16:9 landscape aspect ratio, epic scale, rich natural realism, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    # -------------------------------------------------------------------------
    # ACT VI: PRINCIPLE 5 — AUTONOMOUS CASH FLOW MACHINE & IF-THEN (Scenes 77 - 87)
    # -------------------------------------------------------------------------
    77: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide intricate clockwork automaton",
        "img_prompt": (
            "A magnificent wide shot of a precision mechanical horological clockwork automaton: Interlocking polished brass and steel gears, "
            "escapement mechanisms, and tempered glass conduit tracks operating in perfect silent synchronization under warm volumetric gallery spotlights. "
            "16:9 landscape aspect ratio, intricate mechanical complexity, cinematic depth of field, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    78: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide autonomous control hub",
        "img_prompt": (
            "A wide shot of a modern architectural smart-home operations room: Sleek dark wood cabinetry with embedded flush digital glass panels "
            "monitoring automated routines and energy flows in calm ambient green indicators, looking out onto a peaceful private bamboo garden. "
            "16:9 landscape aspect ratio, ultra-clean contemporary design, soft natural lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    79: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide 3D isometric reservoir system",
        "img_prompt": (
            "A wide 3D isometric diagram of Step 1 'Income Reservoir': A central illuminated crystalline basin receiving monthly revenue, "
            "governed by an automated 24-hour settling sluice gate that prevents any immediate reactive outflow, resting on polished slate. "
            "16:9 landscape aspect ratio, crisp isometric layout, volumetric water and light paths, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    80: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide 3D multi-channel aqueduct network",
        "img_prompt": (
            "A wide 3D isometric visualization of Step 2 '8:00 AM Automated Routing': From the central pool, two distinct glowing aqueducts branch off: "
            "A vibrant 20% stream flows into Bank 2 'Invisible Wealth Vault', while the exact Minimum Operating Number diverts into Bank 3 'Bill Payment Account'. "
            "16:9 landscape aspect ratio, precision isometric routing, glowing green and gold liquid data streams, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    81: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide cafe tabletop with lifestyle card",
        "img_prompt": (
            "A wide shot of a bright sunlit cafe table: A handsome full-grain leather wallet holding a single everyday payment debit card, "
            "beside a fresh espresso cup and morning journal, representing the guilt-free everyday spending remainder of the Two-Box system. "
            "16:9 landscape aspect ratio, warm natural lighting, organic textures, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    82: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide smart home living space",
        "img_prompt": (
            "A wide establishing shot of a serene living room: A wall-mounted smart display shows 'All Monthly Utilities Paid Automatically — Status: Zero Overdue', "
            "illuminating a tidy living room with warm wooden floors, soft linen sofa, and an open balcony with lush green plants. "
            "16:9 landscape aspect ratio, peaceful domestic security, natural daylight, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    83: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide behavioral logic laboratory",
        "img_prompt": (
            "A wide perspective inside a cognitive science laboratory: An elegant glass matrix displays the logic structure of 'IF [TRIGGER] -> THEN [ACTION]', "
            "where incoming sensory triggers automatically illuminate instant pre-programmed neural execution pathways in brilliant amber light. "
            "16:9 landscape aspect ratio, high-tech decision architecture, volumetric rays, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    84: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide mechanical scale installation",
        "img_prompt": (
            "A wide cinematic shot of Rule 1 'Windfall Splitting': A precision brass balance scale where an unexpected bonus cleanly splits: "
            "70% of golden coins automatically tip into a fortified subterranean vault, while 30% slide into a velvet pouch for celebratory spending. "
            "16:9 landscape aspect ratio, exquisite mechanical detail, warm directional studio lighting, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    85: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide city skyline apartment at dusk",
        "img_prompt": (
            "A wide establishing view of Rule 2 'Salary Increase Discipline': A modern city apartment maintaining its peaceful minimalist aesthetic, "
            "with simple tasteful furnishings and an open view of a sparkling downtown skyline, resisting lifestyle inflation despite rising prosperity. "
            "16:9 landscape aspect ratio, evening twilight reflections, cinematic contrast, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    86: {
        "scene_type": "infographic",
        "outfit_id": 0,
        "framing": "wide digital interface timer",
        "img_prompt": (
            "A wide cinematic shot of Rule 3 'Impulse Friction Trigger': A large translucent smart glass panel pausing an online shopping checkout screen, "
            "displaying a glowing frosted timer reading '48-Hour Reflection In Progress — 47:59:58', surrounded by a calm minimalist home office. "
            "16:9 landscape aspect ratio, modern glassmorphism aesthetics, soft ambient light, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    87: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "panoramic pristine mountain river",
        "img_prompt": (
            "A breathtaking panoramic wide vista of a pristine mountain river: Crystal-clear alpine water flowing smoothly and effortlessly "
            "through a lush green valley between ancient pines toward a grand placid mountain lake under a bright golden sunrise, "
            "symbolizing automated wealth flowing as naturally as a heartbeat. "
            "16:9 landscape aspect ratio, epic natural beauty, volumetric sunbeams, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    # -------------------------------------------------------------------------
    # ACT VII: SILENT WEALTH & INSPIRING OUTRO (Scenes 88 - 94)
    # -------------------------------------------------------------------------
    88: {
        "scene_type": "hero",
        "outfit_id": 1,
        "framing": "medium-wide panoramic overlook",
        "img_prompt": (
            "@stickman wearing his dark tailored trench coat and burgundy turtleneck, standing at a panoramic mountain viewpoint "
            "overlooking the twinkling lights of the metropolis below at blue hour, turning thoughtfully toward the camera with profound sincerity. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, cinematic depth of field, dramatic evening atmosphere, clean render, "
            "no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
        )
    },

    89: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide opulent banquet hall",
        "img_prompt": (
            "A wide cinematic shot of noisy, anxious ostentation: An over-decorated, gaudy luxury banquet hall with gold chandeliers, "
            "empty champagne flutes, discarded designer packaging, and a cold superficial emptiness echoing under harsh artificial lighting. "
            "16:9 landscape aspect ratio, cinematic satire, deep chiaroscuro shadows, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    90: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide sun-drenched sanctuary bedroom",
        "img_prompt": (
            "A wide establishing shot of 'Silent Wealth': A serene minimalist master bedroom with pure white linens, open French doors "
            "looking out into a sunlit private courtyard garden with blooming white jasmine, filled with peaceful morning breeze and zero debt anxiety. "
            "16:9 landscape aspect ratio, ethereal morning glow, peaceful organic textures, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    91: {
        "scene_type": "environment",
        "outfit_id": 0,
        "framing": "wide sunlit artisan atelier",
        "img_prompt": (
            "A wide view of sovereign life freedom: A bright creative studio workshop with tall arched windows, shelves of books, "
            "canvas easels, and drafting tools in harmonious natural order, conveying the liberty to work on meaningful passions without external compromise. "
            "16:9 landscape aspect ratio, warm natural illumination, inspiring artistic atmosphere, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    92: {
        "scene_type": "metaphor",
        "outfit_id": 0,
        "framing": "wide stone mountain trail at dawn",
        "img_prompt": (
            "A majestic wide landscape of steady consistent progress: A clean winding stone pathway gently ascending through ancient terraced "
            "gardens toward a sun-drenched mountain summit bathed in radiant morning light, embodying small daily habits leading to great heights. "
            "16:9 landscape aspect ratio, epic natural panorama, volumetric sun rays, photorealistic 3D render, "
            "no human figures, no characters, no stickman, no watermarks, no logos, no text overlays, no subtitles."
        )
    },

    93: {
        "scene_type": "hero",
        "outfit_id": 3,
        "framing": "medium-wide studio shot",
        "img_prompt": (
            "@stickman wearing his modern dark blazer and white crewneck t-shirt, sitting at a warm solid oak desk, holding up a single "
            "crisp index card inscribed with 'Start With One Small Action', looking directly into the camera with an encouraging, grounded smile. "
            "Set in a warm contemporary loft studio with soft lamp lighting and architectural models in the background. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, cinematic depth of field, warm inviting lighting, clean render, "
            "no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
        )
    },

    94: {
        "scene_type": "hero",
        "outfit_id": 1,
        "framing": "cinematic wide outro vista",
        "img_prompt": (
            "@stickman wearing his dark tailored trench coat, walking with steady confident stride along an expansive coastal stone pathway "
            "toward a majestic sunrise cresting over the ocean horizon, while the camera slowly pulls back into an epic wide cinematic vista. "
            "Consistent 2D minimalist character with white round head and bold ink outlines set against photorealistic 3D environment, "
            "16:9 landscape aspect ratio, epic cinematic scope, radiant golden sunrise, clean render, "
            "no watermarks, no logos, no text overlays, no speech bubbles, no subtitles."
        )
    }
}
