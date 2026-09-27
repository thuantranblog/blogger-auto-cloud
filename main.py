#!/usr/bin/env python3
"""
Blogger Gemini AI Cloud Auto-Poster
Tự động viết bài chuẩn SEO và đăng lên Blogger.com trên đám mây (GitHub Actions)
Hỗ trợ: Google Gemini API + Blogger API v3 + CTA LuViet
"""

import os
import sys
import json
import time
from datetime import datetime, timezone, timedelta
import requests

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except ImportError:
    print("❌ Vui lòng cài đặt google-api-python-client và google-auth!")
    sys.exit(1)

# Load local .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ==============================================================================
# CẤU HÌNH HỆ THỐNG
# ==============================================================================
def clean_credential(val):
    if not val:
        return ''
    v = str(val).strip().strip('"').strip("'")
    if '=' in v and not v.startswith('1//'):
        v = v.split('=', 1)[1].strip().strip('"').strip("'")
    # Loại bỏ hoàn toàn ký tự xuống dòng và khoảng trắng do copy-paste từ PowerShell
    v = v.replace('\n', '').replace('\r', '').replace(' ', '')
    return v

def get_api_key_pool():
    import re
    # Hỗ trợ lấy key từ nhiều nguồn biến môi trường: GEMINI_API_KEY, GEMINI_API_KEYS, GEMINI_BACKUP_API_KEY
    # Người dùng có thể nhập 1 key hoặc nhiều key cách nhau bởi dấu phẩy, chấm phẩy hoặc xuống dòng
    raw = os.environ.get('GEMINI_API_KEY', '')
    backups = os.environ.get('GEMINI_API_KEYS', '') + ',' + os.environ.get('GEMINI_BACKUP_API_KEY', '')
    combined = raw + ',' + backups
    tokens = re.split(r'[,;\n\r]+', combined)
    pool = []
    for t in tokens:
        clean_k = clean_credential(t)
        if clean_k and clean_k not in pool:
            pool.append(clean_k)
    return pool

BLOGGER_BLOG_ID = clean_credential(os.environ.get('BLOGGER_BLOG_ID'))
GOOGLE_CLIENT_ID = clean_credential(os.environ.get('GOOGLE_CLIENT_ID'))
GOOGLE_CLIENT_SECRET = clean_credential(os.environ.get('GOOGLE_CLIENT_SECRET'))
GOOGLE_REFRESH_TOKEN = clean_credential(os.environ.get('GOOGLE_REFRESH_TOKEN'))

# Chế độ phát hành: 'schedule' (Lên lịch tương lai), 'publish' (Đăng ngay), 'draft' (Lưu nháp)
POST_MODE = os.environ.get('POST_MODE', 'schedule').lower().strip()
SCHEDULE_HOURS_AHEAD = int(os.environ.get('SCHEDULE_HOURS_AHEAD', '24'))

# Thông tin thương hiệu LuViet & Nền tảng AILADI
REGISTER_URL = os.environ.get('REGISTER_URL', 'https://my.luviet.com/register')
ZALO_URL = os.environ.get('ZALO_URL', 'https://zalo.me/1501073926693571291')
FANPAGE_URL = os.environ.get('FANPAGE_URL', 'https://www.facebook.com/webluviet/')

TOPICS_FILE = os.path.join(os.path.dirname(__file__), 'topics.txt')
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'posted_history.json')

