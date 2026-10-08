@echo off
setlocal
cd /d "%~dp0"

if not exist .venv\Scripts\python.exe (
    py -3 -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt

if not defined HEADLESS set HEADLESS=0
if not defined ACTION_DELAY set ACTION_DELAY=0.8
if not defined BROWSER_CLOSE_DELAY set BROWSER_CLOSE_DELAY=1.0

python -m pytest %*
set TEST_EXIT_CODE=%ERRORLEVEL%

for /f "usebackq delims=" %%I in (`powershell -NoProfile -ExecutionPolicy Bypass -File scripts\setup_allure.ps1`) do set "ALLURE_CMD=%%I"
if defined ALLURE_CMD (
    call "%ALLURE_CMD%" generate report\allure-results --clean --single-file -o report\allure-report
    if errorlevel 1 (
        echo Khong the tao Allure HTML report. Giu lai allure-results de kiem tra loi.
    ) else (
        powershell -NoProfile -ExecutionPolicy Bypass -File scripts\remove_allure_results.ps1
    )
) else (
    echo Khong tim thay Allure CLI. Ket qua tho van nam trong report\allure-results.
)

pause
exit /b %TEST_EXIT_CODE%

