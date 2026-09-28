#!/usr/bin/env python3
"""
Bộ tạo ảnh Thumbnail Doanh Nhân Chuẩn Đổi Cao (High-Converting Executive Thumbnail)
Kết hợp nền AI (Google Imagen 3) + Bộ máy ghép chữ 3D Typography & Hologram HUD
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Ensure utf-8 stdout on Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_best_font(size, bold=True):
    """Tìm font tiếng Việt Unicode chuẩn đẹp nhất trên hệ thống"""
    font_candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        os.path.join(os.path.dirname(__file__), "..", "Roboto-Bold.ttf"),
        r"C:\Windows\Fonts\tahomabd.ttf",
    ]
    for p in font_candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_3d_text(draw, pos, text, font, text_color, shadow_color=(0, 0, 0, 240), stroke_color=(0, 0, 0, 255), stroke_width=6, depth=10):
    """Vẽ chữ hiệu ứng 3D khối nổi nhiều lớp đổ bóng"""
    x, y = pos
    # 1. Vẽ các lớp tạo khối 3D sâu xuống dưới
    for d in range(depth, 0, -1):
        draw.text((x + d, y + d), text, font=font, fill=shadow_color, stroke_width=stroke_width, stroke_fill=shadow_color)
    
    # 2. Vẽ viền nét đậm (Stroke)
    if stroke_width > 0:
        draw.text((x, y), text, font=font, fill=text_color, stroke_width=stroke_width, stroke_fill=stroke_color)
    else:
        draw.text((x, y), text, font=font, fill=text_color)

def create_slanted_banner(draw, top_left, width, height, slant_offset=40, fill_color=(185, 28, 28, 245), border_color=(254, 202, 202, 220), border_width=4):
    """Vẽ dải băng đỏ vát chéo phong cách Dynamic Ribbon"""
    x, y = top_left
    pts = [
        (x + slant_offset, y),
        (x + width + slant_offset, y),
        (x + width, y + height),
        (x, y + height)
    ]
    draw.polygon(pts, fill=fill_color)
    if border_width > 0:
        draw.line(pts + [pts[0]], fill=border_color, width=border_width)

def draw_hud_icon(draw, icon_type, cx, cy, color=(6, 182, 212, 255)):
    """Vẽ icon vector phát sáng chuyên nghiệp cho HUD Hologram"""
    if icon_type == "target":
        draw.ellipse([(cx - 16, cy - 16), (cx + 16, cy + 16)], outline=color, width=2)
        draw.ellipse([(cx - 8, cy - 8), (cx + 8, cy + 8)], outline=color, width=2)
        draw.ellipse([(cx - 3, cy - 3), (cx + 3, cy + 3)], fill=(255, 215, 0, 255))
        draw.line([(cx - 20, cy), (cx + 20, cy)], fill=color, width=2)
        draw.line([(cx, cy - 20), (cx, cy + 20)], fill=color, width=2)
    elif icon_type == "chart":
        draw.rectangle([(cx - 14, cy + 4), (cx - 7, cy + 16)], fill=color)
        draw.rectangle([(cx - 3, cy - 4), (cx + 4, cy + 16)], fill=color)
        draw.rectangle([(cx + 8, cy - 14), (cx + 15, cy + 16)], fill=(255, 215, 0, 255))
        draw.line([(cx - 16, cy + 8), (cx + 5, cy - 10), (cx + 16, cy - 18)], fill=(255, 255, 255, 255), width=2)
    elif icon_type == "money":
        draw.ellipse([(cx - 16, cy - 16), (cx + 16, cy + 16)], outline=(255, 215, 0, 255), width=2)
        draw.text((cx - 6, cy - 13), "$", font=get_best_font(24, bold=True), fill=(255, 215, 0, 255))
    elif icon_type == "shield":
        pts = [(cx, cy - 16), (cx + 15, cy - 8), (cx + 12, cy + 8), (cx, cy + 18), (cx - 12, cy + 8), (cx - 15, cy - 8)]
        draw.polygon(pts, outline=color, width=2)
        draw.line([(cx - 5, cy), (cx - 1, cy + 5), (cx + 7, cy - 4)], fill=(255, 255, 255, 255), width=2)

def build_executive_thumbnail(
    bg_path,
    output_path,
    headline_top="CHỈ NÓI VỀ",
    headline_main="LỢI ÍCH",
    headline_bottom="ĐỪNG NÓI VỀ SẢN PHẨM",
    sub_badges=None
):
    print("🎨 Đang khởi tạo bộ máy thiết kế Thumbnail Doanh Nhân...")
    if not os.path.exists(bg_path):
        raise FileNotFoundError(f"Không tìm thấy ảnh nền tại: {bg_path}")

    # 1. Mở và chuẩn hóa kích thước ảnh nền 1920 x 1080 (Chuẩn Full HD 16:9)
    base_img = Image.open(bg_path).convert("RGBA")
    target_w, target_h = 1920, 1080
    if base_img.size != (target_w, target_h):
        base_img = base_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # 2. Tạo layer bóng tối mờ (Dark Vignette) phía bên trái để chữ nổi bật
    vignette = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for i in range(1000):
        alpha = int(220 * (1 - i / 1000))
        vig_draw.line([(i, 0), (i, target_h)], fill=(5, 10, 20, alpha))
    base_img = Image.alpha_composite(base_img, vignette)

    # 3. Tạo layer vẽ đồ họa và typography
    txt_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Load Fonts
    font_top = get_best_font(105, bold=True)
    font_main = get_best_font(155, bold=True)
    font_bottom = get_best_font(60, bold=True)
    font_badge = get_best_font(28, bold=True)

    # Vị trí trục X bắt đầu bên trái
    start_x = 90

    # --------------------------------------------------------------------------
    # LỚP 1: DÒNG CHỮ TRÊN: "CHỈ NÓI VỀ" (Vàng kim 3D)
    # --------------------------------------------------------------------------
    gold_color = (255, 215, 0, 255)       # Vàng ánh kim
    dark_gold = (180, 120, 10, 255)
    draw_3d_text(draw, (start_x, 80), headline_top, font_top, text_color=gold_color, shadow_color=(0, 0, 0, 250), stroke_color=(0, 0, 0, 255), stroke_width=8, depth=12)

    # --------------------------------------------------------------------------
    # LỚP 2: DẢI BĂNG ĐỎ VÁT CHÉO + DÒNG CHỮ: "LỢI ÍCH" (Trắng Chrome cực đại)
    # --------------------------------------------------------------------------
    banner_y = 230
    banner_w = 720
    banner_h = 190
    
    # Hiệu ứng phát sáng viền đỏ neon phía sau dải băng
    glow_box = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_box)
    create_slanted_banner(glow_draw, (start_x - 15, banner_y - 10), banner_w + 30, banner_h + 20, slant_offset=50, fill_color=(220, 38, 38, 120), border_color=(255, 100, 100, 255), border_width=0)
    glow_box = glow_box.filter(ImageFilter.GaussianBlur(15))
    base_img = Image.alpha_composite(base_img, glow_box)

    # Vẽ dải băng đỏ chính
    create_slanted_banner(draw, (start_x, banner_y), banner_w, banner_h, slant_offset=45, fill_color=(185, 28, 28, 240), border_color=(254, 202, 202, 230), border_width=4)

    # Vẽ chữ "LỢI ÍCH"
    draw_3d_text(draw, (start_x + 60, banner_y + 10), headline_main, font_main, text_color=(255, 255, 255, 255), shadow_color=(60, 5, 5, 255), stroke_color=(20, 0, 0, 255), stroke_width=10, depth=14)

    # --------------------------------------------------------------------------
    # LỚP 3: 4 Ô THẺ INFOGRAPHIC / HUD HOLOGRAM PHÁT SÁNG
    # --------------------------------------------------------------------------
    if sub_badges is None:
        sub_badges = [
            ("target", "GIẢI QUYẾT\nVẤN ĐỀ"),
            ("chart", "TIẾT KIỆM\nTHỜI GIAN"),
            ("money", "TIẾT KIỆM\nCHI PHÍ"),
            ("shield", "AN TÂM &\nHIỆU QUẢ")
        ]

    badge_start_y = 470
    badge_w = 175
    badge_h = 135
    spacing = 20

    for idx, (icon_type, label) in enumerate(sub_badges):
        bx = start_x + idx * (badge_w + spacing)
        by = badge_start_y

        # Khung thẻ nền kính mờ (Glassmorphism) viền Cyan Neon
        badge_pts = [(bx, by), (bx + badge_w, by), (bx + badge_w, by + badge_h), (bx, by + badge_h)]
        draw.polygon(badge_pts, fill=(15, 23, 42, 190))
        draw.line(badge_pts + [badge_pts[0]], fill=(6, 182, 212, 230), width=2)

        # Viền nhấn góc công nghệ (Tech HUD corners)
        draw.line([(bx, by), (bx + 15, by)], fill=(255, 255, 255, 255), width=3)
        draw.line([(bx, by), (bx, by + 15)], fill=(255, 255, 255, 255), width=3)

        # Vẽ Icon vector sắc nét
        draw_hud_icon(draw, icon_type, bx + badge_w // 2, by + 32)

        # Nhãn text 2 dòng
        lines = label.split('\n')
        line_y = by + 68
        for l in lines:
            bbox = draw.textbbox((0, 0), l, font=font_badge)
            lw = bbox[2] - bbox[0]
            draw.text((bx + (badge_w - lw) // 2, line_y), l, font=font_badge, fill=(241, 245, 249, 255))
            line_y += 30

    # --------------------------------------------------------------------------
    # LỚP 4: DẢI BĂNG ĐỎ CHÂN: "ĐỪNG NÓI VỀ SẢN PHẨM"
    # --------------------------------------------------------------------------
    foot_y = 660
    foot_w = 780
    foot_h = 95
    create_slanted_banner(draw, (start_x - 30, foot_y), foot_w, foot_h, slant_offset=30, fill_color=(153, 27, 27, 245), border_color=(254, 202, 202, 220), border_width=3)

    # Chia text: "ĐỪNG NÓI VỀ " (Trắng) + "SẢN PHẨM" (Vàng kim)
    draw_3d_text(draw, (start_x + 25, foot_y + 12), headline_bottom, font_bottom, text_color=(255, 235, 130, 255), shadow_color=(0, 0, 0, 255), stroke_color=(0, 0, 0, 255), stroke_width=6, depth=8)

    # --------------------------------------------------------------------------
    # LỚP 5: WATERMARK / LOGO THƯƠNG HIỆU GÓC TRÊN BÊN PHẢI
    # --------------------------------------------------------------------------
    logo_text = "AILADI"
    logo_sub = "PLATFORM DIGITAL TRANSFORMATION"
    font_logo = get_best_font(50, bold=True)
    font_sub = get_best_font(18, bold=True)

    logo_x = target_w - 360
    logo_y = 60
    # Khung badge logo
    draw.rounded_rectangle([(logo_x - 15, logo_y - 10), (logo_x + 310, logo_y + 80)], radius=8, fill=(15, 23, 42, 200), outline=(220, 38, 38, 220), width=2)
    draw.text((logo_x, logo_y), logo_text, font=font_logo, fill=(239, 68, 68, 255), stroke_width=2, stroke_fill=(255, 255, 255, 255))
    draw.text((logo_x + 190, logo_y + 15), "™", font=get_best_font(24), fill=(255, 255, 255, 220))
    draw.text((logo_x, logo_y + 52), logo_sub, font=font_sub, fill=(203, 213, 225, 255))

    # Ghép layer chữ vào ảnh gốc
    final_img = Image.alpha_composite(base_img, txt_layer)
    final_rgb = final_img.convert("RGB")

    # Lưu kết quả
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final_rgb.save(output_path, "JPEG", quality=95)
    print(f"🎉 Đã xuất thành công Thumbnail Doanh Nhân tại: {output_path}")
    return output_path

# ==============================================================================
# HÀM BỔ TRỢ TỰ ĐỘNG HÓA CHO BLOGGER AUTO-POSTER
# ==============================================================================
def slugify(text):
    """Tạo slug chuẩn SEO không dấu an toàn cho tên file ảnh"""
    import unicodedata
    import re
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.replace('đ', 'd').replace('Đ', 'D')
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).strip().lower()
    s = re.sub(r'[-\s]+', '-', text)[:45].strip('-')
    return s or "article-thumbnail"

def extract_thumbnail_headlines(title, keyword=''):
    """
    Tự động phân tách tiêu đề bài viết thành 3 dòng giật tít chuẩn phong cách Thumbnail Doanh Nhân
    """
    import re
    clean_title = re.sub(r'\[.*?\]|\(.*?\)', '', title).strip()
    
    # 1. Nếu có dấu hai chấm ":"
    if ':' in clean_title:
        parts = clean_title.split(':', 1)
        part_a = parts[0].strip().upper()
        part_b = parts[1].strip().upper()
        # Trọng tâm nằm ở phần ngắn hơn hoặc chứa từ khóa
        if len(part_a) <= 22:
            return "CHIẾN LƯỢC ĐỘT PHÁ", part_a, part_b[:32]
        else:
            words = part_a.split()
            return " ".join(words[:2]), " ".join(words[2:])[:22], part_b[:32]

    # 2. Nếu có từ khóa chính rõ ràng
    if keyword and keyword.lower() in clean_title.lower():
        kw_upper = keyword.strip().upper()
        remaining = clean_title.upper().replace(kw_upper, '').strip()
        rem_clean = re.sub(r'^[,\-\s:]+|[,\-\s:]+$', '', remaining)
        return "BÍ QUYẾT 2026", kw_upper[:22], rem_clean[:32] if rem_clean else "ĐỘT PHÁ DOANH SỐ BÁN HÀNG"

    # 3. Phân chia thông minh theo độ dài từ
    words = clean_title.upper().split()
    if len(words) <= 3:
        return "BÍ QUYẾT KINH DOANH", clean_title.upper(), "TỐI ƯU HIỆU QUẢ"
    top_w = " ".join(words[:2])
    main_w = " ".join(words[2:min(5, len(words))])
    bot_w = " ".join(words[min(5, len(words)):min(10, len(words))]) or "ĐỘT PHÁ DOANH SỐ"
    return top_w, main_w, bot_w

def call_imagen_api(prompt, api_key, output_bg_path):
    """
    Gọi Google Imagen 3 API sinh ảnh nền doanh nhân chất lượng cao
    """
    import requests
    import base64

    if not api_key:
        return False

    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9",
            "outputOptions": {"mimeType": "image/jpeg"}
        }
    }

    try:
        print(f"🎨 Đang gọi Google Imagen 3 API sinh ảnh nền độc quyền...")
        resp = requests.post(url, json=payload, timeout=60)
        if resp.status_code == 200:
            res_json = resp.json()
            predictions = res_json.get('predictions', [])
            if predictions and 'bytesBase64Encoded' in predictions[0]:
                img_data = base64.b64decode(predictions[0]['bytesBase64Encoded'])
                with open(output_bg_path, 'wb') as f:
                    f.write(img_data)
                print(f"✅ Google Imagen 3 đã sinh ảnh nền thành công!")
                return True
        else:
            print(f"ℹ️ Imagen 3 phản hồi HTTP {resp.status_code}. Tự động dùng ảnh nền doanh nhân chuẩn.")
    except Exception as e:
        print(f"ℹ️ Kết nối Imagen 3: {e}. Tự động dùng ảnh nền doanh nhân chuẩn.")
    return False

def create_post_thumbnail(title, keyword="", custom_image_url="", api_key="", repo_full_name="thuantranblog/blogger-auto-cloud"):
    """
    Hàm tổng thể: Tạo ảnh Thumbnail Doanh Nhân 16:9 và trả về link CDN vĩnh viễn
    """
    # 1. Nếu người dùng đã cung cấp sẵn link ảnh trên Google Sheets
    if custom_image_url and custom_image_url.startswith("http"):
        print(f"🖼️ Sử dụng ảnh tùy chỉnh có sẵn từ Google Sheets: {custom_image_url}")
        return custom_image_url

    clean_slug = slugify(title)
    thumb_dir = os.path.join(os.path.dirname(__file__), "thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)
    out_file = os.path.join(thumb_dir, f"{clean_slug}.jpg")

    # 2. Chuẩn bị ảnh nền
    default_sample_bg = os.path.join(os.path.dirname(__file__), "sample_bg.jpg")
    temp_bg = os.path.join(thumb_dir, f"temp_bg_{clean_slug}.jpg")
    bg_used = default_sample_bg

    # Thử gọi Imagen 3 nếu có API key
    if api_key:
        prompt_ai = (
            f"Cinematic 16:9 business YouTube thumbnail background for topic '{title}'. "
            "On the right: Confident handsome 35yo Vietnamese businessman in tailored navy blue suit interacting with glowing futuristic holographic HUD interface. "
            "Night modern luxury boardroom background with city lights bokeh. Left side clean dark negative space for text overlay, no text, photorealistic 8k."
        )
        if call_imagen_api(prompt_ai, api_key, temp_bg):
            bg_used = temp_bg

    # 3. Phân tách dòng chữ tiêu đề
    top_txt, main_txt, bot_txt = extract_thumbnail_headlines(title, keyword)

    # 4. Ghép đồ họa hoàn chỉnh
    build_executive_thumbnail(
        bg_path=bg_used,
        output_path=out_file,
        headline_top=top_txt,
        headline_main=main_txt,
        headline_bottom=bot_txt
    )

    # Xóa file nền tạm nếu có
    if bg_used == temp_bg and os.path.exists(temp_bg):
        try:
            os.remove(temp_bg)
        except Exception:
            pass

    # 5. Link CDN vĩnh viễn trên GitHub
    cdn_url = f"https://raw.githubusercontent.com/{repo_full_name}/main/thumbnails/{clean_slug}.jpg"
    print(f"🔗 Link ảnh CDN chuẩn bị nhúng vào Blogger: {cdn_url}")
    return cdn_url

if __name__ == '__main__':
    bg_file = os.path.join(os.path.dirname(__file__), "sample_bg.jpg")
    out_file = os.path.join(os.path.dirname(__file__), "executive_thumbnail_demo.jpg")
    build_executive_thumbnail(bg_file, out_file)
