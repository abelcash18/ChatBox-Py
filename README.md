# chatbox

A small real-world-ish **AI chatbox** project: **FastAPI backend + simple web UI**.

## Features
- `/` serves a tiny HTML/JS chat UI
- `POST /api/chat` accepts `{ "message": "..." }`
- “RAG-style” retrieval over a local document folder (`data/`)
- Lightweight **local embedding** + cosine similarity (no external API required)
- Mock LLM response generator by default (optional OpenAI via env var)

## Project structure
- `app/main.py` - FastAPI app + API routes
- `app/rag.py` - document loading, chunking, retrieval
- `app/llm.py` - mock LLM and optional OpenAI integration
- `app/static/` - frontend assets
- `data/` - local text documents to index

## Setup (Windows)
1) Create venv
```bat
cd "c:\Users\User\Desktop\New folder (2)\chatbox"
python -m venv .venv
```

2) Activate
```bat
.venv\Scripts\activate
```

3) Install dependencies
```bat
pip install -r requirements.txt
```

## Run
```bat
uvicorn app.main:app --reload --port 8000
```
Then open:
- http://127.0.0.1:8000

## Environment variables (optional)
- `OPENAI_API_KEY` - if set, the LLM can use OpenAI (otherwise mock).
- `EMBED_MODEL` - reserved for future; current embedding is local.

## Tests
```bat
pytest -q
```

# ChatBox-Py
