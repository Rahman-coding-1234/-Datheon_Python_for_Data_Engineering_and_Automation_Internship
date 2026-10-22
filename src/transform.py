import pandas as pd

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw customer data so it can be loaded safely."""
    out = df.copy()

    # 1. Remove leading/trailing spaces in text columns
    for col in ["name", "email"]:
        out[col] = out[col].str.strip()

    # 2. Drop rows without a name (name is NOT NULL in the database)
    out = out.dropna(subset=["name"])

    # 3. Keep only the latest record per customer_id
    out["updated_at"] = pd.to_datetime(out["updated_at"])
    out = out.sort_values("updated_at").drop_duplicates(subset=["customer_id"], keep="last")

    # 4. Convert dates back to text for SQLite
    out["updated_at"] = out["updated_at"].dt.strftime("%Y-%m-%d")

    # 5. Missing emails become None (stored as NULL)
    out["email"] = out["email"].where(out["email"].notna(), None)

    return out.reset_index(drop=True)

if __name__ == "__main__":
    from src.extract import extract
    print(transform(extract()))