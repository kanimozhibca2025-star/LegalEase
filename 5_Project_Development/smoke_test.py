"""Offline smoke test (no Gemini key needed):  python tests/smoke_test.py

Checks the formatters and, if fastapi/httpx are installed, the API with a mocked Gemini.
Output files are written to tests/output/ so you can open and inspect them.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import config
from ai_core.generator import format_docx, format_html_preview, format_pdf, sanitize_text
from ai_core.utils import safe_filename

SAMPLE = """## Freelance Work Contract

Agreement made this 15th day of April, 2025 \u2014 \u201cEffective Date\u201d

Between:

Jane Doe (hereinafter the \u201cService Provider\u201d), residing at [Address]

And:

TechNova Inc. (hereinafter the \u201cClient\u201d), a corporation with fees of $5,000

1. Services:

The Service Provider agrees to deliver the work by May 15, 2025.

2. Termination:

a) Mutual written agreement of the parties;
b) Breach of this Agreement by either party.

**3. Payment:**

* Payment within 7 days of invoice
* Late fees apply <after> 30 days

IN WITNESS WHEREOF, the parties have executed this Agreement.

______________________
Jane Doe (Service Provider)
"""
TERMS = "Work must be delivered by May 15, 2025; Payment within 7 days; Confidentiality at all times"

out = ROOT / "tests" / "output"
out.mkdir(parents=True, exist_ok=True)
config.ensure_logos()

clean = sanitize_text(SAMPLE)
assert "\u201c" not in clean and "##" not in clean and "**" not in clean
print("sanitize_text ... ok")

page = format_html_preview(SAMPLE)
assert "<h2" in page and "&lt;after&gt;" in page and "&#36;5,000" in page and "\n\n" not in page
print("format_html_preview ... ok")

docx_bytes = format_docx(clean, "Freelance Work Contract", TERMS)
assert docx_bytes[:2] == b"PK"
(out / "sample.docx").write_bytes(docx_bytes)
print("format_docx ... ok  ->", out / "sample.docx")

pdf_bytes = format_pdf(clean, "Freelance Work Contract", TERMS)
assert pdf_bytes[:4] == b"%PDF"
(out / "sample.pdf").write_bytes(pdf_bytes)
print("format_pdf ... ok   ->", out / "sample.pdf")

assert safe_filename("Freelance Work Contract") == "freelance_work_contract"

try:
    from fastapi.testclient import TestClient
    from legalEaseAPI.main import app
    from legalEaseAPI import routes
except ImportError as exc:
    print("API test skipped (install fastapi & httpx):", exc)
else:
    routes.gemini_generator.generate_document = lambda *a, **k: SAMPLE
    client = TestClient(app)
    assert client.get("/").status_code == 200
    assert client.get("/health").json()["status"] == "ok"
    r = client.post("/generate", json={
        "document_type": "NDA", "parties": "A (Disclosing), B (Receiving)",
        "terms": "Keep secrets; 2 year term", "dates": "1 Jan 2026"})
    assert r.status_code == 200 and "document" in r.json()
    assert client.post("/generate", json={"document_type": "NDA"}).status_code == 422
    print("API endpoints ... ok")

print("\nAll checks passed.")
