import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# ----------------------------------------------------------
# 1.  .env file location (still external to the bundled EXE)
# ----------------------------------------------------------
def locate_env() -> Path:
    """Return Path to .env living next to the running file/exe."""
    if getattr(sys, "frozen", False):          # PyInstaller one-file
        return Path(sys.executable).parent / ".env"
    return Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=locate_env(), override=True)

# ----------------------------------------------------------
# 2.  OpenAI client
# ----------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ----------------------------------------------------------
# 3.  FastAPI app & static file handling (Fix A)
# ----------------------------------------------------------
app = FastAPI(title="Gekko AI Chatbot", docs_url="/docs")

# Determine where the frontend lives at runtime
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS) / "frontend"         # type: ignore[attr-defined]
else:
    BASE_DIR = Path(__file__).resolve().parent / "frontend"

# Mount CSS/JS
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# ----------------------------------------------------------
# 4.  Chat endpoint
# ----------------------------------------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Optional system prompt
try:
    with open(Path(__file__).resolve().parent / "system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()
except FileNotFoundError:
    system_prompt = "You are GekkoBot, an AI chatbot."

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        if not client.api_key:
            raise ValueError("OpenAI API key is not configured")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message},
            ],
            temperature=0.7,
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# ----------------------------------------------------------
# 5.  Serve the SPA entry point
# ----------------------------------------------------------
@app.get("/")
async def root():
    return FileResponse(BASE_DIR / "index.html")

# ----------------------------------------------------------
# 6.  Dev runner
# ----------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    print("Starting the server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
