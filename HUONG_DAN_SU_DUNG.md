# 📘 CẨM NANG HƯỚNG DẪN SỬ DỤNG BLOGGER AI STUDIO PRO
### Hệ Thống Tự Động Hóa Viết Bài & Thiết Kế Trang Blogger - LuViet Suite
**Thư mục cài đặt:** `D:\BloggerAIStudio\`

---

## 📁 1. Cấu Trúc Thư Mục Hệ Thống
```
D:\BloggerAIStudio\
├── run.bat                          <-- File chạy nhanh bằng 1 click chuột
├── start.py                         <-- Script khởi động server & tự mở trình duyệt
├── server.py                        <-- Backend API FastAPI (Cổng 8888)
├── templates.py                     <-- Bộ sinh mã HTML chuẩn Blogger & linh kiện LuViet
├── blogger_automation.py            <-- Bộ điều khiển tự động hóa Chrome qua CDP (Port 9222)
├── requirements.txt                 <-- Danh sách thư viện Python cần thiết
├── HUONG_DAN_SU_DUNG.md             <-- Tài liệu hướng dẫn sử dụng (File này)
├── README.md                        <-- Giới thiệu tính năng phần mềm
│
├── static\                          <-- Giao diện Web Dashboard hiện đại
│   ├── index.html                   <-- Cấu trúc giao diện
│   ├── index.css                    <-- Giao diện Dark mode & gradient LuViet
│   └── app.js                       <-- Bộ xử lý tương tác trực tiếp
│
├── pages_backup\                    <-- Lưu trữ các trang chuẩn SEO đã hoàn thành
│   ├── trang-1-he-thong-tu-dong-hoa-blogger-ai.html
│   ├── trang-2-huong-dan-thiet-ke-website-wordpress.html
│   ├── trang-3-cach-tro-ten-mien.html
│   ├── trang-4-dich-vu-thiet-ke-website-ban-hang.html
│   ├── trang-5-huong-dan-tai-ve.html
│   └── thiet-ke-website-tron-goi.html
│
└── theme_backup\                    <-- File giao diện Blogger đã fix lỗi menu
    ├── theme-1444221897689962852 (3).xml      (Đã sửa lỗi icon & submenu)
    └── theme-1444221897689962852 (3).xml.bak  (Bản gốc lưu trữ dự phòng)
```

---

## 🚀 2. Cách Khởi Động Công Cụ Nhanh Chóng

### Cách 1: Chạy bằng file `run.bat` (Khuyên dùng)
- Mở thư mục `D:\BloggerAIStudio\`.
- Click đúp chuột vào file **`run.bat`**.
- Màn hình đen Terminal sẽ chạy và tự động mở trình duyệt Chrome tại địa chỉ:
  👉 **`http://127.0.0.1:8888`**

### Cách 2: Chạy qua Command Prompt hoặc PowerShell
Mở terminal và gõ 2 lệnh sau:
```bash
cd D:\BloggerAIStudio
python start.py
```

---

## 🎯 3. Hướng Dẫn Sử Dụng Chi Tiết Từng Tính Năng

### 3.1. Tạo Trang Hoặc Bài Viết Mới Bằng AI
1. Ở cột bên trái, chọn tab **"Cấu Hình & Sinh Mã AI"**:
   - **Mục tiêu xuất bản**: Chọn *Trang Tĩnh (Page)* hoặc *Bài Đăng Mới (Post)*.
   - **Loại hình nội dung**:
     - *Trang Dịch Vụ Trọn Gói*: Dành cho các dịch vụ thiết kế web, hosting, content.
     - *Trang Website Bán Hàng E-Commerce*: Bố cục tối ưu tỷ lệ chuyển đổi cao (CRO), bảng so sánh giá.
     - *Cẩm Nang Hướng Dẫn Kỹ Thuật*: Dành cho các bài hướng dẫn trỏ tên miền, cài đặt WordPress...
     - *Bài Viết Chia Sẻ Chuẩn SEO*: Dành cho các bài blog kiến thức marketing.
   - **Tiêu đề bài viết**: Nhập tiêu đề bạn mong muốn.
   - **Từ khóa SEO**: Nhập các từ khóa chính, ngăn cách bằng dấu phẩy.
2. Bấm nút màu tím nổi bật: **"Tự Động Sinh Mã Giao Diện Chuẩn LuViet"**.
3. Hệ thống sẽ tự động tạo mã HTML chuẩn Blogger, tự chèn Schema JSON-LD và tạo lưới liên kết nội bộ 3 cột.

