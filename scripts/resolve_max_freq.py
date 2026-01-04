import pandas as pd
from src.resolve.max_freq import resolve_max_freq

CAND_FILE = "data/candidates/candidates_v0.1.csv"
OUT_FILE = "data/processed/max_freq_canonical_v0.1.csv"

df = pd.read_csv(CAND_FILE)

# 只处理 max_freq_mhz
df = df[df["field"] == "max_freq_mhz"]

rows = []

for source_file, g in df.groupby("source_file"):
    candidates = []
    for _, r in g.iterrows():
        candidates.append({
            "value": r["candidate"],
            "context": r["context"]
        })

    val = resolve_max_freq(candidates)

    rows.append({
        "source_file": source_file,
        "max_freq_mhz": val
    })

out = pd.DataFrame(rows)
out.to_csv(OUT_FILE, index=False)

print(f"Saved {len(out)} rows to {OUT_FILE}")
