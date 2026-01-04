from pathlib import Path
import csv
import argparse
from src.candidate.candidate_rules import extract_candidates


def main():
    parser = argparse.ArgumentParser(description="Extract candidates from raw text")
    parser.add_argument(
        "--input",
        required=True,
        help="Input directory containing raw text files"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output CSV file for candidates"
    )
    args = parser.parse_args()

    raw_text_dir = Path(args.input)
    out_file = Path(args.output)
    out_dir = out_file.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    txt_files = list(raw_text_dir.rglob("*.txt"))
    if not txt_files:
        print(f"[WARN] No raw_text files found under {raw_text_dir}")
        return

    for txt in txt_files:
        rel_path = txt.relative_to(raw_text_dir)
        print(f"[CAND] Processing raw text: {rel_path}")

        text = txt.read_text(encoding="utf-8", errors="ignore")
        cands = extract_candidates(text)

        for c in cands:
            c["source_file"] = txt.name
            c["source_path"] = str(rel_path)
            rows.append(c)

    if not rows:
        print("[WARN] No candidates extracted.")
        return

    with out_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["source_file", "source_path", "field", "candidate", "context"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Saved {len(rows)} candidates → {out_file}")


if __name__ == "__main__":
    main()
