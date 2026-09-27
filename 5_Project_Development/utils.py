"""Small helpers shared by backend and frontend."""
import re


def split_terms(terms: str) -> list:
    """Split the semicolon (or newline) separated terms into a clean list."""
    return [t.strip(" \t-*") for t in re.split(r"[;\n]+", terms or "") if t.strip(" \t-*")]


def safe_filename(name: str, default: str = "legal_document") -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", (name or "").lower()).strip("_")
    return slug or default
