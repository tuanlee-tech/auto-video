# AI Agent Master Playbook: Tự Động Phối Hợp 20 Skills Trong Auto Video Studio

Tài liệu này là **Cẩm Nang Hành Động Bắt Buộc (SOP)** dành cho mọi AI Agent hoạt động trong không gian dự án `auto-video`. 

> [!IMPORTANT]
> **NGUYÊN TẮC TỰ ĐỘNG HÓA**: Mọi Agent khi tham gia tạo video, viết component hoặc mở rộng pipeline **PHẢI CHỦ ĐỘNG** đọc và phối hợp nhuần nhuyễn 20 kỹ năng trong thư mục `.agent/skills/`. **TUYỆT ĐỐI KHÔNG CHỜ NGƯỜI DÙNG NHẮC NHỞ.**

---

## 1. Ma Trận 20 Skills & Cách Phối Hợp Nhuần Nhuyễn (The 6-Tier Architecture)

Codebase được thiết kế để 20 thư viện hoạt động như một dàn nhạc giao hưởng, phân chia thành **6 tầng chuyên biệt**:

```
                       ┌──────────────────────────────────────────────┐
                       │   TẦNG VI: AUTOMATION & DELIVERY             │
                       │   (gemini-api, browser-automation, youtube)  │
                       └──────────────────────┬───────────────────────┘
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│  TẦNG I: ĐẠO DIỄN VIDEO & TIMELINE MASTER (remotion-video + video-production-master)        │
│  - Điều phối các nhịp Sequence theo Audio Voiceover (Zero Drift)                            │
│  - Khung hình chuẩn 60 FPS, độ phân giải 1080p / 4K                                         │
└───────┬───────────────────────────────┬─────────────────────────────┬───────────────────────┘
        │                               │                             │
        ▼                               ▼                             ▼
┌───────────────────────┐   ┌───────────────────────┐   ┌─────────────────────────────────────┐
│  TẦNG II: 2D & MOTION │   │  TẦNG III: THIẾT KẾ   │   │  TẦNG IV: ĐỒ HỌA 3D & HIỆU ỨNG      │
│  - motion-ai (Spring) │   │  - satori-svg-gen     │   │  - threejs-3d + drei-helpers-r3f    │
│  - gsap-animation     │   │  - svgo-optimizer     │   │  - rapier-physics (Rơi, va chạm)    │
│  - animejs-lightweight│   │  - lottie-after-effect│   │  - postprocessing-effects (Bloom/   │
│  - motion-canvas-ts   │   │  - rive-interactive   │   │    Depth of Field/Film Grain)       │
└───────┬───────────────┘   └───────────┬───────────┘   └─────────────┬───────────────────────┘
        │                               │                             │
        └───────────────────────────────┴─────────────────────────────┘
                                        │
                                        ▼
                       ┌──────────────────────────────────────────────┐
                       │   TẦNG V: ÂM THANH & TRUYỀN THÔNG (AUDIO)    │
                       │   - howler-audio (SFX & sound design)        │
                       │   - whisper-srt (Transcribe & Timestamps)    │
                       │   - ffmpeg-video-assembly (Mastering)        │
                       └──────────────────────────────────────────────┘
```

---

## 2. Bản Đồ Hành Động Cho AI Agent Theo Từng Loại Tác Vụ

Khi nhận một nhiệm vụ cụ thể, Agent phải tự động kích hoạt tổ hợp kỹ năng tương ứng:

