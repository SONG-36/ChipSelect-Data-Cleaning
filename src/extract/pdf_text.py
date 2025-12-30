import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    print(f"[INFO] Opening PDF: {pdf_path}")

    try:
        text_pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)
        return "\n".join(text_pages)

    except Exception as e:
        print(f"[WARN] Failed to parse PDF: {pdf_path}")
        print(f"       Reason: {e}")
        return ""
