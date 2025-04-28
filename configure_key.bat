@echo off
REM ============================================================
REM  Prompt for OpenAI key -> write .env -> copy to dist\
REM  Place and run this script in the project root.
REM ============================================================
setlocal

REM --- 1. Ask user for a key ----------------------------------
set /p KEY=Enter your Gemini API key:
if "%KEY%"=="" (
    echo No key entered. Nothing written.
    goto done
)

REM --- 2. Write .env next to this script ----------------------
echo GEMINI_API_KEY=%KEY%> "%~dp0.env"
echo Key saved to "%~dp0.env"

REM --- 3. Also drop a copy into dist\ (for chatbot.exe) -------
if exist "%~dp0dist\" (
    copy "%~dp0.env" "%~dp0dist" /Y > nul
    echo .env also copied to "%~dp0dist\"
) else (
    echo dist\ folder not found — skipping copy.
)

:done
pause