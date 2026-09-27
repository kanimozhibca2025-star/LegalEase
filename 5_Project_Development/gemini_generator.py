"""Gemini integration: turns user inputs into a structured legal document."""
import logging
import time

import config
from ai_core.utils import split_terms

logger = logging.getLogger(__name__)

try:  # preferred: current official SDK  (pip install google-genai)
    from google import genai as _genai
    from google.genai import types as _types

    _SDK = "google-genai"
except ImportError:  # fallback: legacy SDK  (pip install google-generativeai)
    try:
        import google.generativeai as _legacy

        _SDK = "google-generativeai"
    except ImportError:
        _SDK = None


class GeminiConfigError(RuntimeError):
    """Missing / invalid configuration (API key, SDK not installed)."""


class GeminiGenerationError(RuntimeError):
    """The Gemini API call failed."""


SYSTEM_INSTRUCTION = (
    "You are a meticulous legal drafting assistant. You draft clear, professional, "
    "well-structured legal documents from the details supplied by the user.\n"
    "FORMAT RULES (very important):\n"
    "- Output PLAIN TEXT only. No markdown: no #, *, **, backticks or tables.\n"
    "- The first line is the document title on its own line.\n"
    "- Section headings are on their own line, numbered, e.g. '1. Services:'.\n"
    "- Sub-items use the form 'a) text'.\n"
    "- Use every party name, date and term the user provides, exactly as given.\n"
    "- Where information is missing use square-bracket placeholders such as "
    "[Party Address] or [Governing State].\n"
    "- Finish with an execution / signature block for each party.\n"
    "- Output the document only: no introduction, no commentary, no disclaimers."
)


class GeminiDocumentGenerator:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.GEMINI_MODEL
        self._client = None  # created lazily so the server can start without a key

    # ------------------------------------------------------------------ setup
    def _ensure_client(self):
        if self._client is not None:
            return
        if _SDK is None:
            raise GeminiConfigError("No Gemini SDK installed. Run: pip install google-genai")
        if not config.has_valid_api_key():
            raise GeminiConfigError(
                "GEMINI_API_KEY is missing. Put your key in the .env file "
                "(get one at https://aistudio.google.com/app/apikey) and restart the backend."
            )
        if _SDK == "google-genai":
            self._client = _genai.Client(api_key=config.GEMINI_API_KEY)
        else:
            _legacy.configure(api_key=config.GEMINI_API_KEY)
            self._client = _legacy.GenerativeModel(
                self.model_name, system_instruction=SYSTEM_INSTRUCTION
            )

    # ----------------------------------------------------------------- prompt
    @staticmethod
    def build_prompt(document_type: str, parties: str, terms: str, dates: str) -> str:
        term_lines = "\n".join(f"- {t}" for t in split_terms(terms)) or (
            "- (none supplied: include standard, balanced clauses for this document type)"
        )
        return (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions to include (each must appear as a clause):\n{term_lines}\n"
            "Ensure formal legal structure with multiple sections and legal clauses "
            "(e.g. definitions, obligations, payment or consideration, confidentiality, "
            "term and termination, governing law, entire agreement, severability, signatures)."
        )

    # --------------------------------------------------------------- generate
    def _call(self, prompt: str) -> str:
        if _SDK == "google-genai":
            resp = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=_types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION, temperature=0.4
                ),
            )
        else:
            resp = self._client.generate_content(prompt)
        text = getattr(resp, "text", None)
        if not text or not text.strip():
            raise GeminiGenerationError(
                "Gemini returned an empty response (it may have been blocked by safety filters). "
                "Try rewording your input."
            )
        return text

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        self._ensure_client()
        prompt = self.build_prompt(document_type, parties, terms, dates)
        last_err = None
        for attempt in (1, 2):  # one retry for transient errors
            try:
                return self._call(prompt)
            except GeminiGenerationError:
                raise
            except Exception as exc:  # network, quota, bad model name, ...
                last_err = exc
                logger.warning("Gemini call failed (attempt %s): %s", attempt, exc)
                time.sleep(1.5)
        raise GeminiGenerationError(f"Gemini API error (model '{self.model_name}'): {last_err}")
