import pandas as pd
from src.loader import load

df = pd.DataFrame({
    "customer_id": [1, 2, 3],
    "name": ["Asha", "Ravi", "Meena"],
    "email": ["asha@example.com", "ravi@example.com", "meena@example.com"],
    "updated_at": ["2026-10-22", "2026-10-22", "2026-10-22"],
})

print("First run:", load(df))
print("Second run:", load(df))