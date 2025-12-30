import os
import pandas as pd

from src.extract.pdf_text import extract_text_from_pdf
from src.extract.baseline_extract import extract_baseline_fields

RAW_DIR = "data/raw"
OUT_FILE = "data/processed/chips_v1.1.csv"

rows = []

for root, _, files in os.walk(RAW_DIR):
    for fname in files:
        # 只处理 PDF 文件
        if not fname.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(root, fname)
        print(f"Processing: {pdf_path}")

        # 提取文本（内部已做异常处理）
        text = extract_text_from_pdf(pdf_path)

        # 跳过无法解析 / 空文本的 PDF
        if not text.strip():
            continue

        # 抽取字段
        fields = extract_baseline_fields(text)
        fields["source_file"] = fname
        fields["source_path"] = pdf_path

        rows.append(fields)

# 汇总为 DataFrame
df = pd.DataFrame(rows)

# 确保输出目录存在
os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

# 写出 CSV
df.to_csv(OUT_FILE, index=False)

print(f"Saved {len(df)} records to {OUT_FILE}")
