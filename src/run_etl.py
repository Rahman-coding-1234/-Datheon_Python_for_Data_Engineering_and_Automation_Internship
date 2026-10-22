from src.extract import extract
from src.transform import transform
from src.loader import load
from src.verify import verify

if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    count = load(clean)
    print(f"Loaded {count} rows into data/app.db")
    verify()