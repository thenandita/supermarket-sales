#!/usr/bin/env python3
"""Create supermarket_sales table from SQLModel. Run from project root: python scripts/create_tables.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sqlmodel import SQLModel

from config import get_engine, get_table_name
from models import SupermarketSale  # noqa: F401 — register table


def main():
    SQLModel.metadata.create_all(get_engine())
    print(f"Tables created: {get_table_name()}.")


if __name__ == "__main__":
    main()
