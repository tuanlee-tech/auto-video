# Auto Video Studio: Dynamic Video Pipeline Architecture

Tài liệu này mô tả chi tiết kiến trúc của **Auto Video Studio** - hệ thống sản xuất video AI tự động, hoạt động hoàn toàn **dynamic (linh hoạt 100%)**, **nghiêm cấm hardcode** bất kỳ giá trị nào (như danh sách câu, số lượng scene, tên file ảnh, đường dẫn tĩnh).

Mọi project video mới (dù là 5 phân cảnh hay 500 phân cảnh) đều sử dụng chung một codebase duy nhất thông qua cơ chế hướng cấu hình (**Configuration-Driven & Manifest-Driven**).

---

## 1. Cấu Trúc Thư Mục Chuẩn Đa Kênh (Multi-Channel Architecture)

Hệ thống quản lý tài nguyên theo mô hình 2 tầng: **Channel Profile** (đặc tính kênh) và **Project Workspace** (từng tập video):

```
e:\auto-video\
├── channels/                           # QUẢN LÝ ĐA KÊNH (Channel Profiles)
│   ├── channel_01_finance_stickman/    # Kênh 1: Tài chính dài 16:9
│   │   ├── channel_config.json         # Giọng Hải Đăng, 16:9, @stickman, phong cách Cinematic Hybrid
│   │   ├── characters/                 # Bảng ảnh tham chiếu nhân vật Master (stickman_master.png)
│   │   └── README.md
│   ├── channel_02_life_philosophy/     # Kênh 2: Triết lý cuộc sống 16:9 (Giọng Thiện Minh tự sự)
│   │   └── channel_config.json
│   └── channel_03_finance_shorts/      # Kênh 3: Shorts & TikTok 9:16 (1080x1920 dọc)
│       └── channel_config.json
│
├── workspace/                          # DỮ LIỆU TỪNG DỰ ÁN VIDEO THEO KÊNH
│   └── channel_01_finance_stickman/
│       └── test_vn/                    # Dự án video cụ thể
│           ├── project_config.json     # Cấu hình độc lập (kế thừa từ channel)
│           ├── script.txt              # Kịch bản gốc (hỗ trợ tag [thở dài], [hắng giọng], [cười])
│           ├── manifest.json           # File metadata timeline, prompt, audio, visual
│           ├── audio/                  # Voiceover tách biệt từng scene (scene_001.wav,...)
│           ├── images/                 # Ảnh B-roll tải từ Google Flow (001_..., 002_...)
│           ├── videos/                 # Video clip AI nếu có (001.mp4, 016.mp4,...)
│           ├── prompts/                # flow_prompts.csv, prompts_list.txt, storyboards.json
│           └── out/                    # Video thành phẩm render 60fps (đã được .gitignore)
```

---

## 2. Các Module Cốt Lõi (Python & Remotion)

Codebase được chia thành các tầng module độc lập, có thể tái sử dụng vô hạn lần:

| Module | Đường Dẫn | Nhiệm Vụ |
| :--- | :--- | :--- |
| **Data Models** | `pipeline/models.py` | Định nghĩa schema chuẩn `SceneBeat` và `ProjectConfig`. |
| **Wardrobe Engine** | `pipeline/wardrobe.py` | Bộ sưu tập 10 trang phục chuẩn (`@stickman`), bộ phân tích ngữ cảnh tự động chọn outfit và ánh sáng. |
| **Script Parser** | `pipeline/script_parser.py` | Phân tích cú pháp `script.txt`, tự động tách câu dài thành B-roll (3-5s), nhận diện thẻ video `[VIDEO:6s]`. |
| **Voice Engine** | `pipeline/voice_engine.py` | Sinh TTS tách biệt từng scene bằng **VieNeu-TTS**, đo thời lượng chính xác từng mili-giây, tự động bù padding cho slot video AI cố định. |
| **Prompt Engine** | `pipeline/prompt_engine.py` | Tự động sinh prompt 16:9 kèm thẻ `@stickman` và prompt dạng lưới 4 ô Storyboard Motion cho các cảnh video. |
| **Asset Resolver** | `pipeline/asset_resolver.py` | Quét thư mục ảnh/video và map động theo tiền tố số thứ tự (1_, 01_, 001_). Ưu tiên video clip nếu có. |
| **Project Manager** | `pipeline/project_manager.py` | Bộ điều phối vòng đời của project, đồng bộ assets và trigger Remotion. |
| **Remotion Studio** | `remotion-studio/` | Engine React + TypeScript dựng video **60 FPS** với Ken Burns mượt mà, Kinetic Subtitles và Audio Ducking. |

