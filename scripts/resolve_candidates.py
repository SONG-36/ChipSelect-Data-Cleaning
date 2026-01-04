from pathlib import Path
import csv
import argparse
from collections import defaultdict
from src.resolve.field_resolver import resolve_fields


def main():
    parser = argparse.ArgumentParser(description="Resolve candidates into final chip specs")
    parser.add_argument(
        "--input",
        required=True,
        help="Input candidates CSV file"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output resolved chip CSV file"
    )
    args = parser.parse_args()

    in_file = Path(args.input)
    out_file = Path(args.output)

    if not in_file.exists():
        print(f"[ERROR] Candidates file not found: {in_file}")
        return

    grouped = defaultdict(lambda: defaultdict(list))

    with in_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            grouped[row["source_file"]][row["field"]].append(row)

    rows = []
    for source_file, fields in grouped.items():
        resolved = resolve_fields(fields)
        resolved["source_file"] = source_file
        rows.append(resolved)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "source_file",
                "max_freq_mhz",
                "flash_kb",
                "ram_kb",
                "vdd_min",
                "vdd_max",
                "package",
                "temp_grade",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Saved {len(rows)} records → {out_file}")


if __name__ == "__main__":
    main()
