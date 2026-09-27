@echo off
REM Starts backend and frontend in two windows (Windows). Run from the project folder with venv created.
cd /d "%~dp0"
start "LegalEase Backend" cmd /k "venv\Scripts\activate && uvicorn legalEaseAPI.main:app --reload --port 8000"
timeout /t 3 >nul
start "LegalEase Frontend" cmd /k "venv\Scripts\activate && streamlit run frontend/app.py"
