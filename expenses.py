from database import get_connection

CURRENT_USER_ID = 1

DEFAULT_CATEGORIES = [
    "Groceries", "Rent", "Utilities", "Transportation", "Dining",
    "Entertainment", "Healthcare", "Insurance", "Education",
    "Subscriptions", "Misc"
]


def add_expense(amount, category, date, note):
    user_id = CURRENT_USER_ID
    category_id = get_or_create_category_id(user_id, category)

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO expenses (user_id, category_id, amount, date, note)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, category_id, amount, date, note),
    )
    conn.commit()
    conn.close()

def add_category(name):
    name = name.strip()
    if not name:
        raise ValueError("Category name cannot be empty")

    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO categories (user_id, name) VALUES (?, ?)",
        (CURRENT_USER_ID, name),
    )
    conn.commit()
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
    conn.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, CURRENT_USER_ID),
    )
    conn.commit()
    conn.close()

def update_expense(expense_id, amount, category, date, note):
    user_id = CURRENT_USER_ID
    category_id = get_or_create_category_id(user_id, category)

    conn = get_connection()
    conn.execute(
        """
        UPDATE expenses
        SET amount = ?, date = ?, note = ?, category_id = ?
        WHERE id = ? AND user_id = ?
        """,
        (amount, date, note, category_id, expense_id, user_id),
    )
    conn.commit()
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
    category_name = category_name.strip()

    conn = get_connection()

    row = conn.execute(
        "SELECT id FROM categories WHERE user_id = ? AND name = ?",
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
        "SELECT id FROM categories WHERE user_id = ? AND name = ?",
        (user_id, category_name),
    ).fetchone()[0]

    conn.close()
    return new_id