| Loại Cảnh / Tác Vụ | Tổ Hợp Kỹ Năng Bắt Buộc | Cách Thức Phối Hợp |
| :--- | :--- | :--- |
| **1. Cảnh Kể Chuyện Điện Ảnh (Cinematic Slide)** | `remotion-video` + `motion-ai` + `postprocessing-effects` | Sử dụng `spring()` và `interpolate()` 60fps để zoom/pan Ken Burns mượt mà; phủ lớp vignette và tone màu lạnh/ấm theo tâm lý nhân vật. |
| **2. Phụ Đề Động (Kinetic Typography)** | `remotion-video` + `motion-ai` | Tạo badge kính mờ glassmorphism, dùng spring nảy chữ êm ái khi voice cất lên, tự động highlight từ khóa vàng hổ phách (`#FBBF24`). |
| **3. Sơ Đồ Hệ Thống / Biểu Đồ Tài Chính** | `satori-svg-generator` + `svgo-optimizer` + `gsap-animation` | Dùng Satori biến JSX/HTML thành SVG sắc nét, nén bằng SVGO, rồi dùng GSAP Timeline vẽ nét viền (stroke-dashoffset) và hiệu ứng phân luồng dòng tiền. |
| **4. Hiệu Ứng Vật Lý (Tiền rơi, Bánh răng quay)** | `threejs-3d` + `drei-helpers-r3f` + `rapier-physics` | Nhúng component `<Canvas>` vào Remotion `<Sequence>`, tạo bánh răng đồng thau hoặc đồng tiền vàng rơi va chạm vật lý chân thực. |
| **5. Cảnh Hoạt Họa Vector Phức Tạp** | `lottie-after-effects` hoặc `rive-interactive` | Tích hợp animation Lottie/Rive JSON vào `<AbsoluteFill>` để chạy mượt mà không tốn dung lượng video. |
| **6. Thiết Kế Âm Thanh & Hiệu Ứng (SFX)** | `howler-audio` + `remotion-video` | Tự động ducking nhạc nền xuống `-22dB` khi nhân vật nói, chèn SFX tiếng bánh răng, tiếng leng keng tiền xu hoặc tiếng thở dài tại đúng frame. |
| **7. Tạo Kịch Bản & Bóc Tách B-Roll** | `gemini-api-free` + `whisper-srt-extraction` | Sinh kịch bản và phân rã các nhịp 3–5 giây theo cấu trúc Voice-First. |

---

## 3. Quy Chuẩn Code Mẫu: Kết Hợp Đa Thư Viện Trong Remotion

Dưới đây là mẫu chuẩn để Agent viết một Scene kết hợp cả **Remotion (Director) + Motion (Physics) + Satori (SVG) + Three.js (3D)**:

```tsx
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { Canvas } from '@react-three/fiber';
import { Float, Environment } from '@react-three/drei';

export const AdvancedCinematicScene: React.FC<{ title: string; imageFile: string }> = ({
  title,
  imageFile,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // 1. Spring physics camera zoom (remotion + motion-ai)
  const cameraProgress = interpolate(frame, [0, durationInFrames], [1.0, 1.05], {
    extrapolateRight: 'clamp',
  });

  // 2. Subtitle spring pop-in
  const textPop = spring({ frame: Math.max(0, frame - 15), fps, config: { damping: 14 } });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0f' }}>
      {/* Lớp nền 2D Ken Burns */}
      <img
        src={imageFile}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${cameraProgress})`,
        }}
      />

      {/* Lớp phủ 3D nhẹ (Three.js + Drei) */}
      <Canvas style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}>
        <ambientLight intensity={0.5} />
        <Float speed={2} rotationIntensity={1} floatIntensity={1}>
          {/* Vật thể 3D điểm xuyết (như hạt bụi vàng hoặc biểu tượng tài chính) */}
        </Float>
      </Canvas>

      {/* Lớp phụ đề Kinetic Glassmorphism */}
      <div style={{ position: 'absolute', bottom: 90, width: '100%', display: 'flex', justifyContent: 'center' }}>
        <div
          style={{
            background: 'rgba(12, 14, 20, 0.82)',
            backdropFilter: 'blur(12px)',
            borderRadius: 20,
            padding: '16px 36px',
            transform: `scale(${textPop})`,
            color: '#FFFFFF',
          }}
        >
          {title}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## 4. Bốn Điều Bắt Buộc Khi Tạo Video AI (Google Flow / Veo / Omni Flash)

Khi sinh prompt cho Video AI hoặc Storyboard:

