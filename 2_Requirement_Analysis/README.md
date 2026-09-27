LegalEase - Requirement Analysis

Functional requirements:
- User enters document type, parties, terms, effective date
- System generates a legal document using Gemini AI
- User can edit the generated text
- User can download the document as TXT, DOCX or PDF

Non-functional requirements:
- Fast response (under 30 seconds)
- Simple, easy to use interface
- Secure handling of the API key

Tech requirements:
- Python 3.10+, FastAPI, Streamlit, Google Gemini API, python-docx, fpdf2
