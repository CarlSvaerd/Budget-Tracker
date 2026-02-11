import sqlite3
from pathlib import Path

Path("data").mkdir(exist_ok=True)

conn = sqlite3.connect("data/expenses.db")

with open("schema.sql") as f:
    conn.executescript(f.read())

conn.close()

print("Database initialized!")
