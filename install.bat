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
pyinstaller --onefile --name chatbot --add-data "frontend;frontend" --collect-submodules uvicorn --collect-submodules starlette main.py

echo.
echo Build complete!  You will find chatbot.exe inside the dist\ folder.
echo Remember to copy your .env next to the EXE before running.
pause