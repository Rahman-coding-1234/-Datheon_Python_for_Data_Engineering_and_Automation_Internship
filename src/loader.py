import sqlite3
import pandas as pd

DB_PATH = "data/app.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT,
    updated_at  TEXT
);
"""

UPSERT_SQL = """
INSERT INTO customers (customer_id, name, email, updated_at)
VALUES (?, ?, ?, ?)
ON CONFLICT(customer_id) DO UPDATE SET
    name       = excluded.name,
    email      = excluded.email,
    updated_at = excluded.updated_at;
"""

def load(df: pd.DataFrame, db_path: str = DB_PATH) -> int:
    """Insert new rows or update existing ones. Returns number of rows processed."""
    rows = list(df[["customer_id", "name", "email", "updated_at"]].itertuples(index=False, name=None))
    conn = sqlite3.connect(db_path)
    try:
        with conn:  # transaction: commit if all good, rollback if error
            conn.execute(CREATE_TABLE_SQL)
            conn.executemany(UPSERT_SQL, rows)
        return len(rows)
    finally:
        conn.close()