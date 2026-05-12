#!/usr/bin/env python3
"""Load supermarket sales from Excel (.xlsx) into Postgres via pandas to_sql. Run create_tables.py first. Re-run appends; truncate for fresh load."""

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sqlalchemy import text

from config import get_engine, get_table_name

DEFAULT_SHEET = "SuperMarket Analysis"

COLUMN_MAP = {
    "Invoice ID": "invoice_id",
    "Branch": "branch",
    "City": "city",
    "Customer type": "customer_type",
    "Gender": "gender",
    "Product line": "product_line",
    "Unit price": "unit_price",
    "Quantity": "quantity",
    "Tax 5%": "tax_5",
    "Sales": "sales",
    "Date": "sale_date",
    "Time": "sale_time",
    "Payment": "payment",
    "cogs": "cogs",
    "gross margin percentage": "gross_margin_percentage",
    "gross income": "gross_income",
    "Rating": "rating",
}
TABLE_COLUMNS = list(COLUMN_MAP.values())
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_PATH = DATA_DIR / "supermarket-analysis.xlsx"


def _to_snake(name: str) -> str:
    s = name.strip()
    s = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|\s+|-", "_", s)
    s = re.sub(r"[^a-zA-Z0-9_]", "", s)
    return s.lower().strip("_")


def read_data(path: Path, sheet_name: str = DEFAULT_SHEET) -> pd.DataFrame:
    path = path.resolve()
    if not path.is_file():
        raise SystemExit(f"File not found: {path}")
    if path.suffix.lower() != ".xlsx":
        raise SystemExit("Expecting .xlsx file")
    try:
        df = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    except ValueError as e:
        raise SystemExit(f"Sheet {sheet_name!r} not in workbook: {e}") from e
    df.columns = df.columns.str.strip()
    rename = {}
    for col in df.columns:
        if col in COLUMN_MAP:
            rename[col] = COLUMN_MAP[col]
        else:
            snake = _to_snake(col)
            if snake in TABLE_COLUMNS:
                rename[col] = snake
    df = df.rename(columns=rename)
    missing = [c for c in TABLE_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing expected columns after rename: {missing}")
    df = df[TABLE_COLUMNS]
    return df.where(pd.notna(df), None)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_PATH
    sheet = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_SHEET
    if not path.is_file():
        raise SystemExit(f"Data file not found: {path}. Use: python scripts/load_data.py [path.xlsx] [sheet_name]")
    df = read_data(path, sheet_name=sheet)
    print(f"Read {len(df)} rows from {path} (sheet={sheet!r})")
    engine = get_engine()
    table_name = get_table_name()
    df.to_sql(table_name, engine, if_exists="append", index=False, method="multi", chunksize=5000)
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT count(*) FROM {table_name}")).scalar()
    print(f"Done. Total rows in {table_name}: {count}")


if __name__ == "__main__":
    main()
