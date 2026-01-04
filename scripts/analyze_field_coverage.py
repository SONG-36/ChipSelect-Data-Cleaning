import pandas as pd

CSV_FILE = "data/processed/chips_v1.1.csv"

df = pd.read_csv(CSV_FILE)

print("=== Field Coverage Analysis ===\n")

coverage = (
    df.notna()
      .mean()
      .sort_values(ascending=False)
      .reset_index()
)

coverage.columns = ["field", "coverage_ratio"]

print(coverage.to_string(index=False))

print("\n=== Raw Sample ===")
print(df.head())
