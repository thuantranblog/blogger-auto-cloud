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
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
BLOGGER_BLOG_ID = os.environ.get('BLOGGER_BLOG_ID')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_REFRESH_TOKEN = os.environ.get('GOOGLE_REFRESH_TOKEN')

# Chế độ phát hành: 'schedule' (Lên lịch tương lai), 'publish' (Đăng ngay), 'draft' (Lưu nháp)
POST_MODE = os.environ.get('POST_MODE', 'schedule').lower()
SCHEDULE_HOURS_AHEAD = int(os.environ.get('SCHEDULE_HOURS_AHEAD', '24'))

# Thông tin thương hiệu LuViet
ZALO_URL = os.environ.get('ZALO_URL', 'https://zalo.me/1501073926693571291')
FANPAGE_URL = os.environ.get('FANPAGE_URL', 'https://www.facebook.com/webluviet/')

TOPICS_FILE = os.path.join(os.path.dirname(__file__), 'topics.txt')
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'posted_history.json')

# ==============================================================================
# HÀM GỌI GEMINI AI VIẾT BÀI CHUẨN SEO
# ==============================================================================
def generate_seo_article(topic, labels):
    print(f"\n🧠 Đang gọi Google Gemini AI viết bài cho chủ đề: '{topic}'...")

    prompt = f"""
Bạn là chuyên gia Content SEO Master và Copywriter hàng đầu Việt Nam. Hãy tạo một bài viết chuẩn SEO chuyên sâu, cấu trúc chặt chẽ, tối ưu tỷ lệ chuyển đổi (CRO) bằng tiếng Việt cho Blogger/Blogspot theo các thông số sau:

- Chủ đề / Từ khóa chính: "{topic}"
- Nhãn chuyên mục mong muốn: "{', '.join(labels)}"
- Độ dài mục tiêu: Khoảng 1500 - 2000 từ.
- Tông giọng: Chuyên gia & Thuyết phục, giữ chân người đọc cao.

YÊU CẦU ĐỊNH DẠNG VÀ CẤU TRÚC (BẮT BUỘC):
1. TIÊU ĐỀ (Title): Giật tít hấp dẫn, chứa từ khóa chính ở đầu, dưới 65 ký tự, kích thích lượt click (CTR).
2. SAPO: Mở bài cuốn hút 2-3 đoạn ngắn, nêu bật nỗi đau khách hàng và giải pháp mang lại.
3. THÂN BÀI:
   - Sử dụng thẻ <h2> và <h3> rõ ràng, logic.
   - Luôn sử dụng danh sách gạch đầu dòng (<ul>, <li>) hoặc đánh số (<ol>, <li>) để nội dung thoáng mắt.
   - BẮT BUỘC có 1 Bảng so sánh (HTML <table>) rõ ràng, chuyên nghiệp với đường viền mỏng (border: 1px solid #cbd5e1).
   - BẮT BUỘC có mục <h2>Câu hỏi thường gặp (FAQ)</h2> với ít nhất 3 câu hỏi thực tế và câu trả lời súc tích.
4. KÊU GỌI HÀNH ĐỘNG (CTA - CRO):
   - Chèn khối Call To Action (CTA) thiết kế đẹp mắt với inline CSS ở cuối bài:
     + Nút Zalo OA: Link: "{ZALO_URL}" với text: "💬 Tư Vấn Miễn Phí Qua Zalo OA" (Màu nền xanh Zalo #0068ff, chữ trắng, bo góc 8px, padding 10px 18px).
     + Nút Fanpage: Link: "{FANPAGE_URL}" với text: "👍 Nhắn Tin Qua Fanpage LuViet" (Màu nền xanh Facebook #1877f2, chữ trắng, bo góc 8px, padding 10px 18px).
5. PROMPT TẠO ẢNH:
   - Viết một đoạn Prompt tiếng Anh chi tiết để tạo ảnh Thumbnail đại diện 16:9.

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

    models = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-2.5-flash']
    last_err = None

    for model in models:
        try:
            print(f"👉 Thử tạo bài với Model: {model}...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            body = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
            if '2.5' in model:
                body["generationConfig"]["thinkingConfig"] = {"thinkingBudget": 0}

            resp = requests.post(url, json=body, timeout=90)
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
            print(f"✅ Gemini AI đã tạo xong bài viết: '{data.get('title')}'")
            return data
        except Exception as e:
            last_err = e
            print(f"⚠️ Model {model} gặp sự cố: {e}. Đang thử model kế tiếp...")
            time.sleep(2)

    raise Exception(f"Không thể tạo bài viết qua tất cả các model Gemini: {last_err}")

# ==============================================================================
# HÀM XÁC THỰC VÀ ĐĂNG BÀI QUA BLOGGER API V3
# ==============================================================================
def get_blogger_service():
    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET and GOOGLE_REFRESH_TOKEN):
        raise Exception("Thiếu thông tin Google OAuth (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)!")

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
        raw_topic = line
        labels = ['Kiến Thức', 'Dịch Vụ']
        if '|' in line:
            parts = line.split('|')
            raw_topic = parts[0].strip()
            labels = [l.strip() for l in parts[1].split(',') if l.strip()]

        if raw_topic.lower() not in posted_topics:
            return raw_topic, labels, history

    return None, None, history

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    print("=" * 65)
    print("🤖 BLOGGER GEMINI AI CLOUD AUTO-POSTER (GITHUB ACTIONS)")
    print(f"⏰ Thời gian chạy: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 65)

    if not GEMINI_API_KEY:
        print("❌ Lỗi: Thiếu biến môi trường GEMINI_API_KEY!")
        sys.exit(1)
    if not BLOGGER_BLOG_ID:
        print("❌ Lỗi: Thiếu biến môi trường BLOGGER_BLOG_ID!")
        sys.exit(1)

    # 1. Tìm đề tài chưa đăng
    topic, labels, history = get_next_topic()
    if not topic:
        print("ℹ️ Tất cả đề tài trong topics.txt đều đã được đăng bài!")
        print("💡 Hãy thêm các đề tài mới vào file topics.txt để hệ thống tiếp tục chạy.")
        return

    print(f"\n📝 Đề tài tiếp theo trong hàng đợi: '{topic}'")
    print(f"🏷️ Nhãn chuyên mục: {', '.join(labels)}")

    # 2. Sinh bài viết chuẩn SEO bằng Gemini AI
    article = generate_seo_article(topic, labels)

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