1. **KHẨU HÌNH TỰ NHIÊN, CẤM PHÁT TIẾNG THOẠI (`No Audible Vocal Track`)**:
   - Nhân vật có thể cử động môi, nét mặt biểu cảm và khẩu hình nói chuyện tự nhiên (`natural lip movements, speaking gestures are allowed`).
   - Tuyệt đối **không phát ra tiếng thoại từ video AI (`silent dialogue, no spoken vocal track`)**. Toàn bộ giọng đọc do VieNeu-TTS đảm nhiệm 100% ở hậu kỳ.
   - Âm thanh môi trường và hiệu ứng âm thanh (SFX: tiếng bước chân, gió rít, tiếng lách cách công cụ...) được chấp nhận.
2. **CẤM CHÈN NHẠC NỀN (`No Background Music / Soundtrack`)**:
   - Video AI bắt buộc không có nhạc nền bài hát (`no background music, no musical score/soundtrack`).
   - Nhạc nền (BGM) do Remotion tự động xử lý và Ducking (-22dB) ở hậu kỳ.
3. **CẤM WATERMARK, LOGO VÀ CHỮ TRÊN KHUNG HÌNH (`No Watermarks, No Logos, No Subtitles`)**:
   - Khung hình phải tuyệt đối sạch (`clean cinematic render, no text overlays, no timestamps`).
   - Phụ đề do Kinetic Subtitles render trực tiếp ở 60 FPS.
4. **CẤM TRÍCH DẪN NGUYÊN VĂN TIẾNG VIỆT TRONG PROMPT**:
   - Không đưa câu thoại tiếng Việt hay dấu ngoặc kép `'...'` vào prompt để tránh việc mô hình AI hiểu lầm và vẽ chữ rác lên ảnh.
   - Chuyển toàn bộ nội dung thành mô tả hành động trực quan bằng tiếng Anh (`pure visual action & metaphor`).
5. **CẤM VIDEO CHIA Ô / SPLIT-SCREEN KHI DÙNG ẢNH STORYBOARD THAM CHIẾU**:
   - Khi gán ảnh lưới 4 ô làm tham chiếu trong Video tab, prompt **bắt buộc phải chỉ thị rõ**: 4 ô chỉ là hướng dẫn các mốc chuyển động theo thời gian, video kết xuất ra **phải là 1 khung hình camera duy nhất toàn màn hình 16:9** (`Single full-screen continuous cinematic camera shot, absolutely no split-screen, no 2x2 grid layout, no multiple panels, no collage, no borders`).
6. **CẤM TAG CẢM XÚC TRONG TTS (`No Emotion Tags`)**:
   - Cấm dùng `[thở dài]`, `[hắng giọng]`, `[cười]` trong kịch bản và TTS.
   - Tạo toàn bộ giọng đọc liền mạch trong 1 lần duy nhất (`master_narration.wav`) để giữ trọn hơi thở tự nhiên, dồn dập, sau đó dùng `faster-whisper` bóc tách timestamps chuẩn từng mili-giây.

---

## 5. Quy Chuẩn Tự Động Phối Hợp 20 Skills (Bắt Buộc Cho AI Agent)

Agent **tuyệt đối không chờ người dùng nhắc nhở mới dùng skill**. Hãy tuân theo ma trận kích hoạt tự động sau:

| Ngữ Cảnh Tác Vụ | Thư Viện Kích Hoạt Tự Động | Nguyên Tắc Thực Thi |
| :--- | :--- | :--- |
| **Xây dựng Visual Layout & Đồ họa** | `satori-svg-generator` + `svgo-optimizer` + `gsap-animation` | Biến JSX/HTML thành SVG sắc nét, nén dung lượng và dùng GSAP vẽ timeline mượt mà. |
| **Dựng Scene & Timeline Remotion** | `remotion-video` + `motion-ai` + `postprocessing-effects` | Render 60 FPS chuẩn broadcast, áp dụng Ken Burns mượt mà, chuyển cảnh Cross-Dissolve hòa trộn 18 frames `1 -> 0` và `0 -> 1`. |
| **Phụ Đề Động (Subtitles)** | `remotion-video` + `whisper-srt-extraction` | Khung cố định tĩnh lặng (stationary glassmorphism), highlight active-speech kiểu karaoke đồng bộ chính xác từng mili-giây theo `faster-whisper`. |
| **Mô Phỏng 3D & Vật Lý** | `threejs-3d` + `drei-helpers-r3f` + `rapier-physics` | Nhúng 3D Canvas vào Remotion Sequence khi cần biểu thị bánh răng, dòng tiền, hòm kho báu rơi va chạm vật lý. |
| **Xử Lý Âm Thanh & Nhịp Thoại** | `howler-audio` + `whisper-srt-extraction` + `ffmpeg-video-assembly` | Tạo Master Voice 1 lần duy nhất bằng VieNeu-TTS; dùng Whisper định vị timeline; Audio ducking -22dB khi thoại cất lên. |

