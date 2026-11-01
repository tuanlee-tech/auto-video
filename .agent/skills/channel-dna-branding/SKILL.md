---
name: channel-dna-branding
description: Xây dựng toàn diện DNA kênh YouTube (Niche, Slogan, 3 Content Pillars, Viral Hooks, Tone of Voice) và bộ nhận diện thương hiệu (Prompts Google Flow cho Avatar, Banner có chữ, Thumbnails) cùng SEO Kênh tổng thể (Mô tả Kênh, Từ khóa kênh, Danh mục Playlist).
---

# Channel DNA & Branding Architect Skill

Kỹ năng này chuyên trách định hình và đóng gói toàn bộ bản sắc thương hiệu, triết lý nội dung, hình ảnh nhận diện và chiến lược SEO nền tảng cho bất kỳ kênh YouTube mới nào trong hệ sinh thái `auto-video`.

---

## 1. Khi Nào Kích Hoạt Kỹ Năng Này?

Kích hoạt skill này khi:
* Người dùng muốn tạo một kênh YouTube mới hoàn toàn (ví dụ: kênh tài chính, tâm lý, công nghệ, lịch sử, đời sống...).
* Cần nâng cấp, tái cấu trúc hoặc chuyên nghiệp hóa bản sắc của một kênh hiện có.
* Cần sinh bộ Prompts hình ảnh chuẩn cho Google Flow (Avatar 1:1, Banner 16:9 có chữ, Thumbnail 16:9).
* Cần soạn thảo bộ SEO Kênh tổng thể (Mô tả kênh About, Từ khóa kênh Channel Keywords, Cấu trúc 3 Playlists cốt lõi).

---

## 2. Quy Trình Vận Hành 2 Chế Độ (Adaptive Workflow)

Khi người dùng đưa ra yêu cầu về kênh mới, Agent tự động phân loại thông tin đầu vào theo 2 chế độ:

### Chế độ A: Tổng Hợp Trọn Gói Một Lần (One-Shot Generation)
* **Điều kiện**: Người dùng cung cấp mô tả chi tiết (Tên kênh, ngách nội dung, đối tượng khán giả, phong cách mong muốn).
* **Hành động**: Agent tự động phân tích sâu, kết hợp các nguyên lý tâm lý học/truyền thông đỉnh cao và xuất trọn gói toàn bộ hồ sơ trong 1 lần duy nhất:
  1. File `channels/<channel_id>/CHANNEL_DNA.md`
  2. File `channels/<channel_id>/channel_config.json`
  3. File `channels/<channel_id>/SEO_STRATEGY.md`
  4. Bộ Prompts Google Flow (Avatar, Banner có chữ trực tiếp, 3 mẫu Thumbnail CTR cao).

### Chế độ B: Phỏng Vấn Định Hướng 3 Câu (Guided Interview)
* **Điều kiện**: Người dùng chỉ cung cấp ý tưởng sơ khai (ví dụ: *"tôi muốn làm kênh về quản lý thời gian"*).
* **Hành động**: Agent sử dụng công cụ `ask_question` hỏi tuần tự tối đa 3 câu hỏi cốt lõi:
  1. *Ngách nội dung & Tuyên ngôn giá trị*: Điểm độc bản (USP) khác biệt với đối thủ là gì?
  2. *Hình tượng nhân vật & Phong cách Visual*: Phong cách vẽ nào (Doodle stickman, 3D, Anime...)?
  3. *Tên kênh & Tone of Voice*: Tên chính thức và giọng điệu (Trầm tĩnh khoa học, hóm hỉnh, hay mạnh mẽ quyết liệt)?
  Sau đó xuất toàn bộ hồ sơ như Chế độ A.

---

## 3. Cấu Trúc Hồ Sơ Chuẩn Đầu Ra Của Skill

Mỗi kênh mới được khởi tạo bắt buộc phải có đầy đủ 3 tài liệu chuẩn mực tại `channels/<channel_id>/`:

