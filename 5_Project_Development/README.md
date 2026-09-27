# LegalEase - AI Legal Document Generator

FastAPI backend + Streamlit frontend + Google Gemini. Enter a document type, parties, terms and
effective date, get a formatted legal draft, edit it, and download it as .txt, .docx or .pdf.

```
LegalEase/
├── ai_core/
│   ├── gemini_generator.py   # Gemini prompt + API call
│   ├── generator.py          # sanitize_text, format_docx, format_pdf, format_html_preview
│   └── utils.py
├── legalEaseAPI/
│   ├── main.py               # FastAPI app  (GET /, GET /health)
│   └── routes.py             # POST /generate + DocumentRequest
├── frontend/app.py           # Streamlit UI
├── Image/                    # Logo.png, inverseLogo.png (auto-created; replace with your own)
├── tests/smoke_test.py
├── config.py  .env  .env.example  requirements.txt  run.sh  run.bat
```

## 1. Setup (VS Code terminal, Python 3.10+)

```powershell
# Windows PowerShell                       # macOS / Linux
python -m venv venv                        python3 -m venv venv
venv\Scripts\activate                      source venv/bin/activate
pip install -r requirements.txt            pip install -r requirements.txt
```
In VS Code press `Ctrl+Shift+P` -> "Python: Select Interpreter" -> choose the `venv` one.
If PowerShell blocks activation: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## 2. Add your Gemini key

Get a free key at https://aistudio.google.com/app/apikey and edit `.env`:

```
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-2.5-flash
```
Note: the project document names `gemini-1.5-pro`, but Google has retired the 1.5 models, so the default is a
current model. Any Gemini model name works in `GEMINI_MODEL` (e.g. `gemini-2.5-pro`).

## 3. Run (two terminals, both with the venv active, both in the project root)

```
uvicorn legalEaseAPI.main:app --reload          # terminal 1  -> http://127.0.0.1:8000  (docs: /docs)
streamlit run frontend/app.py                   # terminal 2  -> http://localhost:8501
```
Shortcut: `run.bat` (Windows) or `./run.sh` (macOS/Linux/Git Bash) starts both.

## 4. Test

1. Offline check (no API key needed): `python tests/smoke_test.py` (writes sample files to `tests/output/`).
2. Backend: open http://127.0.0.1:8000/docs -> POST /generate -> "Try it out" with `docs/sample_input.json`.
3. Full app: open http://localhost:8501 and fill in
   - Document Type: `Freelance Work Contract`
   - Parties: `Jane Doe (Service Provider), TechNova Inc. (Client)`
   - Terms: `Work must be delivered by May 15, 2025; Payment will be made within 7 days of invoice; The client retains intellectual property rights; Confidentiality must be maintained at all times`
   - Date: `April 15, 2025`

   Click Generate, check the preview, click Edit and change some text (Ctrl+Enter), then download all three formats
   and confirm the edits, logo, terms table and footer appear.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Cannot reach the backend" | Start uvicorn first; check `BACKEND_URL` in `.env` |
| "GEMINI_API_KEY is missing" | Put the key in `.env`, then restart uvicorn |
| "Gemini API error ... 404 model not found" | Change `GEMINI_MODEL` to a current model name |
| `ModuleNotFoundError: config` / `ai_core` | Run commands from the project root folder |
| PDF errors about `fpdf` | Use `fpdf2` (`pip uninstall fpdf` then `pip install fpdf2`) |
| Port 8000 busy | `uvicorn ... --port 8001` and set `BACKEND_URL=http://localhost:8001` |

AI-generated drafts are not legal advice; have a qualified lawyer review important documents.
