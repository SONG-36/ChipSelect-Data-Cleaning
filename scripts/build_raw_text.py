# scripts/build_raw_text.py

from pathlib import Path
import argparse
from src.extract.pdf_text import extract_text_from_pdf


def main():
    parser = argparse.ArgumentParser(description="PDF → Raw Text builder")
    parser.add_argument("--input", default="data/raw", help="PDF input directory")
    parser.add_argument("--output", default="data/interim/raw_text", help="Raw text output directory")
    parser.add_argument("--force", action="store_true", help="Force rebuild existing raw text")
    args = parser.parse_args()

    raw_pdf_dir = Path(args.input)
    raw_text_dir = Path(args.output)

    raw_text_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(raw_pdf_dir.rglob("*.pdf"))
    if not pdf_files:
        print(f"[WARN] No PDF files found under {raw_pdf_dir}")
        return

    for pdf_path in pdf_files:
        # 保留子目录结构，避免 sku / family 冲突
        relative_path = pdf_path.relative_to(raw_pdf_dir)
        txt_path = raw_text_dir / relative_path.with_suffix(".txt")
        txt_path.parent.mkdir(parents=True, exist_ok=True)

        if txt_path.exists() and not args.force:
            print(f"[SKIP] Raw text already exists: {txt_path}")
            continue

        print(f"[BUILD] Extracting text from: {pdf_path}")
        try:
            text = extract_text_from_pdf(str(pdf_path))
            txt_path.write_text(text, encoding="utf-8")
            print(f"[OK] Saved raw text → {txt_path}")
        except Exception as e:
            print(f"[ERROR] Failed to process {pdf_path}")
            print(f"        Reason: {e}")


if __name__ == "__main__":
    main()