# ==============================================================================
# HÀM GỌI GEMINI AI VIẾT BÀI CHUẨN SEO
# ==============================================================================
def generate_seo_article(topic, labels, summary='', cta_url=REGISTER_URL):
    api_keys = get_api_key_pool()
    if not api_keys:
        raise Exception("Không tìm thấy Gemini API Key nào hợp lệ!")

    print(f"\n🧠 Đang gọi Google Gemini AI viết bài cho chủ đề: '{topic}'...")
    print(f"🔑 Số lượng API Key trong hồ chứa (Key Pool): {len(api_keys)}")

    prompt = f"""
Bạn là chuyên gia Content Marketing, SEO Master và Copywriter hàng đầu Việt Nam. Hãy tạo một bài viết chuẩn SEO chuyên sâu, cấu trúc chặt chẽ, tối ưu tỷ lệ chuyển đổi (CRO) bằng tiếng Việt cho nền tảng Blogger/Blogspot theo các thông số sau:

- Chủ đề / Từ khóa chính: "{topic}"
- Nhãn chuyên mục mong muốn: "{', '.join(labels)}"
{f'- Tóm tắt gợi ý / Góc nhìn: "{summary}"' if summary else ''}
- Liên kết chuyển đổi mục tiêu (BẮT BUỘC): "{cta_url}"
- Độ dài mục tiêu: Khoảng 1500 - 2000 từ.
- Tông giọng: Chuyên gia thực chiến, đồng cảm sâu sắc với nỗi đau của người kinh doanh, lập luận sắc sảo, truyền cảm hứng và thôi thúc hành động mạnh mẽ.

CHIẾN LƯỢC NỘI DUNG & ĐIỀU HƯỚNG CHUYỂN ĐỔI (QUAN TRỌNG NHẤT):
1. ĐỐI TƯỢNG VÀ CHÂN DUNG KHÁCH HÀNG MỤC TIÊU:
   - Bài viết đánh trúng nỗi đau thực tế của: Chủ shop online bán lẻ (thời trang, mỹ phẩm, mẹ & bé), hộ kinh doanh cá thể, chủ quán cafe/nhà hàng/quán ăn (F&B), chủ cơ sở dịch vụ/spa/nha khoa và doanh nghiệp vừa & nhỏ (SMEs).
   - Nỗi đau: Chi phí sàn TMĐT tăng cao (18-25%), rủi ro khóa shop mất trắng khách, chi phí quảng cáo đắt đỏ, đơn hàng bị bom do COD, thuê làm website cồng kềnh 10-20 triệu mà không hiệu quả, quản lý đơn hàng thủ công thất thoát data.

2. GIẢI PHÁP ĐỘT PHÁ - NỀN TẢNG AILADI (my.luviet.com):
   - Định vị AILADI là hệ sinh thái tạo website bán hàng tự động 24/7 và giải pháp chuyển đổi số toàn diện.
   - Khởi tạo siêu tốc 30 giây không cần biết lập trình (No-Code).
   - Form đặt hàng 1-chạm (1-Click Checkout) siêu nhanh, tối ưu trải nghiệm khách hàng.
   - Tích hợp thanh toán VietQR động tự điền số tiền và nội dung, quét app ngân hàng 3 giây tiền về tài khoản ngay, ép tỷ lệ bom hàng về dưới 3%.
   - Kết nối tự động API 4 hãng vận chuyển lớn (GHTK, GHN, Viettel Post, VNPost), tự tính phí ship đến từng xã/phường, in mã vận đơn A6 trong 1 giây.
   - Menu QR Code điện tử đặt món tại bàn và giao tận nơi cho ngành F&B, quán cafe, nhà hàng.
   - Trợ lý AI Gemini 24/7 tự động tư vấn, chốt đơn ca đêm và viết bài SEO.
   - Cơ sở dữ liệu riêng biệt (Database Per-Tenant) an toàn tuyệt đối 100% doanh thu và dữ liệu khách hàng.

3. ĐIỀU HƯỚNG LIÊN KẾT (INTERNAL LINKING - BẮT BUỘC):
   - Trong thân bài: BẮT BUỘC chèn tự nhiên từ 2 đến 3 liên kết ngữ cảnh (contextual anchor text) dẫn người đọc bấm vào link: "{cta_url}".
   - Ví dụ các dạng anchor text chuyển đổi cao:
     + <a href="{cta_url}" target="_blank" rel="noopener">đăng ký tạo website bán hàng miễn phí trên AILADI</a>
     + <a href="{cta_url}" target="_blank" rel="noopener">trải nghiệm nền tảng AILADI</a>
     + <a href="{cta_url}" target="_blank" rel="noopener">tạo tài khoản AILADI chỉ trong 30 giây</a>

4. KHỐI CALL TO ACTION (CTA) ĐẲNG CẤP Ở CUỐI BÀI:
   - BẮT BUỘC chèn khối CTA nổi bật dạng hộp viền nổi, màu sắc bắt mắt, tối ưu tỷ lệ nhấp chuột (CRO):
     <div style="margin: 35px 0 20px; padding: 25px; background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%); border: 2px solid #0284c7; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.15);">
       <h3 style="color: #0369a1; margin-top: 0; font-size: 20px; font-weight: 700;">🚀 Bắt Đầu Đột Phá Doanh Số Bán Hàng Cùng AILADI Ngay Hôm Nay!</h3>
       <p style="color: #334155; font-size: 15px; line-height: 1.6; margin-bottom: 20px;">Đừng để chi phí sàn và quy trình thủ công bào mòn lợi nhuận của bạn. Sở hữu ngay website bán hàng đa kênh tự động trong 30 giây – Miễn phí khởi tạo, không cần biết code, đồng bộ đơn hàng và thanh toán VietQR tức thì.</p>
       <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 12px;">
         <a href="{cta_url}" target="_blank" rel="noopener" style="background: #2563eb; color: #ffffff; font-weight: bold; font-size: 16px; padding: 12px 28px; border-radius: 8px; text-decoration: none; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.35); display: inline-block;">👉 Đăng Ký Tạo Website Miễn Phí Tại Đây</a>
         <a href="{ZALO_URL}" target="_blank" rel="nofollow" style="background: #0068ff; color: #ffffff; font-weight: bold; font-size: 15px; padding: 12px 20px; border-radius: 8px; text-decoration: none; display: inline-block;">💬 Hỗ Trợ Kỹ Thuật Zalo OA</a>
         <a href="{FANPAGE_URL}" target="_blank" rel="nofollow" style="background: #1877f2; color: #ffffff; font-weight: bold; font-size: 15px; padding: 12px 20px; border-radius: 8px; text-decoration: none; display: inline-block;">👍 Nhắn Tin Fanpage LuViet</a>
       </div>
     </div>

5. CẤU TRÚC BÀI VIẾT (BẮT BUỘC):
   - TIÊU ĐỀ (Title): Giật tít hấp dẫn, chứa từ khóa chính ở đầu, dưới 65 ký tự, kích thích lượt click (CTR).
   - SAPO: Mở bài cuốn hút 2-3 đoạn ngắn theo công thức PAS (Problem - Agitate - Solution).
   - THÂN BÀI: Sử dụng thẻ <h2> và <h3> rõ ràng, logic. Luôn dùng danh sách (<ul>, <li>) để thoáng mắt.
   - BẢNG BIỂU: BẮT BUỘC có 1 Bảng so sánh (HTML <table>) trực quan, viền mỏng chuyên nghiệp (border: 1px solid #cbd5e1).
   - FAQ: BẮT BUỘC có mục <h2>Câu hỏi thường gặp (FAQ)</h2> với ít nhất 3 câu hỏi thực tế và câu trả lời thấu đáo.
   - PROMPT TẠO ẢNH: Viết 1 đoạn Prompt tiếng Anh chi tiết, chuyên nghiệp để tạo ảnh Thumbnail 16:9 chất lượng cao.

ĐỊNH DẠNG TRẢ VỀ:
Hãy trả về DUY NHẤT một chuỗi JSON hợp lệ (không kèm theo bất kỳ văn bản giải thích nào ngoài JSON) theo cấu trúc:
{{
  "title": "Tiêu đề bài viết dưới 65 ký tự",
  "labels": ["Nhãn 1", "Nhãn 2"],
  "metaDescription": "Mô tả tìm kiếm tóm tắt dưới 155 ký tự chuẩn SEO",
  "imagePrompt": "English prompt for 16:9 thumbnail image...",
  "content": "<div class='seo-post-content'><p>...</p><h2>...</h2>...</div>"
}}
"""

    models = ['gemini-2.5-flash', 'gemini-2.5-pro']
    last_err = None

    # VÒNG LẶP DỰ PHÒNG QUA TỪNG API KEY (KEY POOL ROTATION)
    for key_idx, current_key in enumerate(api_keys, 1):
        key_masked = current_key[:6] + "..." + current_key[-4:] if len(current_key) > 10 else "***"
        print(f"\n🔑 Thử gọi Gemini với API Key #{key_idx}/{len(api_keys)} [{key_masked}]...")

        key_overloaded = False
        for model in models:
            try:
                print(f"👉 Thử tạo bài với Model: {model}...")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={current_key}"
                body = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "responseMimeType": "application/json"
                    }
                }
                if '2.5' in model:
                    body["generationConfig"]["thinkingConfig"] = {"thinkingBudget": 0}

                resp = requests.post(url, json=body, timeout=90)

                # Kiểm tra quá tải hoặc hết quota để đổi key dự phòng ngay
                if resp.status_code == 429 or "RESOURCE_EXHAUSTED" in resp.text:
                    print(f"⚠️ API Key #{key_idx} gặp sự cố quá tải / hết lượt gọi (HTTP 429 / Quota Exceeded).")
                    key_overloaded = True
                    break  # Thoát loop model để nhảy sang key dự phòng tiếp theo ngay lập tức

                if resp.status_code != 200:
                    raise Exception(f"HTTP {resp.status_code}: {resp.text}")

                res_json = resp.json()
                raw_text = res_json['candidates'][0]['content']['parts'][0]['text']

                # Clean json
                cleaned = raw_text.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()

                data = json.loads(cleaned)
                print(f"✅ Gemini AI đã tạo xong bài viết: '{data.get('title')}' thành công với Key #{key_idx} ({model})!")
                return data
            except Exception as e:
                last_err = e
                print(f"⚠️ Model {model} gặp sự cố: {e}. Đang thử model kế tiếp...")

        if key_overloaded and key_idx < len(api_keys):
            print(f"🔄 Tự động chuyển sang API Key dự phòng #{key_idx + 1}...")

    raise last_err or Exception("Tất cả các API Key trong pool đều bị lỗi hoặc quá tải!")

