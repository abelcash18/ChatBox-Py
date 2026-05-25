# Start the ChatBot FastAPI server
# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Run FastAPI
Write-Host ""
Write-Host "Starting ChatBot server on http://127.0.0.1:8000"
Write-Host ""

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Read-Host "Press Enter to exit"
