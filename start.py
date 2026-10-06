"""
start.py - Khởi động Blogger AI Studio Pro & Tự động mở trình duyệt
"""

import webbrowser
import threading
import time
import uvicorn
import os

def open_browser():
    time.sleep(1.5)
    print("Mở giao diện Blogger AI Studio Pro trên trình duyệt...")
    webbrowser.open("http://127.0.0.1:8888")

if __name__ == "__main__":
    print("=" * 60)
    print("  🚀 KHỞI ĐỘNG BLOGGER AI STUDIO PRO")
    print("  Hệ thống tự động hóa viết bài & thiết kế trang LuViet")
    print("  Địa chỉ: http://127.0.0.1:8888")
    print("=" * 60)
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run uvicorn server
    uvicorn.run("server:app", host="127.0.0.1", port=8888, reload=False)