---

## 6. Bảng Tự Kiểm Tra (Pre-Flight Self-Audit Checklist)

Trước khi bàn giao video hoặc code cho người dùng, Agent **bắt buộc phải tự rà soát 6 tiêu chí**:

- [ ] **1. Master Audio & Không có Emotion Tag**: Script sạch sẽ, phát từ 1 file master narration duy nhất.
- [ ] **2. Không có khoảng lặng chết 1–2s**: Nhịp thoại liền mạch tự nhiên từ master take.
- [ ] **3. Chuyển cảnh Cross-Dissolve hòa trộn mượt mà**: Cảnh cũ `1 -> 0` và cảnh mới `0 -> 1` cùng lúc trong 18 frame, master audio đọc liên tục không gián đoạn.
- [ ] **4. Phụ đề tĩnh lặng Karaoke Active-Speech**: Định vị bằng word timestamps từ faster-whisper.
- [ ] **5. Prompt hình ảnh sạch**: Không có chữ tiếng Việt, không ngoặc kép, luôn có `@stickman`.
- [ ] **6. Không Hardcode**: Toàn bộ dữ liệu đọc dynamic từ `manifest.json` và cấu hình project.
- [ ] **7. Cầu Nối Post-Hook Chuẩn Xác**: Sau 15–30s Hook bắt buộc có câu cầu nối định danh kênh (Intro Welcome) dẫn vào nội dung chính; cuối video chỉ có Outro Slogan, tuyệt đối không đặt câu chào mừng ở cuối.

---

## 7. Quy Tắc Vận Hành Pipeline (Zero-Hardcoding)

- Không bao giờ viết code cứng một lần (one-off script).
- Luôn gọi qua CLI chuẩn:
  ```bash
  python run_pipeline.py init --project <tên_project>
  python run_pipeline.py parse --project <tên_project>
  python run_pipeline.py voice --project <tên_project>
  python run_pipeline.py transcribe --project <tên_project>
  python run_pipeline.py prompts --project <tên_project>
  python run_pipeline.py match --project <tên_project>
  python run_pipeline.py render --project <tên_project> --fps 60
  ```
- Hoặc chạy tự động toàn bộ:
  ```bash
  python run_pipeline.py all --project <tên_project> --fps 60
  ```

---

## 8. Hướng Dẫn Vận Hành 2 Master Skills Cấp Cao (Workflow Skills SOP)

Để tái sử dụng quy trình sản xuất video và mở rộng cho bất kỳ kênh mới nào mà không bị phân mảnh hay hardcode, hệ thống đã đóng gói **2 Master Workflow Skills** tại `.agent/skills/`. Hai skill này đóng vai trò là "Nhạc trưởng" cấp cao, điều phối toàn bộ 20 technical skills ở 6 tầng kiến trúc.

Mọi AI Agent khi làm việc trong workspace **bắt buộc phải nhận diện đúng ngữ cảnh và kích hoạt quy trình chuẩn** theo hướng dẫn chi tiết dưới đây:

---

### 8.1. Skill 1: `channel-dna-branding` — Kiến Trúc Bản Sắc Thương Hiệu & SEO Kênh