### 3.2. Chỉnh Sửa Trực Tiếp & Thư Viện Linh Kiện
- **Tab "Mã HTML Trực Tiếp"**: Bạn có thể sửa trực tiếp bất kỳ đoạn văn, hình ảnh hay đường dẫn nào trong mã HTML. Cột bên phải sẽ tự động làm mới ngay lập tức.
- **Tab "Thư Viện Linh Kiện"**: Cho phép chèn nhanh các khối thành phần chuẩn vào bài:
  - 🏷️ **Bảng Giá 3 Gói**: Khởi Nghiệp, Chuyên Nghiệp, Doanh Nghiệp VIP.
  - 💳 **Khung Thanh Toán Vietcombank**: Hiển thị STK `0121000679358`, Tran Minh Thuan, Vietcombank Đồng Nai.
  - 🔢 **Quy Trình 4-5 Bước**: Đánh số vòng tròn gradient.
  - ❓ **Bảng Câu Hỏi Thường Gặp (FAQ)**: Accordion bấm đóng/mở mượt mà.
  - 🌐 **Lưới Liên Kết Nội Bộ SEO**: Ma trận link 3 cột giúp tăng thứ hạng website.
  - 📞 **Banner Kêu Gọi Hành Động (CTA)**: Nút Zalo `0914.878.680` & Hotline.

### 3.3. Xem Trước Đa Thiết Bị (Live Responsive Preview)
Ở góc trên bên phải khung xem trước, bạn có 3 nút chuyển chế độ:
- 🖥️ **Desktop**: Xem giao diện hiển thị trên màn hình máy tính (100% full width).
- 📱 **Tablet**: Xem giao diện thu nhỏ đúng chuẩn máy tính bảng (768px).
- 📲 **Mobile**: Xem giao diện trên điện thoại di động (375px) để kiểm tra các nút bấm chạm và độ mượt của thẻ.

### 3.4. Đẩy Trực Tiếp Lên Blogger Qua Chrome (1-Click Push)
- Khi góc trên hiển thị chấm tròn màu xanh **`Chrome Đã Kết Nối`**, công cụ đã liên kết với trình duyệt Chrome của bạn.
- **Để cập nhật vào trang/bài có sẵn**:
  1. Bấm nút **"Quản Lý Trang & Bài Viết"** trên thanh menu.
  2. Bảng danh sách toàn bộ các trang và bài viết trên blog của bạn sẽ hiện ra.
  3. Chọn bài viết cần thay đổi giao diện và bấm **"Cập Nhật Trang Này"**.
- **Để đăng một trang mới hoàn toàn**:
  - Chọn mục tiêu là *Trang Tĩnh (Page)* hoặc *Bài Đăng (Post)* ở tab Cấu hình, sau đó bấm nút tím **"Đẩy Lên Blogger"**.
  - Hệ thống sẽ tự động mở trang soạn thảo, nạp mã vào CodeMirror, điền tiêu đề, điền mô tả tìm kiếm và bấm xuất bản!

### 3.5. Lưu File HTML Xuống Máy Tính
- Bấm nút **"Lưu File HTML"** trên thanh menu trên cùng.
- Nhập tên file mong muốn. File sẽ được lưu tự động vào thư mục `C:\Users\Admin\Downloads\` hoặc thư mục bạn chỉ định.

---

## 🎨 4. Hướng Dẫn Tải File Theme Đã Fix Lỗi Menu Lên Blogger
File theme đã xử lý xong lỗi thừa icon và trùng submenu nằm tại:  
📁 `D:\BloggerAIStudio\theme_backup\theme-1444221897689962852 (3).xml`

**Các bước áp dụng lên Blogger:**
1. Mở trang quản trị Blogger: [https://www.blogger.com](https://www.blogger.com).
2. Ở cột bên trái, bấm vào mục **Chủ đề** (Theme).
3. Bấm vào nút **Tùy chỉnh** có dấu mũi tên chỉ xuống ⌄ cạnh nút Tùy chỉnh (Customize).
4. Chọn **Khôi phục** (Restore) ➔ Bấm **Tải lên** (Upload).
5. Tìm và chọn file `D:\BloggerAIStudio\theme_backup\theme-1444221897689962852 (3).xml`.
6. Chờ khoảng 5 giây để Blogger lưu lại. Menu của website `luviet.com` sẽ hiển thị chuẩn xác không còn lỗi icon thừa!

---

## 💡 5. Mẹo Đảm Bảo Kết Nối Chrome CDP Luôn Ổn Định
Để công cụ luôn có thể tương tác tự động với Blogger, bạn chỉ cần khởi động Chrome có cờ remote debugging (như hiện tại máy bạn đang chạy sẵn):
```powershell
chrome.exe --remote-debugging-port=9222
```
Nếu tình cờ Chrome bị tắt hết, bạn chỉ cần mở lại Chrome với cờ trên, đăng nhập Blogger là công cụ sẽ tự động nhận diện lại ngay lập tức!
