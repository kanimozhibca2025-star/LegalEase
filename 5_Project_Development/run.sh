#!/usr/bin/env bash
# Starts the FastAPI backend and the Streamlit frontend (Linux / macOS / Git Bash).
cd "$(dirname "$0")"
uvicorn legalEaseAPI.main:app --reload --port 8000 &
BACKEND_PID=$!
trap "kill $BACKEND_PID 2>/dev/null" EXIT
sleep 2
streamlit run frontend/app.py
