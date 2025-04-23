import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from pathlib import Path
import sys

def locate_env():
    """Return the path to .env that lives next to the running file."""
    if getattr(sys, "frozen", False):          # we are in a PyInstaller EXE
        return Path(sys.executable).parent / ".env"
    return Path(__file__).resolve().parent / ".env"

# Load environment variables
load_dotenv(dotenv_path=locate_env(), override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API client
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

app = FastAPI(
    title="Local AI Chatbot",
    docs_url="/docs",  # keep Swagger UI for quick testing
)

# Mount static assets (CSS/JS)
app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static",
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

try:
    with open("./system_prompt.txt", "r") as f:
        system_prompt = f.read().strip()
except Exception as e:
    system_prompt = "You are GekkoBot, an AI chatbot."

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """Forward the user message to OpenAI and return the reply."""
    try:

        if not client.api_key:
            raise Exception("OpenAI API key is not configured")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ],
            temperature=0.7,
        )
        content = completion.choices[0].message.content
        return {"response": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/")
async def root():
    """Serve the single‑page chat UI."""
    return FileResponse("frontend/index.html")

# Add this section to run the server when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    print("Starting the server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
