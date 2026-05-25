@echo off
REM Start the ChatBot FastAPI server

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run FastAPI
echo.
echo Starting ChatBot server on http://127.0.0.1:8000
echo.
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
