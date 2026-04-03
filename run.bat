@echo off
REM ============================================
REM  Financial RAG Chatbot – Start Both Servers
REM ============================================

echo.
echo  ===  Financial RAG Chatbot  ===
echo.

REM Start FastAPI backend (port 8000) in background
echo [1/2] Starting FastAPI backend on http://localhost:8000 ...
start "FastAPI Backend" cmd /c "cd /d %~dp0 && .venv\Scripts\activate && uvicorn api_app:app --reload --port 8000"

REM Give the backend a moment to boot
timeout /t 3 /nobreak > nul

REM Start Vite frontend (port 5173)
echo [2/2] Starting React frontend on http://localhost:5173 ...
start "React Frontend" cmd /c "cd /d %~dp0\frontend && npm run dev"

echo.
echo  Both servers are starting!
echo  Backend  :  http://localhost:8000
echo  Frontend :  http://localhost:5173
echo.
echo  Press any key to stop both servers...
pause > nul

REM Kill both
taskkill /FI "WINDOWTITLE eq FastAPI Backend" /F > nul 2>&1
taskkill /FI "WINDOWTITLE eq React Frontend" /F > nul 2>&1
echo Stopped.
