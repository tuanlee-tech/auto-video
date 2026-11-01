# Hướng Dẫn Sử Dụng Pipeline Tự Động Hóa Video 60FPS (Auto Video Studio)

Bộ công cụ tự động hóa toàn diện giúp bạn sản xuất các video giải thích dài theo phong cách **Simple Ways of Life** kết hợp **Remotion Studio (React + TypeScript)** ở tốc độ **60 FPS**, loại bỏ hoàn toàn hiện tượng khựng giật, hình chạy trước tiếng hay giật khung hình.

Hệ thống được thiết kế **hoàn toàn Dynamic (100% không hardcode)**: mọi video mới đều dùng chung một bộ code duy nhất, chỉ cần cấp kịch bản là render thành phẩm.

---

## 🎯 Quy Trình 5 Bước Hoàn Toàn Dynamic

```
[1. Khởi tạo Project]
   python run_pipeline.py init -p <tên_project> --voice "Hải Đăng" --fps 60
       ↓
[2. Phân rã Kịch bản thành Nhịp dẫn truyện (Beats)]
   python run_pipeline.py parse -p <tên_project>
       ↓
[3. Sinh Giọng Đọc Tách Scene - Zero Drift]
   python run_pipeline.py voice -p <tên_project>
       ↓
[4. Sinh Prompt 16:9 & Lưới Storyboard Motion Cho Video AI]
   python run_pipeline.py prompts -p <tên_project>
   (Tải ảnh từ Google Flow về workspace/<tên_project>/images/)
       ↓
[5. Khớp Asset & Render Video 60FPS]
   python run_pipeline.py match -p <tên_project>
   python run_pipeline.py render -p <tên_project> --fps 60
```

> [!TIP]
> Bạn có thể chạy toàn bộ 5 bước từ đầu đến cuối chỉ với 1 lệnh:
> ```bash
> python run_pipeline.py all -p <tên_project> --fps 60
> ```

---

## 🛠️ Chi Tiết Từng Lệnh Thực Thi

### Bước 1: Khởi tạo Project mới
```bash
python run_pipeline.py init --project crypto_101 --voice "Hải Đăng" --fps 60
```
Tự động thiết lập cấu trúc thư mục sạch trong `workspace/crypto_101/`. Bạn chỉ cần dán kịch bản vào file `workspace/crypto_101/script.txt`.

### Bước 2: Phân tích Kịch bản & Nhận diện Thẻ Video
```bash
python run_pipeline.py parse --project crypto_101
```
- Tự động tách câu dài thành các B-roll (3 - 5s).
- Nếu câu có gắn thẻ video như `[VIDEO:6s]`, hệ thống sẽ đánh dấu đây là slot video AI cố định thời lượng cho Omni Flash 1.1.

### Bước 3: Sinh Giọng Đọc Từng Scene (VieNeu-TTS v3)
```bash
python run_pipeline.py voice --project crypto_101
```
- Tạo từng file `scene_001.wav`, `scene_002.wav`...
- Đo thời lượng chính xác đến mili-giây và khung hình ở 60 FPS.
- Đảm bảo **Zero Drift**: Hình và tiếng luôn bắt đầu và kết thúc cùng lúc.

### Bước 4: Xuất Prompt cho Google Flow (0 Credit)
```bash
python run_pipeline.py prompts --project crypto_101
```
- Xuất file `prompts/flow_prompts.csv` nạp vào **Auto Flow Studio Extension**.
- Tự động chọn 1 trong 10 bộ trang phục Master `@stickman` theo ngữ cảnh.
- Tạo prompt dạng lưới 4 ô **Storyboard Motion Grid (2x2)** cho các slot video AI.

### Bước 5: Render Video 60FPS Bằng Remotion Studio
```bash
python run_pipeline.py render --project crypto_101 --fps 60
```
- Đồng bộ asset vào Remotion Studio.
- Render song song đa tiến trình trên Chromium 60 FPS.
- Áp dụng camera Ken Burns vật lý mượt mà (Spring Physics), phụ đề Kinetic Subtitles nổi bật từ khóa, và xuất file MP4 sắc nét tại `workspace/<tên_project>/out/final_60fps.mp4`.
