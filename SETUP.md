# Setup Guide

## First Time Setup

### 1. Install Dependencies
```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 2. Add Sample Data (Optional)
Create a file: `data/sample.txt` with some content to test retrieval:
```
FastAPI is a modern web framework for building APIs with Python.
It provides automatic documentation and high performance.
```

## Running the App

### Option 1: PowerShell Script (Recommended)
```powershell
.\run.ps1
```

### Option 2: Batch Script (Windows CMD)
```cmd
run.bat
```

### Option 3: Manual Command
```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Then open browser to: **http://127.0.0.1:8000**

## Troubleshooting

### Problem: "404 Not Found" or "405 Method Not Allowed"
**Cause**: You're accessing from port 5500 (Live Server) instead of port 8000 (FastAPI)

**Solution**: 
- ❌ DO NOT use VS Code Live Server (port 5500)
- ✅ DO use only FastAPI server (port 8000)
- Close any Live Server instances
- Access: http://127.0.0.1:8000 (NOT :5500)

### Problem: "Port 8000 already in use"
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number)
taskkill /PID <PID> /F
```

### Problem: ModuleNotFoundError
**Solution**: Make sure venv is activated:
```powershell
.\.venv\Scripts\Activate.ps1
```

## Test the App
```powershell
pytest -q
```

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Returns HTML UI |
| GET | `/favicon.ico` | Browser favicon |
| POST | `/api/chat` | Chat endpoint |

### Chat Endpoint Example
```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is FastAPI?"}'
```

## Using OpenAI (Optional)
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
uvicorn app.main:app --reload
```

If `OPENAI_API_KEY` is not set, the app uses mock responses.
