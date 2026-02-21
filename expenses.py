from database import get_connection
from datetime import datetime


CURRENT_USER_ID = 1

DEFAULT_CATEGORIES = [
    "Groceries", "Rent", "Utilities", "Transportation", "Dining",
    "Entertainment", "Healthcare", "Insurance", "Education",
    "Subscriptions", "Misc"
]


def add_expense(amount, category, date, note):
    user_id = CURRENT_USER_ID

    amount = verify_amount(amount)
    category = verify_category_name(category)
    date = _validate_date(date)
    note = _clean_note(note)

    category_id = get_or_create_category_id(user_id, category)

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO expenses (user_id, category_id, amount, date, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, category_id, amount, date, note),
        )
        conn.commit()
    finally:
        conn.close()

def _clean_note(note):
    note = (note or "").strip()
    if len(note) > 200:
        raise ValueError("Note is too long (max 200 characters)")
    return note



def verify_category_name(name: str) -> str:
    name = (name or "").strip()
    name = " ".join(name.split())

    if not name:
        raise ValueError("Category name cannot be empty")
    if name.isdigit():
        raise ValueError("Category name cannot be only numbers")
    if len(name) > 30:
        raise ValueError("Category name is too long (max 30 characters)")

    return name
def add_category(name):
    name = verify_category_name(name)

    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT OR IGNORE INTO categories (user_id, name) VALUES (?, ?)",
            (CURRENT_USER_ID, name),
        )
        conn.commit()

        return cur.rowcount == 1
    finally:
        conn.close()

def get_total_spent(category=None):
    conn = get_connection()

    if category:
        row = conn.execute("""
            SELECT COALESCE(SUM(e.amount), 0)
            FROM expenses e
            JOIN categories c ON c.id = e.category_id
            WHERE e.user_id = ? AND c.name = ?
        """, (CURRENT_USER_ID, category)).fetchone()
    else:
        row = conn.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = ?
        """, (CURRENT_USER_ID,)).fetchone()

    conn.close()
    return float(row[0])


def ensure_default_categories():
    conn = get_connection()
    for name in DEFAULT_CATEGORIES:
        conn.execute(
            "INSERT OR IGNORE INTO categories (user_id, name) VALUES (?, ?)",
            (CURRENT_USER_ID, name),
        )
    conn.commit()
    conn.close()


def get_category_totals():
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.name AS category, COALESCE(SUM(e.amount), 0) AS total
        FROM expenses e
        JOIN categories c ON c.id = e.category_id
        WHERE e.user_id = ?
        GROUP BY c.name
        ORDER BY total DESC
    """, (CURRENT_USER_ID,)).fetchall()
    conn.close()
    return rows


def delete_expense(expense_id):
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM expenses WHERE id = ? AND user_id = ?",
            (expense_id, CURRENT_USER_ID),
        )
        conn.commit()
        return cur.rowcount == 1
    finally:
        conn.close()

def verify_amount(amount):
    try:
        value = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number")
    if value <= 0:
        raise ValueError("Amount must be greater than 0")
    return value

def _validate_date(date_str):
    if date_str is None:
        raise ValueError("Date is required")

    date_str = str(date_str).strip()
    if not date_str:
        raise ValueError("Date is required")

    parts = date_str.split("-")
    if len(parts) != 3 or any(not p.isdigit() for p in parts):
        raise ValueError("Date must be in YYYY-MM-DD format")

    year = int(parts[0])
    if year < 1900 or year > 2100:
        raise ValueError("Year must be between 1900 and 2100")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date")

    return date_str

def update_expense(expense_id, amount, category, date, note):
    user_id = CURRENT_USER_ID

    amount = verify_amount(amount)
    category = verify_category_name(category)
    date = _validate_date(date)
    note = _clean_note(note)

    category_id = get_or_create_category_id(user_id, category)

    conn = get_connection()
    try:
        cur =conn.execute(
            """
            UPDATE expenses
            SET amount = ?, date = ?, note = ?, category_id = ?
            WHERE id = ? AND user_id = ?
            """,
            (amount, date, note, category_id, expense_id, user_id),
        )
        conn.commit()
        return cur.rowcount == 1
    finally:
        conn.close()

    
def get_categories():
    conn = get_connection()
    rows = conn.execute(
        "SELECT name FROM categories WHERE user_id = ? ORDER BY name",
        (CURRENT_USER_ID,),
    ).fetchall()
    conn.close()
    return rows


def get_all_expenses():
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT e.id, e.amount, e.date, c.name AS category, e.note
        FROM expenses e
        JOIN categories c ON c.id = e.category_id
        WHERE e.user_id = ?
        ORDER BY e.date DESC, e.id DESC
        """,
        (CURRENT_USER_ID,),
    ).fetchall()
    conn.close()
    return rows


def get_expenses_by_category(category):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT e.id, e.amount, e.date, c.name AS category, e.note
        FROM expenses e
        JOIN categories c ON c.id = e.category_id
        WHERE e.user_id = ? AND c.name = ?
        ORDER BY e.date DESC, e.id DESC
        """,
        (CURRENT_USER_ID, category),
    ).fetchall()
    conn.close()
    return rows

def get_expense_by_id(expense_id):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT e.id, e.amount, e.date, c.name AS category, e.note
        FROM expenses e
        JOIN categories c ON c.id = e.category_id
        WHERE e.user_id = ? AND e.id = ?
        """,
        (CURRENT_USER_ID, expense_id),
    ).fetchone()
    conn.close()
    return row

def get_or_create_category_id(user_id, category_name):
    category_name = verify_category_name(category_name)

    conn = get_connection()
    #COLLATE NOCASE allows us to treat "Groceries" and "groceries" as the same category
    try:
        row = conn.execute(
            "SELECT id FROM categories WHERE user_id = ? AND name = ? COLLATE NOCASE",
            (user_id, category_name),
        ).fetchone()

        if row:
            conn.close()
            return row[0]

        conn.execute(
            "INSERT INTO categories (user_id, name) VALUES (?, ?)",
            (user_id, category_name),
        )
        conn.commit()

        new_id = conn.execute(
            "SELECT id FROM categories WHERE user_id = ? AND name = ? COLLATE NOCASE",
            (user_id, category_name),
        ).fetchone()[0]
        return new_id
    finally:
        conn.close()
  

