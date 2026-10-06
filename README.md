# 🚀 Blogger AI Studio Pro & Cloud Auto-Poster (LuViet Suite)

Hệ thống toàn diện kết hợp **Studio Thiết Kế Trực Quan Cục Bộ (Local Web App)** và **Cỗ Máy Tự Động Hóa Đám Mây 24/7 (GitHub Actions)** dành cho Blogger LuViet.

---

## 🌟 1. Blogger AI Studio Pro (Local Web App & Chrome CDP)

Ứng dụng web chạy trực tiếp trên máy tính (`http://127.0.0.1:8888`), hỗ trợ biên tập nội dung, xem trước đa thiết bị và đẩy trực tiếp lên Blogger qua Chrome DevTools Protocol (Port 9222).

### ✨ Tính Năng Nổi Bật:
1. **Bộ Sinh Giao Diện & Nội Dung AI Chuẩn LuViet**:
   - Sinh mã HTML hoàn chỉnh chuẩn bài đăng Blogger (Pure Post Body, tối ưu thẻ semantic).
   - Tông màu gradient thương hiệu: `linear-gradient(135deg, #6d3990 0%, #d43434 50%, #032690 100%)`.
   - Đa dạng thể loại: Trang Dịch Vụ, Trang Bán Hàng E-Commerce CRO, Cẩm Nang Kỹ Thuật, Bài Viết Blog SEO.
   - Tự động chèn **Schema JSON-LD** và **Ma Trận Liên Kết Nội Bộ 3 Cột (Internal Links Grid)**.
2. **Khung Xem Trước Trực Quan Đa Thiết Bị (Live Multi-Device Preview)**:
   - Tự động cập nhật real-time khi gõ code.
   - Chuyển đổi linh hoạt: **Desktop (100%)**, **Tablet (768px)**, **Mobile (375px)**.
3. **Thư Viện Linh Kiện 1-Click (Component Builder)**:
   - Bảng giá 3 gói (Khởi Nghiệp, Chuyên Nghiệp, VIP).
   - Khung thanh toán Vietcombank + VietQR (`TRAN MINH THUAN - 0121000679358`).
   - Quy trình 4 bước đánh số gradient.
   - Bảng FAQ Accordion đóng/mở mượt mà.
   - Banner CTA chốt khách (Zalo Hotline `0914.878.680`).
4. **Đồng Bộ Trực Tiếp Lên Blogger Qua Chrome CDP (Port 9222)**:
   - Tự động kết nối phiên đăng nhập Chrome, nạp mã vào CodeMirror, điền tiêu đề, Search Description, Labels và xuất bản.
   - Không cần cấu hình Google Cloud API phức tạp.
   - Hỗ trợ nút **Mở Chrome CDP** trực tiếp từ Dashboard hoặc qua file `mo_chrome_cdp.bat`.

### 🚀 Cách Khởi Động Nhanh:
1. **Khởi động Server Studio**: Click đúp vào `run.bat` hoặc:
   ```bash
   python start.py
   ```
   Trình duyệt sẽ mở tại: `http://127.0.0.1:8888`.
2. **Khởi động Chrome CDP (Port 9222)**:
   - Bấm nút **"Mở Chrome CDP"** ngay trên thanh Menu của Studio, HOẶC:
   - Click đúp vào `mo_chrome_cdp.bat` (chọn [1] để mở profile riêng biệt không ảnh hưởng tab đang làm việc).

---

## ☁️ 2. Blogger Gemini AI Auto-Poster Cloud (GitHub Actions 24/7)

Hệ thống tự động hóa viết bài chuẩn SEO và đăng lên Blogger.com hoàn toàn tự động trên nền tảng đám mây **GitHub Actions 24/7**.

### ⚡ Ưu Điểm:
- **100% Miễn phí trọn đời** (2.000 phút/tháng từ GitHub Actions).
- **Hoạt động ngầm trên mây**: Không cần mở máy tính, hệ thống tự động thức dậy theo lịch hẹn để đăng bài.
- **Đồng bộ kế hoạch Google Sheets**: Tự động đọc danh sách bài từ Google Sheets hoặc file `topics.txt`.
- **Chống trùng lặp**: Lưu vết các bài đã đăng vào `posted_history.json`.

### 🔑 Các Biến Cấu Hình (GitHub Repository Secrets):
Vào **Settings** ➔ **Secrets and variables** ➔ **Actions** và thêm:
- `GEMINI_API_KEY`: Khóa Google Gemini AI ([aistudio.google.com](https://aistudio.google.com/app/apikey)).
- `BLOGGER_BLOG_ID`: ID blog Blogger (mặc định: `1444221897689962852`).
- `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET`: OAuth2 Credentials từ Google Cloud Console.
- `GOOGLE_REFRESH_TOKEN`: Chạy `python get_refresh_token.py` trên máy tính để lấy mã vĩnh viễn.
- `GOOGLE_SHEET_URL`: Link Google Sheets kế hoạch bài viết (chia sẻ quyền công khai xem).
- `GOOGLE_SHEET_WEBHOOK_URL`: (Tùy chọn) Webhook Apps Script đồng bộ trạng thái.

---

## 📁 3. Cấu Trúc Thư Mục Dự Án

```text
blogger-auto-cloud/
├── .github/workflows/
│   └── auto_post.yml         # Lịch trình chạy tự động trên GitHub Actions
│
├── server.py                 # Backend FastAPI của Blogger AI Studio Pro (Cổng 8888)
├── start.py                  # Script khởi động server & tự mở trình duyệt
├── run.bat                   # 1-Click khởi động Blogger AI Studio Pro
├── mo_chrome_cdp.bat         # 1-Click khởi động Chrome chế độ DevTools (Port 9222)
├── templates.py              # Bộ sinh mã HTML chuẩn SEO & linh kiện LuViet
├── blogger_automation.py     # Bộ điều khiển Playwright CDP tương tác Blogger
├── static/                   # Giao diện Web Dashboard (HTML, CSS, JS, Favicon)
│   ├── index.html
│   ├── index.css
│   ├── app.js
│   └── favicon.svg
│
├── main.py                   # Script tự động hóa đám mây (Gemini AI + Blogger API)
├── google_indexer.py         # Tự động gửi URL lên Google Indexing API
├── get_refresh_token.py      # Tiện ích lấy Google OAuth2 Refresh Token
├── Ke_Hoach_Bai_Viet_...xlsx # Bảng kế hoạch bài viết chi tiết
├── topics.txt                # Danh sách đề tài dự phòng
├── posted_history.json       # Lịch sử bài viết đã xuất bản
├── pages_backup/             # Bản sao lưu các trang tĩnh chuẩn SEO
├── theme_backup/             # Bản sao lưu theme Blogger đã sửa lỗi menu
├── requirements.txt          # Danh sách thư viện Python
└── README.md                 # Tài liệu hướng dẫn sử dụng này
```

---

## 📞 Hỗ Trợ Kỹ Thuật
- **Đơn vị phát triển**: LuViet Solution Suite
- **Hotline / Zalo**: `0914.878.680`
- **Chủ sở hữu**: Trần Minh Thuận (`thuantranblog@gmail.com`)
