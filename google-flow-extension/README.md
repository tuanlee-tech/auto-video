# Auto Flow: AI Video & Image Generator (Pro Clone Unlocked)

Bản clone kiến trúc chuẩn của extension Auto Flow (`lhcmnhdbddgagibbbgppakocflbnknoa`) trên Chrome Web Store, đã được dịch ngược, phân tích toàn diện và mở khóa hoàn toàn 100% tính năng (MAX / VIP Tier), loại bỏ triệt để hệ thống kiểm tra bản quyền và giới hạn tài khoản.

---

## 1. Tại sao Extension cũ thất bại và Kiến trúc mới vượt trội?

| Tiêu chí | Extension cũ (DOM Simulation) | Kiến trúc Auto Flow Clone (RPC Native) |
|---|---|---|
| **Phương thức hoạt động** | Giả lập click chuột và gõ phím vào DOM HTML của Google Flow. | Gọi trực tiếp giao thức RPC `batchexecute` của Google Flow (`flow.google.com`). |
| **Bảo mật & Anti-bot** | Bị Google Flow honeypot chặn ngay lập tức (`extension_hijack_detected`). | `interceptor.js` hook vào `MAIN` world trước khi bundle của Google tải, bảo tồn hàm `execute` gốc sạch 100%. |
| **reCAPTCHA Enterprise** | Thất bại hoặc treo vì token bị gắn nhãn giả mạo. | `mainworld-bridge.js` mint authentic reCAPTCHA Enterprise token theo từng action cụ thể (`IMAGE_GENERATION`, `VIDEO_GENERATION`). |
| **Xác thực phiên (Auth)** | Không lấy được token. | Tự động trích xuất các token ngầm từ `window.WIZ_global_data` (`SNlM0e` = at, `cfb2h` = bl, `FdrFJe` = sid) & email. |
| **Độ ổn định** | Google đổi giao diện là extension hỏng. | Giao tiếp qua giao thức dữ liệu `protobuf/wrb.fr` độc lập hoàn toàn với DOM giao diện. |
| **Tính năng & Hạn chế** | Giới hạn, lỗi giật lag. | Đầy đủ mọi chế độ Video, Image, Upscale, Hàng chờ, Tự động tải về, Đặt tên file thông minh. |

---

## 2. Các tính năng đã được Mở Khóa Hoàn Toàn (Unlocked MAX)

1. **Không giới hạn Prompts (Unlimited Prompts):**
   - Không bị giới hạn 5 prompt như bản miễn phí của store. Chạy hàng trăm, hàng nghìn prompt tự động.
2. **Đa luồng tối đa (Max Threads = 10):**
   - Chạy đồng thời tối đa 10 luồng tạo video/ảnh cùng lúc để tối ưu thời gian.
3. **Mở khóa toàn bộ chế độ Video (All Video Modes):**
   - **Text to Video (`t2v`)**: Tạo video từ mô tả văn bản.
   - **Image to Video (`i2v`)**: Tạo video từ 1 ảnh bắt đầu (Start Frame).
   - **First & Last Frame (`first_last`)**: Tạo video chuyển động giữa ảnh đầu và ảnh cuối.
   - **Reference Images / Ingredients (`r2v`)**: Tạo video tham chiếu nhân vật / phong cách từ nhiều ảnh.
   - **Video Edit (`edit`)**: Mở rộng và chỉnh sửa video có sẵn.
4. **Hỗ trợ đầy đủ các Models mới nhất:**
   - **Video**: `Omni 1.1 Flash`, `Veo 3.1 - Fast`, `Veo 3.1 - Lite`, `Veo 3.1 - Quality`.
   - **Image**: `🍌 Nano Banana Pro`, `🍌 Nano Banana 2.1`, `🍌 Nano Banana 2 Lite` (và Imagen).
5. **Nâng cấp độ phân giải (Upscale):**
   - Video upscale: 1080p, 4K.
   - Image upscale: 2K, 4K.
