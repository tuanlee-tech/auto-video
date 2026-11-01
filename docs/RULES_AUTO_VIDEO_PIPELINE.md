# Tài Liệu Quy Chuẩn Hệ Thống Auto Video Pipeline

Xem tài liệu chi tiết tại file gốc: [GEMINI.md](file:///e:/auto-video/GEMINI.md)

### Tóm tắt nhanh cho Nhà sáng tạo & Developer:
1. **TTS Engine**: Sử dụng VieNeu-TTS v3 Turbo (Voice: `Hải Đăng`).
2. **Character Tag**: Mọi prompt phải bắt đầu bằng `@stickman` kèm mô tả 1 trong 10 bộ trang phục từ Character Wardrobe Sheet.
3. **Phong cách visual**: Cinematic Hybrid (2D Minimalist Cel-shaded character trên nền 3D Photorealistic Cinematic Environment).
4. **Lệnh tạo dữ liệu**:
   - `python run_pipeline.py timeline ...`
   - `python run_pipeline.py broll ...`
5. **Lệnh dựng video**:
   - `python run_pipeline.py assemble --audio ... --images ... --manifest ... --res 1080p --out ...`
