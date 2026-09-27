LegalEase - Project Documentation

Project Name: LegalEase - AI-Powered Legal Document Generator

Purpose:
LegalEase helps entrepreneurs, freelancers and individuals generate professional legal documents (contracts, NDAs, lease agreements) without needing a legal background.

How it works:
1. User enters document type, parties involved, terms and conditions, and effective date.
2. The Streamlit frontend sends this data to a FastAPI backend.
3. The backend builds a prompt and sends it to Google Gemini AI.
4. Gemini generates a structured legal document.
5. The user can preview, edit, and download the document as TXT, DOCX or PDF.

Tech stack: Python, FastAPI, Streamlit, Google Gemini API, python-docx, fpdf2, Pillow

Setup instructions: see README.md in the LegalEase folder for full installation and run steps.

Disclaimer: AI-generated drafts are for convenience only and are not legal advice. A qualified lawyer should review important documents.
