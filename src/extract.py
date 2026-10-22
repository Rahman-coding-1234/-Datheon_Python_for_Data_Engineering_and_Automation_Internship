import pandas as pd

RAW_PATH = "data/customers_raw.csv"

def extract(path: str = RAW_PATH) -> pd.DataFrame:
    """Read the raw customer CSV and return it as a DataFrame."""
    df = pd.read_csv(path)
    def extract(path: str = RAW_PATH) -> pd.DataFrame:
    """Read the raw customer CSV and return it as a DataFrame."""
    df = pd.read_csv(path)
    return df
    return df

if __name__ == "__main__":
    print(extract().head())