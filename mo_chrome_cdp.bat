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
    echo Vui long cai dat Google Chrome roi thu lai.
    pause
    exit /b 1
)

:: 2. Thiet lap thu muc profile rieng de Chrome bat buoc mo cong 9222
set "PROFILE_DIR=%LOCALAPPDATA%\BloggerStudioProfile"
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

:: 3. Kiem tra xem port 9222 co dang bi chiem khong
netstat -ano | findstr /R /C:":9222 .*LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo [THONG BAO] Cong 9222 dang hoat dong.
    echo Dang lam moi ket noi Chrome CDP...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":9222 .*LISTENING"') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    ping -n 2 127.0.0.1 >nul
)

:: 4. Khoi dong Google Chrome voi day du co Remote Debugging Port 9222
echo Dang mo Google Chrome CDP tren cong 9222...
start "" "%MAIN_CHROME%" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="%PROFILE_DIR%" --no-first-run --no-default-browser-check "http://127.0.0.1:8888" "https://www.blogger.com/blog/pages/1444221897689962852"

:: 5. Kiem tra port 9222 san sang
echo Dang kiem tra ket noi...
set "PORT_OK=0"
for /L %%i in (1,1,10) do (
    netstat -ano | findstr /R /C:":9222 .*LISTENING" >nul 2>&1
    if %errorlevel%==0 (
        set "PORT_OK=1"
        goto port_ready
    )
    ping -n 2 127.0.0.1 >nul
)

:port_ready
if "%PORT_OK%"=="1" (
    echo.
    echo ================================================================
    echo   [OK] GOOGLE CHROME CDP DA SAN SANG TREN CONG 9222!
    echo   Blogger AI Studio Pro: http://127.0.0.1:8888
    echo ================================================================
    echo.
    echo LUU Y QUAN TRONG:
    echo 1. Chuyen sang cua so Chrome vua mo.
    echo 2. Neu chua dang nhap tai khoan Blogger (thuantranblog), hay dang nhap 1 lan duy nhat.
    echo 3. Sau khi dang nhap xong, quay lai Blogger Studio va bam 'Thu Lai' de su dung.
    echo.
) else (
    echo.
    echo ================================================================
    echo   [CANH BAO] Chrome da mo nhung cong 9222 chua san sang ngay.
    echo   Vui long doi 3-5 giay roi bam 'Thu Lai' tren giao dien web.
    echo ================================================================
    echo.
)

echo Nhan phim bat ky hoac dong cua so nay de tiep tuc...
pause >nul
exit /b 0
