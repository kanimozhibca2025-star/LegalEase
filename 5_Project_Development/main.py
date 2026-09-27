"""FastAPI entry point.  Run from the project root:

    uvicorn legalEaseAPI.main:app --reload
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from legalEaseAPI.routes import router

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

app = FastAPI(title="LegalEase - AI Legal Document Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
def home():
    return {"message": "Welcome to LegalEase AI Legal Document Generator API"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": config.GEMINI_MODEL,
        "api_key_configured": config.has_valid_api_key(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
