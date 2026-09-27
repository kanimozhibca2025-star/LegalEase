LegalEase - Project Design

Architecture:
Streamlit Frontend (user inputs, preview, download)
    -> FastAPI Backend (/generate endpoint)
        -> Gemini AI (generates document text)
    <- Formatting modules (DOCX, PDF, TXT)

Components:
- frontend/app.py - Streamlit UI
- legalEaseAPI/main.py - FastAPI app
- legalEaseAPI/routes.py - /generate endpoint, request validation
- ai_core/gemini_generator.py - builds the prompt, calls Gemini
- ai_core/generator.py - sanitizes text, builds DOCX/PDF/HTML preview
- config.py - settings, API key, logo handling

Data flow: user fills form -> Streamlit sends POST /generate -> FastAPI calls Gemini -> text returned -> user edits -> downloads in chosen format.
