"""
blogger_automation.py - Playwright CDP Controller for Blogger
Tự động hóa giao tiếp trực tiếp với phiên đăng nhập Blogger trên Chrome qua CDP (Port 9222).
Không cần cấu hình Google Cloud API hay OAuth phức tạp.
"""

from playwright.sync_api import sync_playwright
import time
import urllib.request
import json
import socket
import os
import subprocess

def is_port_open(host="127.0.0.1", port=9222, timeout=0.25):
    """Kiểm tra nhanh cổng có đang mở không bằng socket (tránh bị treo 2s khi gọi urlopen)"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def is_cdp_available(port=9222):
    """Kiểm tra CDP endpoint của Chrome trên port chỉ định"""
    if not is_port_open("127.0.0.1", port):
        return False, f"Cổng Chrome CDP ({port}) chưa được kích hoạt."
    try:
        url = f"http://127.0.0.1:{port}/json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return True, data
    except Exception as e:
        return False, str(e)

def find_chrome_path():
    """Tự động tìm kiếm đường dẫn chrome.exe trên máy Windows"""
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def launch_chrome_cdp(mode="profile", port=9222, target_url="https://www.blogger.com/blog/pages/1444221897689962852"):
    """
    Khởi động Chrome với cờ CDP --remote-debugging-port
    - mode='profile': Khởi chạy với thư mục profile riêng biệt (hoạt động ngay kể cả khi Chrome thông thường đang mở nhiều tab)
    - mode='restart': Đóng Chrome hiện tại và khởi động lại với port 9222 (dùng lại tài khoản Google đã đăng nhập)
    """
    chrome_path = find_chrome_path()
    if not chrome_path:
        return {"success": False, "error": "Không tìm thấy file chrome.exe trên hệ thống. Vui lòng cài đặt Google Chrome."}

    try:
        if mode == "restart":
            # Đóng tất cả process chrome đang chạy để mở lại với port 9222 bằng default profile
            subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
            time.sleep(1.5)
            cmd = [
                chrome_path,
                f"--remote-debugging-port={port}",
                target_url
            ]
            subprocess.Popen(cmd)
        else:
            # Nếu port đã mở sẵn ở profile riêng
            if is_port_open("127.0.0.1", port):
                return {"success": True, "message": f"Chrome CDP đã sẵn sàng trên cổng {port}."}

            profile_dir = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\BloggerStudioProfile")
            os.makedirs(profile_dir, exist_ok=True)
            cmd = [
                chrome_path,
                f"--remote-debugging-port={port}",
                f"--user-data-dir={profile_dir}",
                "--no-first-run",
                "--no-default-browser-check",
                target_url
            ]
            subprocess.Popen(cmd)

        # Chờ tối đa 5 giây để port sẵn sàng
        for _ in range(10):
            time.sleep(0.5)
            if is_port_open("127.0.0.1", port):
                return {
                    "success": True,
                    "message": f"Khởi động Chrome CDP thành công trên cổng {port}!",
                    "mode": mode
                }

        return {
            "success": True,
            "message": f"Đã gửi lệnh khởi động Chrome trên cổng {port}. Vui lòng kiểm tra cửa sổ trình duyệt.",
            "mode": mode
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_active_browser_info(port=9222):
    ok, data = is_cdp_available(port)
    if not ok:
        return {"connected": False, "error": data}
    
    blogger_tabs = []
    need_login = False
    if isinstance(data, list):
        for item in data:
            url = item.get("url", "")
            title = item.get("title", "")
            if "accounts.google.com" in url or "ServiceLogin" in url:
                need_login = True
            if "blogger.com" in url or "luviet.com" in url or "accounts.google.com" in url:
                blogger_tabs.append({"id": item.get("id"), "title": title, "url": url})
            
    return {
        "connected": True,
        "need_login": need_login,
        "total_tabs": len(data) if isinstance(data, list) else 0,
        "blogger_tabs": blogger_tabs
    }

def get_items_list(blog_id="1444221897689962852", item_type="pages", port=9222):
    """
    Lấy danh sách các trang (pages) hoặc bài viết (posts) từ Blogger
    """
    ok, err = is_cdp_available(port)
    if not ok:
        return {
            "success": False,
            "cdp_offline": True,
            "error": "Chrome CDP (port 9222) chưa sẵn sàng. Vui lòng bấm 'Khởi Động Chrome CDP' hoặc chạy mo_chrome_cdp.bat.",
            "items": []
        }

    target_url = f"https://www.blogger.com/blog/{item_type}/{blog_id}"

    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
            context = browser.contexts[0]
            
            # Ưu tiên tái sử dụng tab Blogger hoặc tab đăng nhập đang mở
            page = None
            for p_tab in context.pages:
                u = p_tab.url
                if f"/blog/{item_type}/{blog_id}" in u or "blogger.com" in u or "accounts.google.com" in u:
                    page = p_tab
                    break
            if not page:
                page = context.pages[0] if context.pages else context.new_page()

            # Điều hướng đến target_url nếu chưa ở đó
            if target_url not in page.url:
                page.goto(target_url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(2)

            # Kiểm tra trạng thái đăng nhập hoặc chờ bảng danh sách tải (tối đa 10 giây)
            for _ in range(12):
                current_url = page.url
                if "accounts.google.com" in current_url or "ServiceLogin" in current_url or "signin/identifier" in current_url:
                    return {
                        "success": False,
                        "need_login": True,
                        "error": "Cửa sổ Chrome chưa đăng nhập tài khoản Google. Vui lòng chuyển sang cửa sổ Chrome đang mở và đăng nhập vào tài khoản Blogger của bạn, sau đó bấm 'Thử Lại'.",
                        "items": []
                    }
                
                # Kiểm tra xem danh sách đã xuất hiện trong DOM chưa
                has_items = page.evaluate('''([itemType]) => {
                    const selector = `a[href*="/${itemType === 'pages' ? 'page' : 'post'}/edit/"], a[href*="/edit/"]`;
                    return document.querySelectorAll(selector).length > 0;
                }''', [item_type])
                
                if has_items:
                    break
                time.sleep(0.8)

            # Lần kiểm tra cuối cùng xem có bị redirect sang login không
            if "accounts.google.com" in page.url or "ServiceLogin" in page.url:
                return {
                    "success": False,
                    "need_login": True,
                    "error": "Cửa sổ Chrome chưa đăng nhập tài khoản Google. Vui lòng chuyển sang cửa sổ Chrome đang mở và đăng nhập vào tài khoản Blogger của bạn, sau đó bấm 'Thử Lại'.",
                    "items": []
                }

            # Trích xuất dữ liệu bài viết / trang
            items = page.evaluate('''([itemType]) => {
                const results = [];
                const editRegex = new RegExp(`/(page|post)/edit/\\\\d+/(\\\\d+)`);
                const selector = `a[href*="/${itemType === 'pages' ? 'page' : 'post'}/edit/"], a[href*="/edit/"]`;
                const editLinks = document.querySelectorAll(selector);
                
                editLinks.forEach(a => {
                    const href = a.getAttribute('href') || a.href || '';
                    const m = href.match(editRegex);
                    if (m && m[2]) {
                        const id = m[2];
                        let title = a.innerText.trim();
                        if (!title) {
                            const row = a.closest('div[role="row"]') || a.closest('.IL5y5c') || a.closest('.W4rOsd') || a.parentElement;
                            if (row) {
                                const titleEl = row.querySelector('.W4rOsd, [data-title], [role="heading"]') || row;
                                title = titleEl.innerText.split('\\n')[0].trim();
                            }
                        }
                        if (!title) title = `(Mục ID: ${id})`;
                        if (!results.some(r => r.id === id)) {
                            results.push({ id, title, href });
                        }
                    }
                });
                return results;
            }''', [item_type])

            return {"success": True, "count": len(items), "items": items}
        except Exception as e:
            return {"success": False, "error": str(e), "items": []}

def push_to_blogger(blog_id="1444221897689962852", target_type="page", target_id=None, title="", content_html="", search_desc="", labels=None, port=9222):
    """
    Đăng bài mới hoặc cập nhật trang/bài hiện có trên Blogger.
    target_type: 'page' | 'post'
    target_id: None (tạo mới) hoặc chuỗi số ID (cập nhật bài cũ)
    """
    ok, _ = is_cdp_available(port)
    if not ok:
        return {
            "success": False,
            "cdp_offline": True,
            "error": "Chrome CDP (port 9222) chưa sẵn sàng. Vui lòng khởi động Chrome CDP trước khi đăng bài."
        }

    if target_id:
        edit_url = f"https://www.blogger.com/blog/{target_type}/edit/{blog_id}/{target_id}"
    else:
        edit_url = f"https://www.blogger.com/blog/{target_type}/edit/{blog_id}"

    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
            context = browser.contexts[0]
            
            page = None
            for p_tab in context.pages:
                if f"/blog/{target_type}/" in p_tab.url or "blogger.com" in p_tab.url or "accounts.google.com" in p_tab.url:
                    page = p_tab
                    break
            if not page:
                page = context.pages[0] if context.pages else context.new_page()

            page.goto(edit_url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(2.5)

            # Kiểm tra xem có bị bắt đăng nhập không
            if "accounts.google.com" in page.url or "ServiceLogin" in page.url:
                return {
                    "success": False,
                    "need_login": True,
                    "error": "Cửa sổ Chrome chưa đăng nhập tài khoản Google. Vui lòng đăng nhập Blogger trên Chrome trước khi đăng bài."
                }

            # 1. Update Title
            if title:
                title_inp = page.locator('input[aria-label="Tiêu đề"]')
                if title_inp.is_visible():
                    title_inp.fill(title)

            # 2. Check HTML mode vs Compose mode
            is_html_mode = page.evaluate('() => !!document.querySelector(".CodeMirror")')
            if not is_html_mode:
                view_mode_btn = page.locator('div[aria-label="Chế độ xem Soạn thảo"], div[aria-label="Chế độ xem HTML"], div[jsname="xw1cm"][aria-haspopup="menu"]').first
                if view_mode_btn.is_visible():
                    view_mode_btn.click()
                    time.sleep(0.8)
                    html_option = page.locator('div[role="menuitem"]:has-text("Chế độ xem HTML")').first
                    if html_option.is_visible():
                        html_option.click()
                        time.sleep(1)

            # 3. Inject Content into CodeMirror
            cm_res = page.evaluate('''([html]) => {
                const cm = document.querySelector(".CodeMirror")?.CodeMirror;
                if (cm) {
                    cm.setValue(html);
                    cm.save();
                    return true;
                }
                return false;
            }''', [content_html])

            if not cm_res:
                return {"success": False, "error": "Không tìm thấy trình biên tập HTML (CodeMirror) trên trang Blogger."}

            # 4. Search Description (Mô tả tìm kiếm - Max 150 ký tự, hỗ trợ id="c12" và dynamic controls)
            if search_desc:
                try:
                    clean_desc = search_desc.strip()[:150]
                    page.evaluate('''([desc]) => {
                        const allBtns = Array.from(document.querySelectorAll('div[jsname="HSrbLb"]'));
                        const descBtn = allBtns.find(b => b.innerText && b.innerText.includes("Mô tả tìm kiếm"));
                        if (descBtn) {
                            if (descBtn.getAttribute('aria-expanded') !== 'true') {
                                descBtn.click();
                            }
                            const regionId = descBtn.getAttribute('aria-controls') || 'c12';
                            const region = document.getElementById(regionId) || descBtn.closest('.mT05K');
                            if (region) {
                                const ta = region.querySelector('textarea');
                                if (ta) {
                                    ta.focus();
                                    ta.value = desc;
                                    ta.dispatchEvent(new Event('input', { bubbles: true }));
                                    ta.dispatchEvent(new Event('change', { bubbles: true }));
                                    ta.blur();
                                    return true;
                                }
                            }
                        }
                        const fallbackTa = document.querySelector('textarea[aria-label*="mô tả tìm kiếm" i], textarea[aria-label*="Mô tả tìm kiếm"]');
                        if (fallbackTa) {
                            fallbackTa.focus();
                            fallbackTa.value = desc;
                            fallbackTa.dispatchEvent(new Event('input', { bubbles: true }));
                            fallbackTa.dispatchEvent(new Event('change', { bubbles: true }));
                            fallbackTa.blur();
                            return true;
                        }
                        return false;
                    }''', [clean_desc])
                except Exception as e:
                    print("Lỗi điền search_desc:", e)

            # 5. Labels (Nhãn bài viết - Hỗ trợ id="c8" và textarea[aria-label="Phân tách các nhãn bằng dấu phẩy"])
            if target_type == 'post' and labels:
                try:
                    labels_str = ", ".join(labels) if isinstance(labels, list) else str(labels)
                    page.evaluate('''([lblText]) => {
                        const allBtns = Array.from(document.querySelectorAll('div[jsname="HSrbLb"]'));
                        const lblBtn = allBtns.find(b => b.innerText && b.innerText.includes("Nhãn"));
                        if (lblBtn) {
                            if (lblBtn.getAttribute('aria-expanded') !== 'true') {
                                lblBtn.click();
                            }
                            const regionId = lblBtn.getAttribute('aria-controls') || 'c8';
                            const region = document.getElementById(regionId) || lblBtn.closest('.mT05K');
                            if (region) {
                                const ta = region.querySelector('textarea');
                                if (ta) {
                                    ta.focus();
                                    ta.value = lblText;
                                    ta.dispatchEvent(new Event('input', { bubbles: true }));
                                    ta.dispatchEvent(new Event('change', { bubbles: true }));
                                    ta.blur();
                                    return true;
                                }
                            }
                        }
                        const fallbackTa = document.querySelector('textarea[aria-label*="dấu phẩy" i], textarea[aria-label*="Nhãn"]');
                        if (fallbackTa) {
                            fallbackTa.focus();
                            fallbackTa.value = lblText;
                            fallbackTa.dispatchEvent(new Event('input', { bubbles: true }));
                            fallbackTa.dispatchEvent(new Event('change', { bubbles: true }));
                            fallbackTa.blur();
                            return true;
                        }
                        return false;
                    }''', [labels_str])
                except Exception as e:
                    print("Lỗi điền nhãn:", e)

            time.sleep(1)

            # 6. Click "Cập nhật" or "Đăng" button
            click_res = page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('div[role="button"], button'));
                const updateBtn = btns.find(b => b.innerText && b.innerText.includes("Cập nhật"));
                if (updateBtn) {
                    updateBtn.click();
                    return "update";
                }
                const publishBtn = btns.find(b => b.innerText && b.innerText.includes("Đăng"));
                if (publishBtn) {
                    publishBtn.click();
                    return "publish";
                }
                return "none";
            }''')

            time.sleep(2)

            # Check confirmation modal if any
            page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('div[role="button"], button'));
                const confirmBtn = btns.find(b => b.innerText && b.innerText.includes("XÁC NHẬN"));
                if (confirmBtn) {
                    confirmBtn.click();
                }
            }''')

            time.sleep(3)
            return {
                "success": True,
                "action": click_res,
                "final_url": page.url,
                "target_type": target_type,
                "target_id": target_id,
                "title": title
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
