@echo off
setlocal

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
pause
exit /b %TEST_EXIT_CODE%

