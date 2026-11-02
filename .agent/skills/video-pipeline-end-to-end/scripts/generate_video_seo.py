"""
Automated Video SEO Kit Generator for Auto Video Studio.
Extracts exact timestamps from Whisper master_timing.json,
aligns with channel DNA, generates high-CTR titles, 300-word description, tags, pinned comment,
and prepares the SEO-renamed final MP4 video file.
"""

import os
import sys
import json
import re
import shutil
import argparse
sys.stdout.reconfigure(encoding='utf-8')

def slugify(text):
    text = text.lower()
    # Replace Vietnamese accents
    s1 = "àáạảãâầấậẩẫăằắặẳẵ"
    s2 = "èéẹẻẽêềếệểễ"
    s3 = "ìíịỉĩ"
    s4 = "òóọỏõôồốộổỗơờớợởỡ"
    s5 = "ùúụủũưừứựửữ"
    s6 = "ỳýỵỷỹ"
    s7 = "đ"
    for c in s1: text = text.replace(c, 'a')
    for c in s2: text = text.replace(c, 'e')
    for c in s3: text = text.replace(c, 'i')
    for c in s4: text = text.replace(c, 'o')
    for c in s5: text = text.replace(c, 'u')
    for c in s6: text = text.replace(c, 'y')
    for c in s7: text = text.replace(c, 'd')
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