# ==============================================================================
# HÀM XÁC THỰC VÀ ĐĂNG BÀI QUA BLOGGER API V3
# ==============================================================================
def get_blogger_service():
    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET and GOOGLE_REFRESH_TOKEN):
        raise Exception("Thiếu thông tin Google OAuth (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)!")

    print(f"🔍 Kiểm tra định dạng Google OAuth:")
    print(f"   - Client ID: {GOOGLE_CLIENT_ID[:12]}...{GOOGLE_CLIENT_ID[-15:]} (Độ dài: {len(GOOGLE_CLIENT_ID)})")
    print(f"   - Client Secret: {GOOGLE_CLIENT_SECRET[:6]}... (Độ dài: {len(GOOGLE_CLIENT_SECRET)})")
    print(f"   - Refresh Token: {GOOGLE_REFRESH_TOKEN[:8]}... (Độ dài: {len(GOOGLE_REFRESH_TOKEN)})")

    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET
    )

    service = build('blogger', 'v3', credentials=creds, cache_discovery=False)
    return service

def post_to_blogger(service, article, original_labels):
    print(f"\n🚀 Đang gửi bài viết lên Blogger Blog ID: {BLOGGER_BLOG_ID}...")

    # Labels
    post_labels = article.get('labels') or original_labels
    if isinstance(post_labels, str):
        post_labels = [l.strip() for l in post_labels.split(',') if l.strip()]

    post_body = {
        'kind': 'blogger#post',
        'title': article['title'],
        'content': article['content'],
        'labels': post_labels
    }

    # Handling schedule
    is_draft = (POST_MODE == 'draft')
    if POST_MODE == 'schedule':
        # Calculate future published datetime in ISO format (UTC)
        scheduled_dt = datetime.now(timezone.utc) + timedelta(hours=SCHEDULE_HOURS_AHEAD)
        post_body['published'] = scheduled_dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        print(f"⏰ Chế độ hẹn giờ: Bài viết sẽ tự động xuất bản vào lúc: {scheduled_dt.strftime('%d/%m/%Y %H:%M UTC')}")

    request = service.posts().insert(
        blogId=BLOGGER_BLOG_ID,
        body=post_body,
        isDraft=is_draft
    )
    result = request.execute()
    post_url = result.get('url') or f"https://www.blogger.com/blog/post/edit/{BLOGGER_BLOG_ID}/{result.get('id')}"
    print(f"🎉 ĐĂNG BÀI THÀNH CÔNG LÊN BLOGGER!")
    print(f"📌 Tiêu đề: {result.get('title')}")
    print(f"🔗 Link bài: {post_url}")
    return result

