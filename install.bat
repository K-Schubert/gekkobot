@echo off
REM ============================================================
REM  Build a one-file Windows executable for the FastAPI chatbot
REM ============================================================

REM ----- 1. Create / activate virtual environment -------------
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate

REM ----- 2. Ensure tools & deps -------------------------------
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller

REM ----- 3. Run PyInstaller -----------------------------------
pyinstaller --onefile --name gekkobot --add-data "frontend;frontend" --collect-submodules uvicorn --collect-submodules starlette main.py

REM ----- 4. Copy system_prompt.txt to dist folder -------------
copy system_prompt.txt dist\ /Y
echo Copied system_prompt.txt to dist folder. Users can modify this file directly.

echo.
echo Build complete!  You will find gekkobot.exe inside the dist\ folder.
echo Remember to copy your .env next to the EXE before running.
echo You can modify system_prompt.txt in the dist folder without rebuilding the app.
pause