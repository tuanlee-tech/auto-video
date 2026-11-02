# Auto Video Studio: Guidelines & Rules for AI Agents

Tài liệu này là bộ quy tắc bắt buộc (Master Rules) dành cho tất cả các AI Agent làm việc trong không gian dự án `auto-video`. Mọi agent khi tham gia phát triển, viết kịch bản hoặc mở rộng pipeline đều phải tuân thủ nghiêm ngặt các nguyên tắc dưới đây.

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC: TỰ ĐỘNG PHỐI HỢP 20 SKILLS (XEM CHI TIẾT TẠI `AGENT.md`)**
> Toàn bộ 20 kỹ năng chuẩn đã được tích hợp tại `.agent/skills/`. Mọi Agent **BẮT BUỘC PHẢI CHỦ ĐỘNG** đọc và kết hợp các thư viện (Remotion, Motion AI, GSAP, Satori, Three.js, Rapier, Postprocessing, Howler, VieNeu-TTS...) theo Ma trận phối hợp 6 tầng trong file [`AGENT.md`](file:///e:/auto-video/AGENT.md). **TUYỆT ĐỐI KHÔNG ĐƯỢC CHỜ NGƯỜI DÙNG PHẢI NHẮC NHỞ MỚI DÙNG SKILL.**

---

## 1. Triết Lý Kiến Trúc: "Master Voice & Whisper Timeline"

Khác với các công cụ tạo video AI thông thường (sinh ảnh trước rồi ép thoại vào) hoặc ghép nối nhiều đoạn audio rời rạc gây đứt quãng nhịp thở, hệ thống hoạt động theo triết lý **Master Voice & Whisper Timeline**:

1. **Sinh Master Voice 1 Lần Duy Nhất**: Toàn bộ kịch bản được đọc liền mạch trong 1 lần duy nhất bằng **VieNeu-TTS v3 Turbo** (ưu tiên giọng `Hải Đăng` cho năng lượng tươi trẻ hoặc `Thiện Minh` cho phong cách tự sự), xuất ra file `master_narration.wav`. Nhịp điệu phát thanh giữ nguyên hơi thở tự nhiên, dồn dập, lôi cuốn mà không bị cắt vụn.
2. **Bóc tách Timeline Bằng Faster-Whisper**: Chạy `faster-whisper` (word_timestamps=True) trên file master audio để trích xuất mốc thời gian chính xác từng mili-giây (`start_ms`, `end_ms`) cho từng từ và phân rã thành ranh giới chính xác cho toàn bộ các phân cảnh (từ 50–200 scenes tùy độ dài kịch bản).
3. **Phân rã B-roll Theo Mốc Thời Lượng Thực Tế**: Sau khi Faster-Whisper hoàn tất, hệ thống mới tính toán chính xác thời lượng hiển thị từng giây cho từng phân cảnh, từ đó kết xuất danh sách B-roll và Storyboard video AI chuẩn xác để tạo visual trên Google Flow (0 credit). TUYỆT ĐỐI KHÔNG TẠO VISUAL KHI CHƯA CÓ WHISPER TIMELINE.

---

## 2. Quy Tắc Nhân Vật Nhất Quán & Tách Biệt B-Roll (Decouple Character from Scene)

Hệ thống tuân thủ nghiêm ngặt nguyên tắc **"Tách biệt Nhân vật khỏi Bối cảnh" (Decouple Character from Scene)** theo chuẩn Điện ảnh:
- **Tỷ lệ phân bổ**: **15% – 25% Hero Persona** (Nhân vật dẫn chuyện `@stickman`) và **75% – 85% Concept B-Roll thuần túy** (Vật thể, sơ đồ, phép ẩn dụ điện ảnh — **TUYỆT ĐỐI KHÔNG NHÉT STICKMAN**).
- **Nhịp thở phân cảnh (Cinematic Pacing)**: Mỗi phân cảnh kéo dài **12 – 18 giây** (tương đương 50 – 75 từ). Đối với video 17 – 20 phút, tổng số phân cảnh tối ưu chỉ từ **55 – 75 scenes**. **TUYỆT ĐỐI CẤM CẮT VỤN 3-5 GIÂY** làm gián đoạn cảm xúc và gây chóng mặt cho người xem.

### A. Phân Cảnh Hero Persona (Có thẻ `@stickman` — 15-25%):
Dùng cho cảnh Hook mở đầu, kết luận Outro, khoảnh khắc tự vấn hoặc chuyển giao cảm xúc cá nhân. Sử dụng ảnh tham chiếu Master trong **Character Library** định danh là `@stickman`.
* **Cú pháp Prompt**:
  ```text
  @stickman [TÊN BỘ TRANG PHỤC TƯƠNG ỨNG], [HÀNH ĐỘNG & BIỂU CẢM], [BỐI CẢNH 3D ĐIỆN ẢNH & ÁNH SÁNG], 16:9.
  ```
* **Bảng 10 Trang Phục Chuẩn**:
  1. `@stickman wearing his dark tailored trench coat and burgundy turtleneck...`: Dùng cho cảnh chiêm nghiệm triết học, suy nghĩ sâu sắc, đứng trước câu hỏi lớn.
  2. `@stickman in his sharp black business suit with tie, carrying a briefcase...`: Dùng cho cảnh kiếm tiền, đàm phán tài chính, đầu tư, thị trường chứng khoán.
  3. `@stickman in his modern dark blazer and white crewneck t-shirt...`: Dùng cho cảnh khởi nghiệp, làm việc sáng tạo, phân tích sơ đồ hệ thống.
  4. `@stickman wearing his overworked wrinkled white dress shirt with loosened tie...`: Dùng cho cảnh tăng ca kiệt sức, áp lực deadline, ngập trong nợ nần và hóa đơn.
  5. `@stickman in his navy hooded outdoor windbreaker jacket, backpack on shoulders...`: Dùng cho cảnh đối mặt giông bão, kiên trì theo đuổi mục tiêu (hải đăng, ngọn núi).
  6. `@stickman in his casual minimalist blue t-shirt and dark chinos...`: Dùng cho sinh hoạt hàng ngày, lối sống tối giản, mua sắm cơ bản.
  7. `@stickman wearing a cozy knitted cardigan and reading glasses, holding an open book...`: Dùng cho cảnh tiếp thu kiến thức, đọc sách, nghiên cứu.
  8. `@stickman wearing his black athletic gym sportswear and running hoodie...`: Dùng cho cảnh rèn luyện kỷ luật, thói quen thể thao, dậy sớm, Dopamine Detox.
  9. `@stickman in oversized warm brown knit sweater, holding a steaming coffee mug...`: Dùng cho cảnh bình yên tại nhà, thói quen sáng/tối, an tâm tài chính.
  10. `@stickman wrapped comfortably in a warm folded orange knit blanket...`: Dùng cho cảnh yếu đuối tâm lý, hoang mang, cần được chữa lành và đồng cảm.

### B. Phân Cảnh Concept B-Roll (KHÔNG CÓ STICKMAN — 75-85%):
Tập trung 100% vào việc **minh họa chân thực, sống động đúng thực thể/khái niệm/phép ẩn dụ** đang được nhắc tới trong lời thoại:
* **Infographic & Blueprint B-Roll**: Mô hình 3D não bộ trong suốt với các luồng xung thần kinh Dopamine phát sáng giữa hạch hạnh nhân và vỏ não; sơ đồ dòng tiền 2 chiếc hộp pha lê; màn hình ứng dụng ngân hàng giao diện tối giản với công tắc chuyển tiền tự động; biểu đồ baseline chi phí sinh hoạt.
* **Metaphorical B-Roll**: Con heo đất vỡ vụn dưới ánh đèn lạnh; đồng hồ cát bằng đồng cổ với dòng cát vàng tích lũy; thẻ tín dụng bị đóng băng trong khối đá pha lê (ma sát 48h); cỗ máy bánh răng cơ học tự động phân phối tiền vàng; ngọn lửa trại nguyên thủy trong hang đá; ngọn hải đăng sừng sững giữa đêm bão.
* **Cú pháp Prompt**:
  ```text
  [CHI TIẾT MÔ HÌNH VẬT THỂ / SƠ ĐỒ 3D / PHÉP ẨN DỤ ĐIỆN ẢNH], Set in [BỐI CẢNH 3D ĐIỆN ẢNH & ÁNH SÁNG], 16:9 landscape, cinematic depth of field, chiaroscuro lighting, volumetric atmosphere, photorealistic 3D render, no human figures, no characters, no watermarks, no logos, no text overlays, no speech bubbles.
  ```

---

## 3. Phong Cách Hình Ảnh "Cinematic Hybrid"

* **Nhân vật**: Hoạt hình 2D tối giản (Cel-shaded), đầu tròn hình trứng màu trắng trơn, nét viền đen dày dặn (`bold clean black ink outlines`), biểu cảm mắt và miệng linh hoạt, **tuyệt đối không có tóc và không vẽ mũi**.
* **Không gian (Background)**: Không gian 3D điện ảnh photorealistic có chiều sâu (Brutalist concrete architecture, modern glass office at night, rainy city streets, stormy ocean lighthouse).
* **Màu sắc & Ánh sáng**:
  - Giai đoạn Vấn đề / Áp lực: Gam màu lạnh u tối (Desaturated teal-gray, slate, rain reflections, hard chiaroscuro shadows, điểm nhấn neon đỏ cảnh báo).
  - Giai đoạn Thức tỉnh / Giải pháp: Gam màu ấm áp hy vọng (Warm amber / tungsten glow, luồng sáng vàng từ ngọn hải đăng, bình minh rạng rỡ).

---

## 4. Quy Trình Dựng & Xuất Video Chuẩn 60 FPS (Remotion Studio)

* Dự án sử dụng **Remotion Studio** (`remotion-studio/`) viết bằng React + TypeScript làm Render Engine chính ở tốc độ **60 FPS**:
  - **Spring Physics Camera**: Ken Burns mượt mà không khựng giật (`interpolate` & `spring` 60fps).
  - **Kinetic Subtitles**: Phụ đề động kiểu Documentary hiện đại, nền translucent glassmorphism, tự động highlight từ khóa tài chính/tâm lý vàng hổ phách (`#FBBF24`).
  - **Master Audio & Zero-Drift**: Toàn bộ voiceover được phát từ một file master audio duy nhất (`master_narration.wav`), loại bỏ 100% hiện tượng lệch tiếng, đứt nhịp hay khoảng lặng bất thường giữa các cảnh.
  - Hỗ trợ phát liền mạch cả ảnh tĩnh (`<CinematicSlide>`) lẫn video clip MP4 sinh từ AI Video (`<VideoAssetScene>`).
  - Audio Ducking thông minh: Tự động giảm nhạc nền xuống `-22dB` khi nhân vật cất tiếng nói.

---

## 5. Nguyên Tắc Cốt Lõi: Hoàn Toàn Dynamic - Cấm Tiệt Hardcode

* **Tuyệt đối không hardcode**:
  - Không hardcode danh sách câu, số lượng scene, tên file ảnh, tên file audio, hay đường dẫn tĩnh trong bất kỳ file Python hay React nào.
  - Mọi project mới trong `workspace/<project_name>/` đều tự động chạy trơn tru qua `run_pipeline.py`.
  - Toàn bộ pipeline hoạt động theo cơ chế **Configuration-Driven & Manifest-Driven** (`project_config.json` và `manifest.json`).

---

## 6. Quy Tắc Slot Video AI & Storyboard Motion Grid

* Khi một phân cảnh quan trọng (Hook mở đầu, cơ chế then chốt, cao trào giông bão) được chỉ định chuyển thành video AI:
  - Sử dụng thẻ `[VIDEO:4s]`, `[VIDEO:6s]`, `[VIDEO:8s]`, hoặc `[VIDEO:10s]` để khớp với thời lượng cố định của model **Omni Flash 1.1** (hoặc `10s` cho Veo 3.x).
  - Prompt engine tự động sinh **Prompt Lưới Chuyển Động 4 Ô (4-Panel Storyboard Motion Grid 2x2)** mô tả 4 giai đoạn hành động (Establishing -> Action -> Climax -> Resolution) trong `prompts_img_list.txt` để tạo ảnh storyboard trước, và `prompt_aiv_list.txt` để tạo video AI tham chiếu ảnh.
  - Khi file MP4 được tải về `workspace/<project>/videos/`, Remotion tự động nhận diện và ưu tiên phát video ở 60fps.

---

## 7. Cấu Trúc Thư Mục Chuẩn

* `pipeline/`: Các module lõi (`models.py`, `wardrobe.py`, `script_parser.py`, `voice_engine.py`, `whisper_engine.py`, `prompt_engine.py`, `asset_resolver.py`, `bgm_engine.py`, `project_manager.py`).
* `remotion-studio/`: Engine dựng video React 60fps đa luồng.
* `channels/common_assets/bgm/`: Kho Smart Mood BGM sạch bản quyền (dark_suspense, deep_contemplative, hopeful_awakening, peaceful_minimal).
* `google-flow-extension/`: Chrome Extension Native RPC `batchexecute` cho Google Flow.
* `workspace/<project_name>/`: Thư mục project độc lập chứa:
  - `script.txt`: Kịch bản chữ.
  - `manifest.json`: Toàn bộ metadata timeline, prompt, audio, visual, bgm.
  - `audio/`: `master_narration.wav` (File master thoại nguyên vẹn).
  - `bgm/`: Nhạc nền đã khớp mood hoặc sinh từ AI.
  - `timings/`: `scene_XXX_timing.json` và `master_timing.json` (Trích xuất từ faster-whisper).
  - `images/`: Ảnh tải từ Google Flow.
  - `videos/`: Video clip AI nếu có.
  - `prompts/`: `prompts_img_list.txt`, `prompt_aiv_list.txt`, và `bgm_prompts.txt`.
  - `out/`: Video 60fps render hoàn chỉnh (`final_60fps.mp4`).

---

## 10. Hệ Thống Nhạc Nền Tự Động (Smart Mood BGM & Audio Ducking)

Hệ thống hỗ trợ cơ chế phối nhạc thông minh kết hợp cả hai phương thức:
1. **Nhạc nền mặc định Kênh & Ghi công bản quyền (Default BGM & Mandatory Attribution)**:
   - **BGM Mặc định**: `a_better_future.wav` (*A Better Future by Aventure* - Modern Chill Corporate Technology Beat).
   - **Âm lượng chuẩn Documentary**: `volume_ducked: 0.035` (~ -29dB) khi có giọng đọc; `volume_normal: 0.09` (~ -21dB) khi ngắt câu.
   - **BẮT BUỘC CHÈN MUSIC ATTRIBUTION VÀO SEO**: Mọi video của kênh `thoi-quen-thinh-vuong` khi đóng gói file SEO (`SEO_VIDEO.md`) đều **BẮT BUỘC TỰ ĐỘNG CHÈN** đoạn credit FreeToUse sau đây vào phần mô tả YouTube:
     ```text
     🎵 BẢN QUYỀN ÂM NHẠC / MUSIC ATTRIBUTION:
     _______________________________________
     Music track: A Better Future by Aventure
     Source: https://freetouse.com/music
     _______________________________________
     ```
2. **Smart Mood Library & Dual-Track Crossfade (Tùy biến nâng cao)**:
   - Tự động phân tích Emotion Arc của kịch bản (mở đầu u tối/suy tư -> kết thúc thức tỉnh/bình yên).
   - Tự động chọn 2 track nhạc đối ứng (Part 1 và Part 2) từ kho nhạc sạch bản quyền và tạo chuyển tiếp (cross-fade 120 frames) tại phân cảnh đổi chiều cảm xúc.
3. **AI Generative BGM (MusicFX / MusicGen Prompts)**:
   - Tự động xuất `bgm_prompts.txt` trong thư mục `prompts/` để phục vụ tạo nhạc nền độc bản qua Google MusicFX (0 credit) hoặc MusicGen.
4. **Audio Ducking thời gian thực**:
   - Dựa vào mốc thời gian từng từ của Faster-Whisper, nhạc nền tự động giảm xuống `-29dB` (`volume: 0.035`) khi nhân vật cất tiếng nói, và tự động nổi nhẹ lên (`volume: 0.09`) ở những khoảng lặng giữa các câu để tăng sức hút điện ảnh.

---

## 8. Quy Tắc Bắt Buộc Cho Video AI: Khẩu Hình Tự Nhiên, Không Tiếng Thoại & Không Rác Visual

Mọi prompt sinh ảnh storyboard hoặc video AI trên Google Flow (Veo 3.x / Omni Flash 1.1) đều phải tuân thủ nghiêm ngặt các quy định sau:

1. **Không phát tiếng nói thoại (`No Audible Vocal Track`) - Khẩu hình linh hoạt**:
   - Nhân vật có thể có cử động môi, nét mặt biểu cảm và khẩu hình nói chuyện tự nhiên (`natural lip movements, speaking gestures are allowed`).
   - Tuyệt đối **không phát ra tiếng thoại nhân vật từ video AI (`silent vocal dialogue track`)**. Toàn bộ lời thoại được hệ thống VieNeu-TTS đảm nhiệm 100% trong khâu hậu kỳ.
   - Âm thanh hiệu ứng môi trường (SFX: tiếng bước chân, gió rít, tiếng lách cách công cụ...) được chấp nhận nếu có.

2. **Tuyệt đối không chèn nhạc nền trong video AI (`No Background Music / Soundtrack`)**:
   - Video AI không được chứa nhạc nền bài hát (`no background music, no musical score`).
   - Nhạc nền (BGM) được hậu kỳ Remotion tự động xử lý kèm Audio Ducking thông minh (-22dB khi thoại cất lên).

3. **Tuyệt đối không có watermark, logo hay chữ (`No Watermarks, No Logos, No Text Overlay`)**:
   - Khung hình phải hoàn toàn sạch sẽ (`clean cinematic render`).
   - Cấm tiệt: chữ mờ (watermark), logo thương hiệu, bong bóng thoại (speech bubble), phụ đề đóng cứng (burnt-in subtitles), hoặc ngày giờ hiển thị trên khung hình.
   - Phụ đề động Kinetic Subtitles được Remotion render trực tiếp ở 60 FPS với hiệu ứng nổi bật từ khóa vàng hổ phách.
   - **Nguyên tắc khử Watermark**: Watermark được xử lý sạch 100% ngay từ đầu vào (Input-Side) thông qua Chrome Extension (`google-flow-extension` tích hợp Reverse Alpha Blending). Khi nạp vào Remotion, pipeline giữ nguyên vẹn 100% khung hình gốc và chất lượng pixel nguyên bản, không áp dụng bất kỳ bộ lọc crop hay delogo làm mờ nào lúc render.

4. **Khung hình đơn toàn màn hình (`Single Full-Screen Viewport, No Split-Screen`)**:
   - Khi tham chiếu ảnh Storyboard lưới 4 ô (2x2), prompt video AI **bắt buộc phải nhấn mạnh**: 4 ô trong ảnh tham chiếu chỉ là các mốc chuyển động (keyframe guide). Video xuất ra **phải là 1 khung hình camera duy nhất toàn màn hình 16:9** diễn hoạt chuyển động mượt mà từ Panel 1 đến Panel 4.
   - Tuyệt đối cấm video giữ nguyên giao diện chia 4 ô màn hình (`absolutely no split-screen, no 2x2 grid layout, no collage, no borders, no sub-frames`).

---

## 9. Cấm Dùng Emotion Tags Trong TTS & Kịch Bản

- **Nghiêm cấm chèn các tag cảm xúc giả tạo**: `[thở dài]`, `[hắng giọng]`, `[cười]`, `[sigh]`, `[gasp]` vào kịch bản `script.txt` và pipeline giọng đọc.
- Giọng đọc VieNeu-TTS phải được giữ trong trẻo, tự nhiên, chuyển tiếp mạch lạc với nhịp ngắt chuẩn:
  - `leading_sec <= 0.04s` (đọc ngay khi cảnh bắt đầu, không có khoảng lặng ngắc ngứ).
  - `trailing_sec = 0.15s - 0.25s` (nhịp thở dồn dập, lôi cuốn, không để khoảng chết 1-2 giây).

---

## 11. DNA Kênh Chính Thức: "Thói Quen Thịnh Vượng" (@thoi-quen-thinh-vuong)

Mọi video, kịch bản, lời thoại và visual của channel `thoi-quen-thinh-vuong` **bắt buộc phải tuân thủ nghiêm ngặt** bộ định hướng chiến lược tại [`channels/thoi-quen-thinh-vuong/CHANNEL_DNA.md`](file:///e:/auto-video/channels/thoi-quen-thinh-vuong/CHANNEL_DNA.md):
- **Tên kênh**: **Thói Quen Thịnh Vượng**
- **Thông điệp cốt lõi**: *"Hành động nhỏ, nhất quán hàng ngày để tạo dựng sự tự chủ tài chính và tự do cuộc sống."*
- **Slogan**: *"Hành động nhỏ, Tự chủ lớn"* | *"Xây dựng hệ thống, Chinh phục tự do"*
- **3 Trụ cột nội dung**:
  1. *Thói Quen Quản Lý Dòng Tiền (Financial Micro-Habits)*: Pay yourself first, ma sát chi tiêu 48h, quy tắc 2 chiếc hộp.
  2. *Tâm Lý Học Hành Vi & Khoa Học Thần Kinh (Behavioral Neuroscience)*: Dopamine Detox, Identity Shift, Decision Fatigue.
  3. *Thiết Lập Cuộc Sống Tự Động (Autopilot Living)*: Tự động hóa dòng tiền, quy tắc If-Then, môi trường giảm ma sát.
- **Công thức Viral Hook 3 tầng**: Nỗi đau quen thuộc -> Câu hỏi phản tư duy (Contrarian) -> Cam kết giải pháp khoa học (Systems > Motivation).
- **Tone giọng**: Trầm tĩnh, khoa học, khách quan, thấu hiểu nhưng trực diện. Triết lý "Keep It Simple".

---

## 12. Hai Master Workflow Skills Cấp Cao (Xem Chi Tiết Tại `AGENT.md`)

Mọi Agent phải chủ động áp dụng 2 Master Workflow Skills tại `.agent/skills/`:
1. **`channel-dna-branding`**: Xây dựng toàn diện DNA kênh (`CHANNEL_DNA.md`), 3 content pillars, viral hooks, tone voice, prompts Google Flow (Avatar 1:1, Banner có chữ 16:9, Thumbnails) và SEO kênh (`SEO_STRATEGY.md`).
2. **`video-pipeline-end-to-end`**: Sản xuất video toàn trình 2 pha tương tác:
   - *Pha 1 (Pre-Asset)*: Parse script $\to$ VieNeu-TTS $\to$ Faster-Whisper $\to$ Prompts lưới 4 ô $\to$ Dừng xuất bảng prompt cho người dùng.
   - *Pha 2 (Post-Asset & SEO)*: Khử Watermark (Reverse Alpha Blending 100% sạch) $\to$ Match visual $\to$ Dual-track BGM Ducking (-22dB) $\to$ Remotion 60fps render $\to$ Subtitles SRT $\to$ Tự động đóng gói `SEO_VIDEO.md` (3 tiêu đề CTR cao, mô tả kèm Timestamps chuẩn từng giây từ Whisper, tags, pinned comment).