# ==============================================================================
# HÀM QUẢN LÝ DANH SÁCH BÀI & LỊCH SỬ
# ==============================================================================
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_updated": None, "total_posted": 0, "history": []}

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_next_topic():
    if not os.path.exists(TOPICS_FILE):
        raise Exception(f"Không tìm thấy file danh sách đề tài: {TOPICS_FILE}")

    with open(TOPICS_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    history = load_history()
    posted_topics = set(item['topic'].lower() for item in history.get('history', []))

    for line in lines:
        parts = [p.strip() for p in line.split('|')]
        raw_topic = parts[0]
        summary = ''
        labels = ['AILADI Platform', 'Kinh Doanh Online']
        cta_url = REGISTER_URL

        if len(parts) == 2:
            # Format: Tiêu đề | Nhãn 1, Nhãn 2
            labels = [l.strip() for l in parts[1].split(',') if l.strip()]
        elif len(parts) >= 3:
            # Format: Tiêu đề | Tóm tắt gợi ý | Link CTA (hoặc Nhãn)
            summary = parts[1]
            if parts[2].startswith('http'):
                cta_url = parts[2]
            else:
                labels = [l.strip() for l in parts[2].split(',') if l.strip()]
            if len(parts) >= 4:
                if parts[3].startswith('http'):
                    cta_url = parts[3]
                elif parts[3]:
                    labels = [l.strip() for l in parts[3].split(',') if l.strip()]

        if raw_topic.lower() not in posted_topics:
            return raw_topic, labels, summary, cta_url, history

    return None, None, '', REGISTER_URL, history

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    print("=" * 65)
    print("🤖 BLOGGER GEMINI AI CLOUD AUTO-POSTER (GITHUB ACTIONS)")
    print(f"⏰ Thời gian chạy: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 65)

    api_keys = get_api_key_pool()
    if not api_keys:
        print("❌ Lỗi: Thiếu biến môi trường GEMINI_API_KEY (hoặc GEMINI_API_KEYS)!")
        sys.exit(1)
    print(f"🔑 Tìm thấy {len(api_keys)} Gemini API Key sẵn sàng trong Pool.")
    if not BLOGGER_BLOG_ID:
        print("❌ Lỗi: Thiếu biến môi trường BLOGGER_BLOG_ID!")
        sys.exit(1)

    # 1. Tìm đề tài chưa đăng
    topic, labels, summary, cta_url, history = get_next_topic()
    if not topic:
        print("ℹ️ Tất cả đề tài trong topics.txt đều đã được đăng bài!")
        print("💡 Hãy thêm các đề tài mới vào file topics.txt để hệ thống tiếp tục chạy.")
        return

    print(f"\n📝 Đề tài tiếp theo trong hàng đợi: '{topic}'")
    print(f"🏷️ Nhãn chuyên mục: {', '.join(labels)}")
    if summary:
        print(f"💡 Góc nhìn gợi ý: {summary}")
    print(f"🎯 Link đích chuyển đổi: {cta_url}")

    # 2. Sinh bài viết chuẩn SEO bằng Gemini AI
    article = generate_seo_article(topic, labels, summary=summary, cta_url=cta_url)

    # 3. Kết nối Blogger API và đăng/lên lịch bài viết
    service = get_blogger_service()
    result = post_to_blogger(service, article, labels)

    # 4. Ghi nhận lịch sử
    history_entry = {
        "topic": topic,
        "title": result.get('title'),
        "post_id": result.get('id'),
        "url": result.get('url'),
        "published": result.get('published'),
        "posted_at": datetime.now(timezone.utc).isoformat(),
        "mode": POST_MODE
    }
    history['history'].append(history_entry)
    history['total_posted'] = len(history['history'])
    history['last_updated'] = datetime.now(timezone.utc).isoformat()
    save_history(history)

    print(f"\n💾 Đã lưu lịch sử đăng bài vào posted_history.json. Tổng cộng đã đăng: {history['total_posted']} bài.")
    print("=" * 65)
    print("🎉 HOÀN THÀNH TIẾN TRÌNH TỰ ĐỘNG HÓA THÀNH CÔNG!")
    print("=" * 65)

if __name__ == '__main__':
    main()
