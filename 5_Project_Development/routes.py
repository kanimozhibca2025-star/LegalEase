"""API routes: POST /generate builds a legal document with Gemini."""
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from ai_core.gemini_generator import (
    GeminiConfigError,
    GeminiDocumentGenerator,
    GeminiGenerationError,
)

logger = logging.getLogger(__name__)

router = APIRouter()
gemini_generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    document_type: str = Field(..., min_length=2, max_length=200)
    parties: str = Field(..., min_length=2, max_length=2000)
    terms: str = Field("", max_length=8000)
    dates: str = Field(..., min_length=2, max_length=100)


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        response = gemini_generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates,
        )
    except GeminiConfigError as exc:
        logger.error("Configuration error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
    except GeminiGenerationError as exc:
        logger.error("Generation error: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc))
    return {"document": response}
