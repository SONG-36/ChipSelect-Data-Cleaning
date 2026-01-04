# src/extract/pdf_text.py

from pathlib import Path
import pdfplumber

def extract_text_from_pdf(pdf_path: Path) -> str:
    text_pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_pages.append(page_text)

    return "\n".join(text_pages)