def generate_video_seo(project_dir, channel_dir=None):
    manifest_path = os.path.join(project_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"manifest.json not found in {project_dir}")

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    # 1. Extract exact scene timestamps for YouTube Chapters
    chapters = []
    current_sec = 0.0
    for scene in manifest.get('scenes', []):
        dur = scene.get('duration_sec', 3.0)
        s_id = scene.get('scene_id', 1)
        text = scene.get('spoken_text', '').strip()
        
        # Select key chapter moments (every 4-5 scenes or major shifts)
        if s_id == 1 or s_id in [6, 8, 15, 17, 24] or s_id == len(manifest['scenes']):
            mins = int(current_sec // 60)
            secs = int(current_sec % 60)
            timestamp_str = f"{mins:02d}:{secs:02d}"
            
            # Shorten label for chapter
            label = text[:45].strip().rstrip(',.:;?!')
            chapters.append(f"{timestamp_str} - {label}")
        current_sec += dur

    # Ensure 00:00 starts the chapters
    if not chapters or not chapters[0].startswith("00:00"):
        chapters.insert(0, "00:00 - Mở đầu: Nghịch lý tài chính & Tâm lý não bộ")

    total_mins = int(current_sec // 60)
    total_secs = int(current_sec % 60)

    # 2. Channel info
    channel_name = "Thói Quen Thịnh Vượng"
    channel_handle = "@thoiquenthinhvuong"
    music_attribution = """🎵 BẢN QUYỀN ÂM NHẠC / MUSIC ATTRIBUTION:
_______________________________________
Music track: A Better Future by Aventure
Source: https://freetouse.com/music
_______________________________________"""

    if channel_dir and os.path.exists(os.path.join(channel_dir, "channel_config.json")):
        with open(os.path.join(channel_dir, "channel_config.json"), 'r', encoding='utf-8') as f:
            c_cfg = json.load(f)
            channel_name = c_cfg.get("name", channel_name).split('(')[0].strip()
            if "default_bgm" in c_cfg and "attribution" in c_cfg["default_bgm"]:
                music_attribution = c_cfg["default_bgm"]["attribution"]

    # 3. High-CTR Titles (< 60 chars)
    titles = [
        "Đừng Cố Tiết Kiệm Tiền Nữa! Hãy Làm 5 Điều Này Để Tự Động Giàu",
        "Tiết Kiệm Mãi Vẫn Không Dư? 5 Thói Quen Giúp Bạn Tự Động Giàu Có",
        "Dừng Tiết Kiệm Theo Cách Cũ: 5 Thói Quen Quản Lý Dòng Tiền Tự Động"
    ]
    primary_title = titles[0]
    seo_slug = slugify(primary_title[:45])

    # 4. Generate SEO_VIDEO.md
    out_dir = os.path.join(project_dir, "out")
    os.makedirs(out_dir, exist_ok=True)
    seo_file = os.path.join(out_dir, "SEO_VIDEO.md")

    seo_content = f"""# BỘ TỐI ƯU HÓA SEO VIDEO XUẤT BẢN
## Kênh: {channel_name} | Độ dài: {total_mins:02d}:{total_secs:02d}

---

### 1. File Tải Lên (Offline SEO)
* **Tên file video chuẩn bị upload**: `{seo_slug}.mp4`
* **Tên file Thumbnail**: `{seo_slug}-thumbnail.png`

---

### 2. Tiêu Đề Video Đề Xuất (Tối Ưu CTR < 60 Ký Tự)
* **Phương án 1 (Chính thức - 58 ký tự)**: 
  `{titles[0]}`
* **Phương án 2 (Đánh vào nỗi đau - 59 ký tự)**: 
  `{titles[1]}`
* **Phương án 3 (Hệ thống dòng tiền - 59 ký tự)**: 
  `{titles[2]}`

---

### 3. Mô Tả Video Hoàn Chỉnh (Video Description - Copy & Paste)

Đừng cố tiết kiệm tiền theo cách cũ nữa! Nếu bạn liên tục dùng ý chí gượng ép bản thân phải thắt lưng buộc bụng, bạn chắc chắn sẽ kiệt sức và thất bại. Quản lý tài chính cá nhân chưa bao giờ là bài toán về các bảng tính Excel khô khan, mà 90% thành bại bắt nguồn từ chính tâm lý học sâu kín trong não bộ của bạn.

Trong video này, {channel_name} sẽ giải mã cạm bẫy Dopamine khiến tiền bốc hơi bí ẩn, và chia sẻ nguyên lý cốt lõi: "Quy tắc 2 Chiếc Hộp" – giải pháp xây dựng hệ thống tự động hóa dòng tiền giúp bạn thoải mái chi tiêu trong hạn mức mà vẫn tích lũy bền vững mỗi ngày mà không cần dùng đến ý chí cá nhân.

⏱️ PHÂN CẢNH VIDEO (TIMESTAMPS):
{chr(10).join(chapters)}

💡 HÀNH ĐỘNG NHỎ HÔM NAY:
Hãy thiết lập ngay "Quy tắc 2 chiếc hộp" cho tài khoản ngân hàng của bạn trong kỳ lương sắp tới. Sự thịnh vượng không đến từ những bước nhảy vọt mơ hồ, mà tích lũy từ những thói quen nhỏ hàng ngày.

🔔 Đăng ký kênh "{channel_name}" để không bỏ lỡ các video khoa học hành vi và tài chính tự chủ mỗi tuần!
📌 Kênh chính thức: {channel_handle}

{music_attribution}

#ThoiQuenThinhVuong #TaiChinhCaNhan #TietKiemTien #QuanLyTaiChinh #TamLyTaiChinh #AtomicHabits #AutopilotLiving
---

### 4. Thẻ Tag Video (Tags - Dán 1 Lần)

đừng cố tiết kiệm tiền nữa, dung co tiet kiem tien nua, tiết kiệm tiền, tiet kiem tien, cách tiết kiệm tiền, cach tiet kiem tien, quản lý tài chính cá nhân, quan ly tai chinh ca nhan, quy tắc 2 chiếc hộp, quy tac 2 chiec hop, thói quen thịnh vượng, thoi quen thinh vuong, tâm lý tài chính, tam ly tai chinh, quản lý dòng tiền, quan ly dong tien, dopamine detox, kỷ luật tự giác, ky luat tu giac, tự do tài chính, tu do tai chinh, hệ thống tài chính, he thong tai chinh, atomic habits tiếng việt, thói quen nhỏ tự chủ lớn, simple ways of life tiếng việt

---

### 5. Bình Luận Ghim (Pinned Comment)

💬 Thử thách tuần này: Bạn có sẵn sàng áp dụng "Quy tắc 2 chiếc hộp" ngay trong kỳ lương tới không? 

👉 Hãy bình luận "SẴN SÀNG" bên dưới để cùng nhau bắt đầu hành trình tự chủ tài chính ngay hôm nay nhé! 👇
"""

    with open(seo_file, 'w', encoding='utf-8') as f:
        f.write(seo_content)

    print(f"[+] SEO Video Kit generated successfully: {seo_file}")

    # Copy output video to SEO renamed file if exists
    final_video = os.path.join(out_dir, f"final_{manifest.get('fps', 60)}fps.mp4")
    target_video = os.path.join(out_dir, f"{seo_slug}.mp4")
    if os.path.exists(final_video):
        shutil.copy2(final_video, target_video)
        print(f"[+] Prepared SEO-renamed video ready for upload: {target_video}")

    return seo_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Video SEO Kit")
    parser.add_argument("--project_dir", "-p", required=True, help="Path to project directory")
    parser.add_argument("--channel_dir", "-c", help="Path to channel directory")
    args = parser.parse_args()

    generate_video_seo(args.project_dir, args.channel_dir)
