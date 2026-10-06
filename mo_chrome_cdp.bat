@echo off
title Blogger AI Studio Pro - Khoi Dong Chrome CDP (Port 9222)
chcp 65001 >nul
echo ========================================================
echo   🚀 KHOI DONG GOOGLE CHROME DEBUGGING (PORT 9222)
echo   Dung cho Blogger AI Studio Pro - LuViet Automation
echo ========================================================
echo.
echo Chon che do khoi dong:
echo   [1] Khoi dong Chrome profile rieng (Khuyen dung - Khong anh huong cac tab dang mo)
echo   [2] Khoi dong lai Chrome chinh (Giu nguyen tai khoan Google dang dang nhap)
echo.
set /p opt="Nhap lua chon [1 hoac 2, mac dinh 1]: "

if "%opt%"=="2" goto restart_main

:profile_mode
echo.
echo Dang khoi dong Chrome voi profile rieng tren cong 9222...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\BloggerStudioProfile" --no-first-run --no-default-browser-check "https://www.blogger.com/blog/pages/1444221897689962852" "http://127.0.0.1:8888"
goto done

:restart_main
echo.
echo Dang dong cac cua so Chrome hien tai va bat lai voi cong 9222...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 1 >nul
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 "https://www.blogger.com/blog/pages/1444221897689962852" "http://127.0.0.1:8888"
goto done

:done
echo.
echo [OK] Chrome da duoc bat tren cong 9222!
echo Truy cap Blogger AI Studio tai: http://127.0.0.1:8888
timeout /t 3 >nul