---

## 3. Quy Trình Vận Hành 100% Dynamic Qua CLI

Mọi thao tác sản xuất video đều được điều khiển qua `run_pipeline.py`:

### Bước 1: Khởi tạo project mới
```bash
python run_pipeline.py init --project crypto_101 --voice "Hải Đăng" --fps 60
```
Tự động tạo đầy đủ cây thư mục và `project_config.json`. Người dùng chỉ việc đặt nội dung vào `workspace/crypto_101/script.txt`.

### Bước 2: Phân rã kịch bản (Parse)
```bash
python run_pipeline.py parse --project crypto_101
```
Tự động tách kịch bản thành các nhịp dẫn chuyện (beats) dài 3-5 giây, gán outfit phù hợp và lưu vào `manifest.json`.

### Bước 3: Sinh giọng đọc chuẩn mili-giây (Voice)
```bash
python run_pipeline.py voice --project crypto_101
```
Sinh từng file `scene_001.wav`, `scene_002.wav`... đo chính xác số khung hình tại 60 FPS. Đảm bảo **Zero Drift (triệt tiêu 100% hiện tượng lệch tiếng và hình)**.

### Bước 4: Xuất Prompt cho Google Flow (Prompts)
```bash
python run_pipeline.py prompts --project crypto_101
```
Xuất ra `flow_prompts.csv` và `prompts_list.txt`. Đối với các cảnh video AI, tự động sinh prompt **4-panel storyboard motion grid** để tạo video trên Flow Video / Omni Flash 1.1.

### Bước 5: Khớp ảnh/video đã tải về (Match)
```bash
python run_pipeline.py match --project crypto_101
```
Tự động quét thư mục `images/` và `videos/`, ghép nối chính xác từng file vào từng scene trong manifest mà không cần hardcode tên file.

### Bước 6: Render video 60fps hoàn chỉnh (Render)
```bash
python run_pipeline.py render --project crypto_101 --fps 60
```
Đồng bộ asset vào Remotion Studio, gọi Remotion engine render song song đa luồng ở 60 FPS, áp dụng Ken Burns mượt mà, Kinetic Subtitles và xuất ra file MP4 chất lượng cao.

> [!TIP]
> Bạn cũng có thể chạy toàn bộ quy trình từ đầu đến cuối chỉ bằng 1 câu lệnh duy nhất:
> ```bash
> python run_pipeline.py all --project crypto_101 --fps 60
> ```

---

## 4. Cơ Chế Slot Video AI (Omni Flash 1.1 Fixed Durations)

Khi muốn một cảnh là video chuyển động thay vì ảnh tĩnh (ví dụ: cảnh Hook đầu video, cảnh cơ chế then chốt):
1. Thêm thẻ thời lượng vào đầu câu trong `script.txt`:
   ```text
   [VIDEO:6s] Bạn có bao giờ tự hỏi: Tại sao kiếm tiền đã khó, nhưng giữ được tiền lại còn khó hơn gấp mười lần?
   ```
2. Các thời lượng hợp lệ của model **Omni Flash 1.1**: `4s`, `6s`, `8s`, `10s`.
3. `voice_engine.py` sẽ tự động tính toán và bù trailing silence (khoảng lặng tinh tế) để audio dài đúng bằng thời lượng video AI.
4. `prompt_engine.py` sẽ tạo prompt dạng **4-panel storyboard motion grid (2x2)** mô tả chuyển động liên tục qua 4 khung hình (Establishing, Action Build-up, Climax, Resolution).
5. Người dùng đưa ảnh grid đó sang Flow Video để sinh ra video clip MP4, lưu vào `workspace/<project>/videos/001_hook.mp4`.
6. Remotion Studio tự động nhận diện file MP4 và phát video mượt mà tại đúng thời điểm đó.
