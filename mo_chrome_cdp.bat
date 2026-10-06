@echo off
title Blogger AI Studio Pro - Khoi Dong Chrome CDP (Port 9222)
cls
echo ================================================================
echo    KHOI DONG GOOGLE CHROME DEBUGGING (PORT 9222)
echo    Danh cho he thong Blogger AI Studio Pro - LuViet Automation
echo ================================================================
echo.

:: Tim Google Chrome chinh
set "MAIN_CHROME="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set "MAIN_CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set "MAIN_CHROME=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set "MAIN_CHROME=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
)

:: Tim Chromium doc lap (Playwright) de chay song song khong bi xung dot
set "ISOLATED_CHROME="
for /d %%d in ("%LOCALAPPDATA%\ms-playwright\chromium-*") do (
    if exist "%%d\chrome-win64\chrome.exe" (
        set "ISOLATED_CHROME=%%d\chrome-win64\chrome.exe"
    )
)

:: Kiem tra port 9222 co dang bat khong
netstat -ano | findstr /R /C:":9222 .*LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo [THONG BAO] Cong 9222 DANG HOAT DONG SAN SANG!
    echo.
    echo Ban co muon:
    echo   [1] Mo trang Blogger AI Studio (http://127.0.0.1:8888)
    echo   [2] Tat tien trinh cu va khoi dong lai
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
echo   [1] CHAY SONG SONG (Khuyen dung)
echo       Khong dong bat ky tab nao ban dang xem.
echo       Mo cua so Chromium moi tren cong 9222.
echo.
echo   [2] KHOI DONG LAI CHROME CHINH
echo       Dong Chrome hien tai va bat lai voi cong 9222.
echo       Giu nguyen 100%% tai khoan Google & cac tab dang dang nhap.
echo.
echo   [3] Thoat
echo.
set "choice=1"
set /p "choice=Nhap lua chon [1, 2 hoac 3, mac dinh 1]: "

if "%choice%"=="2" goto mode_restart_main
if "%choice%"=="3" goto exit_now

:mode_parallel
echo.
echo Dang khoi dong cua so Chromium doc lap tren cong 9222...
set "CHROME_TO_RUN=%ISOLATED_CHROME%"
if not defined CHROME_TO_RUN set "CHROME_TO_RUN=%MAIN_CHROME%"

set "PROFILE_DIR=%LOCALAPPDATA%\BloggerStudioProfile"
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

start "" "%CHROME_TO_RUN%" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="%PROFILE_DIR%" --no-first-run --no-default-browser-check "https://www.blogger.com/blog/pages/1444221897689962852" "http://127.0.0.1:8888"
goto check_port_ready

:mode_restart_main
echo.
echo CANH BAO: Thao tac nay se dong cac cua so Google Chrome dang mo de khoi dong lai voi port 9222.
set /p "confirm=Xac nhan dong Chrome de bat lai? (Y/N, mac dinh Y): "
if /i "%confirm%"=="N" goto exit_now

echo Dang dong Chrome...
taskkill /F /IM chrome.exe >nul 2>&1
ping -n 3 127.0.0.1 >nul

echo Dang mo lai Chrome chinh voi cong 9222...
start "" "%MAIN_CHROME%" --remote-debugging-port=9222 --remote-allow-origins=* "https://www.blogger.com/blog/pages/1444221897689962852" "http://127.0.0.1:8888"
goto check_port_ready

:kill_and_restart
echo.
echo Dang tat tien trinh cu tren cong 9222...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":9222 .*LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)
ping -n 2 127.0.0.1 >nul
goto mode_parallel

:check_port_ready
echo Dang kiem tra ket noi port 9222...
ping -n 3 127.0.0.1 >nul

:done_success
echo.
echo ================================================================
echo   [OK] CHROME CDP DA SAN SANG TREN CONG 9222!
echo   Blogger Studio: http://127.0.0.1:8888
echo ================================================================
echo.
echo Ban co the bat dau su dung Blogger AI Studio Pro.
echo Nhan phim bat ky hoac dong cua so nay de tiep tuc...
pause >nul
exit /b 0

:exit_now
echo Da huy.
exit /b 0
