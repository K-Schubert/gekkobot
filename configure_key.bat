@echo off
REM ============================================================
REM  Prompt the user for an OpenAI key and save it to .env
REM  Place this script next to chatbot.exe or in the repo root
REM ============================================================
setlocal
set /p KEY=Enter your OpenAI API key:
if "%KEY%"=="" (
    echo No key entered.  Nothing written.
    goto :eof
)
echo OPENAI_API_KEY=%KEY%> "%~dp0\.env"
echo Key saved to %~dp0.env
pause