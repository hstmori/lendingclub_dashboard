"""Lọc file LendingClub gốc (2007–2018Q4) xuống các khoản giải ngân từ 2010 đến hết 2017.

Chạy từ thư mục gốc của repo:
    python scripts/00_filter_2010_2017.py
"""
from pathlib import Path

import pandas as pd

input_file = Path("data/raw/accepted_2007_to_2018Q4.csv")
output_file = Path("data/raw/accepted_2010_to_2017.csv")

chunk_size = 200_000
first_write = True
total_input = 0
total_output = 0

for chunk_number, chunk in enumerate(
    pd.read_csv(input_file, chunksize=chunk_size, low_memory=False),
    start=1,
):
    total_input += len(chunk)

    # Tách năm từ chuỗi như "Dec-2015"
    issue_year = pd.to_numeric(
        chunk["issue_d"].astype("string").str.strip().str.extract(r"(\d{4})$", expand=False),
        errors="coerce",
    )

    # Giữ các khoản vay từ 2010 đến hết 2017
    filtered_chunk = chunk.loc[issue_year.between(2010, 2017, inclusive="both")].copy()

    if not filtered_chunk.empty:
        filtered_chunk.to_csv(
            output_file,
            mode="w" if first_write else "a",
            header=first_write,
            index=False,
            encoding="utf-8-sig",
        )
        first_write = False
        total_output += len(filtered_chunk)

    print(f"Chunk {chunk_number:02}: xử lý {len(chunk):,} dòng, giữ lại {len(filtered_chunk):,} dòng")

print("-" * 60)
print(f"Tổng số dòng đã đọc: {total_input:,}")
print(f"Tổng số dòng được giữ lại: {total_output:,}")
print(f"File đầu ra: {output_file}")