* **Vị trí**: [`.agent/skills/channel-dna-branding/`](file:///e:/auto-video/.agent/skills/channel-dna-branding/SKILL.md)
* **Script hỗ trợ**: `python .agent/skills/channel-dna-branding/scripts/init_channel.py --channel_id <id> --name "<Tên Kênh>"`

#### A. Khi Nào Tự Động Kích Hoạt?
Agent phải chủ động kích hoạt skill này khi người dùng có các yêu cầu:
- *"Tạo kênh mới / xây dựng kênh YouTube về chủ đề X"*
- *"Xác định DNA kênh / định vị thương hiệu / phong cách kênh"*
- *"Tạo prompt làm Avatar, Banner, Thumbnail cho kênh"*
- *"Làm SEO tổng thể cho kênh / viết mô tả kênh, từ khóa kênh, danh mục playlist"*

#### B. Quy Trình 2 Chế Độ Linh Hoạt (Adaptive Flow)
1. **Chế độ A — One-Shot Generation (Khi người dùng cung cấp thông tin chi tiết)**:
   - Nếu người dùng đã nêu rõ ngách, đối tượng, phong cách $\to$ Agent tự động tổng hợp trọn bộ hồ sơ trong 1 lần duy nhất mà không cần hỏi lại.
2. **Chế độ B — Guided Interview (Khi người dùng chỉ đưa ý tưởng sơ khai)**:
   - Nếu người dùng chỉ nói chung chung (ví dụ: *"tôi muốn làm kênh tâm lý học"*), Agent dùng công cụ `ask_question` hỏi tuần tự tối đa 3 câu:
     1. *USP & Đối tượng mục tiêu*: Điểm độc bản khác biệt là gì?
     2. *Hình tượng Visual & Nhân vật*: Phong cách gì (Doodle Stickman, 3D Cinematic, Minimalist...)?
     3. *Tên kênh & Tone of Voice*: Tên chính thức và giọng đọc mong muốn (Trầm tĩnh khoa học hay truyền cảm hứng)?

#### C. Sản Phẩm Đầu Ra Bắt Buộc Của Agent
Khi hoàn thành nhiệm vụ, Agent phải bàn giao đầy đủ:
1. `channels/<channel_id>/CHANNEL_DNA.md`: 7 mục chiến lược (Định vị, 3 Trụ cột nội dung, Công thức Viral Hook 3 tầng, Cấu trúc 5 giai đoạn, Tone TTS, Quy chuẩn nhân vật `@stickman`, Thư viện 7 mẫu tiêu đề CTR cao).
2. `channels/<channel_id>/channel_config.json`: File cấu hình kỹ thuật dynamic cho pipeline.
3. `channels/<channel_id>/SEO_STRATEGY.md`: Hồ sơ SEO kênh (About 150 ký tự đầu chuẩn SEO, Channel Keywords 1 dòng copy dán, 3 Playlists theo 3 trụ cột).
4. **Bộ Prompts Google Flow (0 Credit)**:
   - **Avatar (1:1)**: Nhân vật lọt khung tròn an toàn, phong nền tối giản sạch sẽ.
   - **Banner (16:9)**: Phong cảnh rộng, vùng an toàn $1546 \times 423$, **bắt buộc ép AI vẽ trực tiếp Tên kênh và Slogan vào ảnh**.
   - **3 Thumbnails (16:9)**: Nền giấy trắng sạch, hộp highlight dạ quang bọc chữ < 5 từ, độ tương phản cực đại trên Dark Mode.

---

### 8.2. Skill 2: `video-pipeline-end-to-end` — Sản Xuất Video Toàn Trình 60FPS

* **Vị trí**: [`.agent/skills/video-pipeline-end-to-end/`](file:///e:/auto-video/.agent/skills/video-pipeline-end-to-end/SKILL.md)
* **Script hỗ trợ**: `python .agent/skills/video-pipeline-end-to-end/scripts/generate_video_seo.py -p workspace/<channel>/<project> -c channels/<channel>`

#### A. Khi Nào Tự Động Kích Hoạt?
Agent phải chủ động kích hoạt skill này khi:
- Người dùng cung cấp kịch bản (`script.txt`) và yêu cầu sản xuất video mới.
- Người dùng yêu cầu chạy lại pipeline, render video 60fps hoặc xử lý khử watermark cho video AI.
- Người dùng yêu cầu trích xuất timestamps, tạo SEO Video hoặc đóng gói file xuất bản YouTube.

#### B. Tiêu Chuẩn Thời Lượng Video Dài & Chiều Sâu (Longform Standard)
- **Thời lượng**: **> 15 phút, trung bình ~20 phút, tối đa 30–35 phút** tùy thuộc chủ đề.
- **Tôn chỉ "Sâu sắc, Tinh gọn, Không Lan Man"**: Video dài vì mang hàm lượng khoa học thần kinh và thực chiến cao, tuyệt đối cấm kéo dài hoặc bôi chữ thừa chỉ để đủ phút.
- **Quy mô kịch bản**: ~3.000 – 3.500 từ cho video 20 phút (VieNeu-TTS tốc độ 150-160 từ/phút), phân rã thành 50–75 visual beats (mỗi beat 10–20s kết hợp Ken Burns camera và đồ họa Satori/GSAP).

#### C. Quy Trình Vận Hành 2 Pha Bắt Buộc (Strict 2-Phase Interactive SOP)
Agent **bắt buộc tuân thủ ranh giới giữa 2 Pha** để phối hợp mượt mà với người dùng:

```
┌────────────────────────────────────────────────────────────────────────┐
│  PHA 1: TIỀN KỲ & SINH PROMPTS (PRE-ASSET)                             │
│  1. python run_pipeline.py init -p <project> -c <channel>              │
│  2. python run_pipeline.py parse -p <project>                          │
│  3. python run_pipeline.py voice -p <project> (VieNeu-TTS Master Take) │
│  4. python run_pipeline.py transcribe -p <project> (Faster-Whisper)   │
│  5. python run_pipeline.py prompts -p <project> (Motion Grid & Flow)   │
│  ===> DỪNG LẠI, XUẤT BẢNG PROMPT VÀ HƯỚNG DẪN NGƯỜI DÙNG TẠO ASSET <===│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Người dùng nạp ảnh & video vào
                                    ▼ images/ và videos/
┌────────────────────────────────────────────────────────────────────────┐
│  PHA 2: HẬU KỲ 60FPS & BỘ SEO XUẤT BẢN (POST-ASSET & SEO)              │
│  1. python run_pipeline.py clean -p <project> (Watermark Removal 100%) │
│  2. python run_pipeline.py match -p <project>                          │
│  3. python run_pipeline.py bgm -p <project> (Dual BGM & Ducking -22dB) │
│  4. python run_pipeline.py render -p <project> --fps 60                │
│  5. python .agent/.../generate_video_seo.py -p <proj_path> -c <ch_path>│
│  ===> BÀN GIAO VIDEO HOÀN CHỈNH, FILE SRT VÀ BỘ SEO YOUTUBE FULL <===  │
└────────────────────────────────────────────────────────────────────────┘
```

#### C. Chi Tiết Thực Thi Từng Bước Cho Agent:

> [!CAUTION]
> **QUY TẮC BẤT KHẢ XÂM PHẠM: TUYỆT ĐỐI KHÔNG ĐẢO NGƯỢC THỨ TỰ (VOICE -> WHISPER -> PROMPTS)**
> 1. Master Voice (`master_narration.wav`) phải được sinh hoàn chỉnh trước để xác lập dòng thời gian thực tế.
> 2. Faster-Whisper phải bóc tách xong mốc thời gian từng từ (`start_ms`, `end_ms`) và phân rã ranh giới cảnh trước.
> 3. **CHỈ SAU KHI Whisper hoàn tất** mới được chạy lệnh `prompts` để xuất bảng phân cảnh visual và bàn giao cho người dùng tạo asset trên Google Flow.
> TUYỆT ĐỐI CẤM bàn giao prompts hay hướng dẫn người dùng tạo ảnh/video khi Faster-Whisper chưa chạy xong.

##### Bước 1 đến 5 (Pha 1):
1. Đọc kịch bản `script.txt`, làm sạch emotion tags (cấm `[thở dài]`, `[cười]`).
2. Sinh giọng đọc VieNeu-TTS v3 Turbo (`Hải Đăng` hoặc `Thiện Minh`) thành 1 file `master_narration.wav` duy nhất (Zero Drift).
3. Chạy Faster-Whisper trích xuất mốc thời gian chính xác từng từ và phân ranh giới cảnh.
4. Sinh file prompt ảnh và prompt video lưới 4 ô (Storyboard Motion Grid 2x2).
5. **DỪNG LẠI**: Xuất bảng hướng dẫn kèm prompt rõ ràng cho người dùng tạo ảnh/video trên Google Flow (0 credit).

##### Bước 6 đến 10 (Pha 2):
6. **Khử Watermark Tự Động**: Khi người dùng nạp video AI, Agent chạy `python run_pipeline.py clean -p <project>`. Hệ thống tự động dùng **Reverse Alpha Blending + Contour Laplace** xóa sạch watermark ngôi sao của Veo/Omni Flash mà không crop hay zoom khung hình.
7. **Khớp Visual**: Chạy `python run_pipeline.py match -p <project>`.
8. **Phối BGM & Audio Ducking**: Chạy `python run_pipeline.py bgm -p <project>` tạo Dual-Track Crossfade và hạ nhạc nền xuống `-22dB` khi nhân vật nói.
9. **Render 60FPS & Xuất SRT**: Chạy `python run_pipeline.py render -p <project> --fps 60` xuất `final_60fps.mp4` và `subtitles_vi.srt`.
10. **Tự Động Đóng Gói Bộ SEO**: Chạy script:
    ```bash
    python .agent/skills/video-pipeline-end-to-end/scripts/generate_video_seo.py -p workspace/<channel>/<project> -c channels/<channel>
    ```
    Bàn giao cho người dùng file `SEO_VIDEO.md` gồm:
    - 3 Tiêu đề High-CTR (< 60 ký tự).
    - Mô tả 300 từ tối ưu từ khóa trong 2 dòng đầu.
    - Danh sách Phân cảnh / Timestamps chuẩn từng giây từ Whisper (`00:00`).
    - Thẻ Tags và Bình luận ghim (Pinned comment).
    - Tên file video upload đã đổi chuẩn SEO.

---

### 8.3. Bảng Ánh Xạ Phối Hợp Giữa 2 Master Skills Với 20 Technical Skills

| Bước Trong Quy Trình | Kỹ Năng Master Điều Phối | 20 Kỹ Năng Kỹ Thuật Tham Gia Phối Hợp |
| :--- | :--- | :--- |
| **Xây dựng DNA & Brand Identity** | `channel-dna-branding` | `gemini-api-free` (phân tích tâm lý/chiến lược) + `satori-svg-generator` (vẽ bố cục branding) |
| **Soạn & Chuốt Kịch Bản** | `video-pipeline-end-to-end` | `gemini-api-free` (cấu trúc 5 giai đoạn, xóa emotion tags) |
| **Sinh Giọng Đọc Master Voice** | `video-pipeline-end-to-end` | `ffmpeg-video-assembly` (chuẩn hóa âm lượng, sample rate 44.1kHz) |
| **Bóc Tách Timeline & Mốc Thời Gian** | `video-pipeline-end-to-end` | `whisper-srt-extraction` (Faster-Whisper word_timestamps=True) |
| **Tạo Prompt Visual & B-roll** | `video-pipeline-end-to-end` | `browser-automation-claude` / Google Flow Extension + Thẻ `@stickman` |
| **Khử Watermark Video** | `video-pipeline-end-to-end` | `ffmpeg-video-assembly` + OpenCV Reverse Alpha Blending |
| **Dựng Khung Hình & Camera 60FPS** | `video-pipeline-end-to-end` | `remotion-video` + `motion-ai` (Spring physics) + `postprocessing-effects` (Color grading) |
| **Phụ Đề Động & Bảng Biểu** | `video-pipeline-end-to-end` | `remotion-video` + `satori-svg-generator` + `svgo-optimizer` + `gsap-animation` |
| **Âm Thanh & Ducking** | `video-pipeline-end-to-end` | `howler-audio` (Audio Ducking -22dB, SFX cue points) |
| **Đóng Gói SEO & Xuất Bản** | `video-pipeline-end-to-end` | `whisper-srt-extraction` (Timestamps cho Chapters) + `youtube-api-upload` (khi cần đẩy trực tiếp) |


