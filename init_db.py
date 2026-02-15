import sqlite3
from pathlib import Path

Path("data").mkdir(exist_ok=True)

db_path = Path("data/expenses.db")

if db_path.exists():
    print("Database already exists. Refusing to overwrite.")
    exit()

conn = sqlite3.connect(db_path)

with open("schema.sql", "r", encoding="utf-8") as f:
    conn.executescript(f.read())
row = conn.execute("SELECT id FROM users WHERE id = 1").fetchone()
if row is None:
    conn.execute("INSERT INTO users (id, name) VALUES (1, 'Demo User')")
    conn.commit()

# seed default standardized categories for the demo user
default_categories = [
    "Groceries", "Rent", "Utilities", "Transportation", "Dining",
    "Entertainment", "Healthcare", "Insurance", "Education",
    "Subscriptions", "Misc"
]

for cat in default_categories:
    existing = conn.execute(
        "SELECT id FROM categories WHERE user_id = ? AND name = ?",
        (1, cat),
    ).fetchone()
    if existing is None:
        conn.execute(
            "INSERT INTO categories (user_id, name) VALUES (?, ?)",
            (1, cat),
        )

conn.commit()
conn.close()

print("Database initialized!")