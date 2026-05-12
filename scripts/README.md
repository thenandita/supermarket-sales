# Database scripts

**SQLModel** (schema) + **pandas** `to_sql` (load) + **Pydantic settings** (config). Python only.

## Prerequisites

- DB running: `db/start.sh`. Copy `db/.env.example` to `db/.env` and adjust if needed.
- Excel file at `data/supermarket-analysis.xlsx` (transactional sheet **SuperMarket Analysis**), or pass a path.
- Dependencies: `pip install -r requirements.txt` (project `.venv` recommended).

## Commands (from project root `supermarket-sales/`)

```bash
./create_tables.sh                              # create supermarket_sales table
./load_data.sh                                  # load default file + sheet
./load_data.sh path/to/other.xlsx               # custom workbook (same sheet name unless second arg set)
./load_data.sh path/to/file.xlsx "Sheet Name" # custom path and sheet
./verify_data.sh                                # verify row/column counts vs source
./verify_data.sh path/to/file.xlsx "Sheet Name"
```

Or: `.venv/bin/python scripts/create_tables.py`, `scripts/load_data.py [path] [sheet]`, `scripts/verify_data.py [path] [sheet]`.

Re-running `load_data` **appends**. Truncate the table for a clean reload.

## Layout

| File | Role |
|------|------|
| `config.py` | Settings from `db/.env` (DB + `TABLE_NAME`), engine, `get_table_name()` |
| `models.py` | SQLModel table `SupermarketSale` |
| `create_tables.py` | Create table from metadata |
| `load_data.py` | Read .xlsx (default sheet `SuperMarket Analysis`), bulk insert via `to_sql` |
| `verify_data.py` | Compare source file vs DB (row count, non-null per column) |

**Default table:** `supermarket_sales` (override with `TABLE_NAME` in `db/.env`).

The workbook also has a **sales** pivot sheet; loads use **SuperMarket Analysis** unless you pass another sheet name.
