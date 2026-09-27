"""Streamlit frontend for LegalEase.  Run from the project root:

    streamlit run frontend/app.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # so `config` and `ai_core` can be imported

import requests
import streamlit as st

import config
from ai_core.generator import format_docx, format_html_preview, format_pdf, sanitize_text
from ai_core.utils import safe_filename

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="centered")
config.ensure_logos()

# ------------------------------------------------------------------ session state
for key, default in {
    "generated_text": "",
    "doc_type": "",
    "terms": "",
    "show_edit": False,
}.items():
    st.session_state.setdefault(key, default)


def _toggle_edit():
    st.session_state.show_edit = not st.session_state.show_edit


def _apply_edit():
    st.session_state.generated_text = st.session_state.editor_widget


# ------------------------------------------------------------------ header
_, col2, _ = st.columns([1, 2, 1])
with col2:
    st.image(str(config.WEB_LOGO_PATH), width=300)

st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Backend status")
    try:
        info = requests.get(f"{config.BACKEND_URL}/health", timeout=2).json()
        st.success(f"Connected - model: {info.get('model')}")
        if not info.get("api_key_configured"):
            st.warning("GEMINI_API_KEY is not set in .env")
    except Exception:
        st.error(f"Backend not reachable at {config.BACKEND_URL}. Start it with uvicorn.")
    st.caption("AI-generated drafts are for convenience only and are not legal advice. "
               "Have a qualified lawyer review important documents.")

# ------------------------------------------------------------------ inputs
document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if st.button("Generate Document"):
    if not (document_type.strip() and parties.strip() and dates.strip()):
        st.warning("Please fill in Document Type, Parties Involved and Effective Date.")
    else:
        with st.spinner("Drafting your document with Gemini..."):
            try:
                response = requests.post(
                    f"{config.BACKEND_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates,
                    },
                    timeout=180,
                )
                if response.ok:
                    st.session_state.generated_text = sanitize_text(response.json()["document"])
                    st.session_state.doc_type = document_type.strip()
                    st.session_state.terms = terms
                    st.session_state.show_edit = False
                    st.session_state.pop("editor_widget", None)
                    st.success("✅ Document Generated Successfully!")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except ValueError:
                        detail = response.text
                    st.error(f"Generation failed: {detail}")
            except requests.exceptions.ConnectionError:
                st.error(f"Cannot reach the backend at {config.BACKEND_URL}. "
                         "Start it with: uvicorn legalEaseAPI.main:app --reload")
            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")
            except Exception as exc:  # noqa: BLE001
                st.error(f"Unexpected error: {exc}")

if not st.session_state.generated_text:
    st.info("Click 'Generate Document' to start")
    st.stop()

# ------------------------------------------------------------------ preview
generated_text = st.session_state.generated_text
styled_html = format_html_preview(generated_text)
st.markdown(
    "<div style='background:#111827;border:1px solid #1f2937;border-radius:10px;padding:20px;"
    f"max-height:420px;overflow-y:auto;'>{styled_html}</div>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ edit
st.button("✏️ Click to Edit Document", on_click=_toggle_edit)
if st.session_state.show_edit:
    st.text_area(
        "Edit Document Below:",
        value=st.session_state.generated_text,
        height=300,
        key="editor_widget",
        on_change=_apply_edit,
    )
    st.caption("Press Ctrl+Enter to apply your edits. Downloads always use the latest edited text.")

# ------------------------------------------------------------------ downloads
text_now = st.session_state.generated_text
doc_type_now = st.session_state.doc_type or "Legal Document"
terms_now = st.session_state.terms
base_name = safe_filename(doc_type_now)

st.markdown("#### Download")
try:
    st.download_button(
        "📄 Download as .TXT",
        data=text_now,
        file_name=f"{base_name}.txt",
        mime="text/plain",
    )
    st.download_button(
        "📝 Download as .DOCX",
        data=format_docx(text_now, doc_type_now, terms_now),
        file_name=f"{base_name}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    st.download_button(
        "📕 Download as .PDF",
        data=format_pdf(text_now, doc_type_now, terms_now),
        file_name=f"{base_name}.pdf",
        mime="application/pdf",
    )
except Exception as exc:  # noqa: BLE001
    st.error(f"Could not build the download files: {exc}")