6. **Thư viện nhân vật & Tự động ghép tham chiếu:**
   - Lưu trữ thư viện nhân vật, hỗ trợ mention `@CharacterName` trong prompt để tự động gán ID tham chiếu.
7. **Tự động tải về & Đặt tên file thông minh:**
   - Tự động download ngay khi tạo xong với các mẫu định dạng: `{row}_{prompt}_{slot}`, `{timestamp}_{prompt}_{slot}`, `{date}_{row}_{prompt}`...

---

## 3. Cấu trúc thư mục Extension

```
google-flow-extension/
├── manifest.json              # Khai báo quyền, Content Scripts, Side Panel, Background Worker
├── interceptor.js             # Bẫy bảo vệ anti-hijack trong MAIN world (document_start)
├── mainworld-bridge.js        # Cầu nối lấy WIZ_global_data và mint reCAPTCHA hợp lệ
├── service-worker-loader.js   # Loader khởi tạo Service Worker (MV3)
├── assets/                    # Bundles đã giải mã và mở khóa
│   ├── adapter-CEOGdgvO.js    # Bộ điều phối gọi RPC Google Flow & xử lý protobuf wrb.fr
│   ├── blobStore-D681W2yd.js  # Bộ xử lý bộ nhớ tạm ảnh, mã hóa base64 và state
│   ├── naming-Com-V7dk.js     # Bộ sinh tên file tự động & hệ thống cấu hình nội bộ
│   ├── index.ts-Pz8Pbha5.js   # Background Service Worker quản lý hàng chờ, tab và engine
│   ├── index.ts-B45OwTZr.js   # Content Script chạy engine thực thi lệnh trên flow.google.com
│   ├── window-B6anPs25.js     # Giao diện Vue 3 Control Panel hiện đại
│   └── window-hUD5yl96.css    # CSS giao diện Dark Mode tối ưu
├── src/
│   ├── ui/window.html         # Trang giao diện Control Panel độc lập
│   └── icons/                 # Bộ biểu tượng extension 16, 32, 48, 128px
└── _locales/                  # Đa ngôn ngữ (Tiếng Việt `vi`, Tiếng Anh `en`...)
```

---

## 4. Hướng dẫn Cài đặt & Sử dụng (Chỉ 1 phút)

### Bước 1: Nạp Extension vào trình duyệt
1. Mở trình duyệt Chrome hoặc Microsoft Edge.
2. Truy cập vào đường dẫn: `chrome://extensions/` (hoặc `edge://extensions/`).
3. Bật công tắc **Chế độ dành cho nhà phát triển (Developer mode)** ở góc trên bên phải.
4. Nhấn nút **Tải tiện ích đã giải nén (Load unpacked)** ở góc trên bên trái.
5. Chọn thư mục: `E:\auto-video\google-flow-extension`.

### Bước 2: Mở và sử dụng
1. Truy cập vào trang web Google Flow: **`https://flow.google.com`** và đăng nhập tài khoản Google của bạn.
2. Bạn sẽ thấy một **nút tròn phát sáng (Launcher Icon)** ở góc phải phía dưới màn hình của Flow, HOẶC bạn có thể click vào biểu tượng Extension trên thanh công cụ của trình duyệt.
3. Cửa sổ **Auto Flow Control Panel** sẽ xuất hiện với đầy đủ tính năng:
   - Dán danh sách prompt vào ô nhập (hỗ trợ phân tách bằng dòng mới).
   - Chọn loại phương tiện: **Video (Veo)** hoặc **Image (Nano Banana)**.
   - Tùy chỉnh tỷ lệ (16:9, 9:16), số luồng chạy đồng thời (Threads), thời lượng (5s, 8s).
   - Thêm ảnh tham chiếu (nếu dùng chế độ Image-to-Video hoặc Reference).
   - Nhấn **Run / Chạy hàng chờ** và extension sẽ tự động làm toàn bộ việc còn lại!
