import sqlite3
from pathlib import Path

# 1) Ensure the data folder exists
Path("data").mkdir(exist_ok=True)

# 2) Create/open the database file
conn = sqlite3.connect("data/expenses.db")

# 3) Create the table (if it doesn't already exist)
conn.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    note TEXT
);
""")

# 4) Save and close
conn.commit()
conn.close()

print("Database ready: data/expenses.db")