### 1. `CHANNEL_DNA.md` (Hiến Chương Kênh)
Bao gồm 7 mục chiến lược:
1. **Định Vị & Triết Lý Cốt Lõi**: Niche positioning, Quiet Wealth/Value, Slogan chính & phụ.
2. **3 Trụ Cột Nội Dung (Content Pillars)**: 3 nhánh chủ đề lớn với các tiểu chủ đề hành động vi mô.
3. **Công Thức Viral Hook 3 Tầng & Cầu Nối Post-Hook (Post-Hook Transition Bridge)**:
   - 3 tầng Hook: Nỗi đau quen thuộc $\to$ Câu hỏi phản tư duy $\to$ Cam kết giải pháp khoa học/hệ thống.
   - **Bắt buộc**: Bộ 5 mẫu cầu nối định danh thương hiệu ngay sau Hook (Option 1: *"Hôm nay, hãy cùng {channel} tìm hiểu..."*, Option 2: *"Xin chào, tôi là {character} từ {channel}..."*, v.v.).
4. **Cấu Trúc Video 5 Giai Đoạn**: Khung sườn kịch bản giữ chân người xem (Retention & Binge-watching).
5. **Tone of Voice & Nhạc Nền**: Giọng đọc TTS chuẩn (Hải Đăng/Thiện Minh), sắc thái, câu Outro cố định.
6. **Quy Chuẩn Nhân Vật & Hình Ảnh**: Thẻ nhân vật (ví dụ `@stickman`), bảng trang phục, màu sắc chủ đạo.
7. **Thư Viện Tiêu Đề Mẫu High-CTR**: 7 công thức tiêu đề theo 4 góc độ tâm lý.

### 2. `channel_config.json` (Cấu Hình Kỹ Thuật Kênh)
```json
{
  "channel_id": "<channel_id>",
  "name": "<Tên Kênh Chính Thức>",
  "slogan": "<Slogan Chính>",
  "secondary_slogan": "<Slogan Phụ>",
  "description": "<Mô tả định vị ngắn>",
  "aspect_ratio": "16:9",
  "width": 1920,
  "height": 1080,
  "fps": 60,
  "default_voice": "Hải Đăng",
  "character_tag": "@<character_id>",
  "character_reference_image": "characters/<character_master>.png",
  "wardrobe_rule": "<Tên bộ sưu tập trang phục>",
  "art_style": "<Mô tả phong cách mỹ thuật>",
  "lighting_style": "<Quy tắc ánh sáng>",
  "content_pillars": [
    "<Trụ cột 1>",
    "<Trụ cột 2>",
    "<Trụ cột 3>"
  ],
  "outro_catchphrase": "<Câu khẩu hiệu kết video>"
}
```

### 3. `SEO_STRATEGY.md` (Chiến Lược SEO Kênh)
1. **Mô tả Kênh (Channel About)**: Tối ưu 150 ký tự đầu tiên chứa từ khóa chính, tổng độ dài 800-1000 ký tự.
2. **Từ khóa của Kênh (Channel Keywords)**: 1 chuỗi phân tách bằng dấu phẩy để dán trực tiếp vào YouTube Studio Settings.
3. **Cấu trúc 3 Playlists**: Tiêu đề và mô tả chuẩn SEO cho từng danh sách phát theo 3 trụ cột.

---

## 4. Quy Chuẩn Viết Prompt Cho Google Flow (0 Credit)

Mọi prompt sinh ảnh thương hiệu do skill này tạo ra phải tuân thủ nghiêm ngặt:
* **Avatar (1:1)**: Nhân vật nằm gọn trong khung tròn an toàn ($R=360\text{ px}$), biểu cảm rạng rỡ, thân thiện, phông nền đơn sắc tối giản.
* **Banner (16:9)**: Phong cảnh toàn cảnh, có vùng an toàn ở trung tâm ($1546 \times 423$), **bắt buộc yêu cầu AI vẽ trực tiếp tên kênh và slogan** vào bầu trời với vệt highlight nổi bật.
* **Thumbnail (16:9)**: Nền giấy trắng sạch sẽ, hộp highlight màu dạ quang (vàng/cam) bọc lấy tiêu đề ngắn gọn (dưới 5 từ), nhân vật tương tác với sơ đồ minh họa, độ tương phản cực đại trên YouTube Dark Mode.
