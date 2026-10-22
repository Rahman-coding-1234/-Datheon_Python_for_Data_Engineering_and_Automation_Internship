import sqlite3

DB_PATH = "data/app.db"

CHECKS = {
    "total_rows": "SELECT COUNT(*) FROM customers;",
    "duplicate_ids": """
        SELECT COUNT(*) FROM (
            SELECT customer_id FROM customers
            GROUP BY customer_id HAVING COUNT(*) > 1
        );
    """,
    "null_names": "SELECT COUNT(*) FROM customers WHERE name IS NULL;",
}

def verify(db_path: str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    try:
        for label, sql in CHECKS.items():
            value = conn.execute(sql).fetchone()[0]
            print(f"{label}: {value}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify()