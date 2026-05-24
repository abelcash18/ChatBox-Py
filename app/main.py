from __future__ import annotations



from fastapi/middleware.cors 
import CORSMiddleware


from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.rag import RagEngine
from app.llm import generate_reply


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

app = FastAPI(title="chatbox")
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
app.add_middleware(
)

# Static + UI
static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# RAG engine
rag = RagEngine(data_dir=DATA_DIR)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    ui_path = static_dir / "index.html"
    return ui_path.read_text(encoding="utf-8")


@app.post("/api/chat")
def chat(payload: dict) -> JSONResponse:

    # Expected: {"message": "..."}
    message = (payload.get("message") or "").strip()
    if not message:
        return JSONResponse({"reply": "Please type a message."})

    retrieved = rag.retrieve(message, top_k=4)
    reply = generate_reply(user_message=message, retrieved_chunks=retrieved)
    return JSONResponse({"reply": reply, "retrieved": retrieved})

