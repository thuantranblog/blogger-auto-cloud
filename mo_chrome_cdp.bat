@echo off
title Blogger AI Studio Pro - Khoi Dong Chrome CDP (Port 9222)
cls
echo ================================================================
echo    KHOI DONG GOOGLE CHROME DEBUGGING (PORT 9222)
echo    Blogger AI Studio Pro - LuViet Automation
echo ================================================================
echo.

:: 1. Tim Google Chrome chinh
set "MAIN_CHROME="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set "MAIN_CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set "MAIN_CHROME=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set "MAIN_CHROME=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
)

if not defined MAIN_CHROME (
    echo [LOI] Khong tim thay Google Chrome tren may tinh cua ban!
    pause
    exit /b 1
)

:: 2. Kiem tra port 9222 co dang hoat dong khong
netstat -ano | findstr /R /C:":9222 .*LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo [THONG BAO] Cong 9222 DANG HOAT DONG SAN SANG!
    echo.
    echo Ban co muon:
    echo   [1] Mo trang Blogger AI Studio (http://127.0.0.1:8888)
    echo   [2] Tat tien trinh cu va khoi dong lai Chrome chinh
    echo.
    set "pchoice=1"
    set /p "pchoice=Nhap lua chon [1 hoac 2, mac dinh 1]: "
    if "%pchoice%"=="2" goto kill_and_restart
    start "" "http://127.0.0.1:8888"
    start "" "https://www.blogger.com/blog/pages/1444221897689962852"
    goto done_success
)

echo Chon che do khoi dong Chrome:
echo.
echo   [1] KHOI DONG LAI CHROME CHINH (KHUYEN DUNG NHAT - 100%% TU DONG)
echo       -> Dong Chrome hien tai va bat lai voi cong 9222.
echo       -> Giu nguyen 100%% tai khoan thuantranblog & cac tab dang xem.
echo       -> KHONG CAN DANG NHAP LAI BAT KY THU GI!
echo.
echo   [2] MO CUA SO CHROME MOI RIENG BIET (Chay song song)
echo       -> Mo cua so Chrome rieng, khong dong tab nao dang mo.
echo       -> Can dang nhap tai khoan Google Blogger 1 lan duy nhat.
echo.
echo   [3] Thoat
echo.
set "choice=1"
set /p "choice=Nhap lua chon [1, 2 hoac 3, mac dinh 1]: "

if "%choice%"=="2" goto mode_parallel
if "%choice%"=="3" goto exit_now

:mode_restart_main
echo.
echo Dang dong cac tien trinh Chrome cu...
taskkill /F /IM chrome.exe >nul 2>&1
ping -n 3 127.0.0.1 >nul

echo Dang mo lai Chrome chinh voi cong 9222 tren Profile Blogger...
start "" "%MAIN_CHROME%" --remote-debugging-port=9222 --remote-allow-origins=* --profile-directory="Profile 2" "http://127.0.0.1:8888" "https://www.blogger.com/blog/pages/1444221897689962852"
goto check_port_ready

:mode_parallel
echo.
echo Dang mo cua so Chrome rieng biet tren cong 9222...
set "PROFILE_DIR=%LOCALAPPDATA%\BloggerStudioProfile"
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

start "" "%MAIN_CHROME%" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="%PROFILE_DIR%" --no-first-run --no-default-browser-check "https://www.blogger.com/blog/pages/1444221897689962852" "http://127.0.0.1:8888"
goto check_port_ready

:kill_and_restart
echo.
echo Dang tat tat ca tien trinh tren cong 9222 va Chrome...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":9222 .*LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)
taskkill /F /IM chrome.exe >nul 2>&1
ping -n 3 127.0.0.1 >nul
goto mode_restart_main

:check_port_ready
echo.
echo Dang kiem tra ket noi port 9222...
for /L %%i in (1,1,10) do (
    netstat -ano | findstr /R /C:":9222 .*LISTENING" >nul 2>&1
    if %errorlevel%==0 goto done_success
    ping -n 2 127.0.0.1 >nul
)

:done_success
echo.
echo ================================================================
echo   [OK] GOOGLE CHROME CDP DA SAN SANG TREN CONG 9222!
echo   Blogger AI Studio Pro: http://127.0.0.1:8888
echo ================================================================
echo.
echo Ban da co the su dung chuc nang Quet Trang / Quet Bai Viet.
echo Nhan phim bat ky hoac dong cua so nay de hoan tat...
pause >nul
exit /b 0

:exit_now
echo Da huy.
exit /b 0
