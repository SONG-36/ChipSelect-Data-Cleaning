import os
import re
import csv
from src.extract.pdf_text import extract_text_from_pdf

RAW_DIR = "data/raw/st"
OUT_DIR = "data/candidates"
OUT_FILE = os.path.join(OUT_DIR, "candidates_v0.1.csv")

os.makedirs(OUT_DIR, exist_ok=True)

FIELDS = {
    "max_freq_mhz": r"(\d{2,4})\s*mhz",
    "flash_kb": r"(\d{2,5})\s*(k|kb|kbyte|kbytes|mbyte)",
    "ram_kb": r"(\d{2,5})\s*(k|kb|kbyte|kbytes)\s*(sram)?",
    "vdd": r"(\d\.\d)\s*v",
}

def extract_candidates(text: str, field: str, pattern: str):
    results = []
    for m in re.finditer(pattern, text, flags=re.IGNORECASE):
        start = max(m.start() - 40, 0)
        end = min(m.end() + 40, len(text))
        context = text[start:end].replace("\n", " ")
        results.append({
            "field": field,
            "candidate": m.group(1),
            "context": context
        })
    return results

def main():
    rows = []

    for fname in os.listdir(RAW_DIR):
        if not fname.lower().endswith(".pdf"):
            continue

        sku = fname.replace("_DS.pdf", "")
        pdf_path = os.path.join(RAW_DIR, fname)
        print(f"[INFO] Processing {sku}")

        try:
            text = extract_text_from_pdf(pdf_path)
        except Exception as e:
            print(f"[WARN] Failed to parse {fname}: {e}")
            continue

        for field, pattern in FIELDS.items():
            candidates = extract_candidates(text, field, pattern)
            for c in candidates:
                rows.append({
                    "sku": sku,
                    "field": c["field"],
                    "candidate": c["candidate"],
                    "context": c["context"],
                    "source_file": fname
                })

    with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["sku", "field", "candidate", "context", "source_file"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"[DONE] Saved {len(rows)} candidates to {OUT_FILE}")

if __name__ == "__main__":
    main()
