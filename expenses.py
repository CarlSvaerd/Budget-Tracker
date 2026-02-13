from database import get_connection


def add_expense(amount, category, date, note):
    conn = get_connection()

    conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date, note)
    )

    conn.commit()
    conn.close()
    print("Expense added!")


def get_total_spent(category=None):
    conn = get_connection()

    if category:
        row = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = ?",
            (category,),
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses"
        ).fetchone()

    conn.close()
    return float(row[0])

def get_category_totals():
    conn = get_connection()

    rows = conn.execute("""
        SELECT category, COALESCE(SUM(amount), 0) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    conn.close()
    return rows

def delete_expense(expense_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()
    print(f"Deleted expense {expense_id}")


def update_expense(expense_id, amount, category, date, note):
    conn = get_connection()

    conn.execute(
        """
        UPDATE expenses
        SET amount = ?, category = ?, date = ?, note = ?
        WHERE id = ?
        """,
        (amount, category, date, note, expense_id)
    )

    conn.commit()
    conn.close()
    print(f"Updated expense {expense_id}")


def get_all_expenses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    return rows


def get_expenses_by_category(category):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT id, amount, category, date, note
        FROM expenses
        WHERE category = ?
        ORDER BY date DESC, id DESC
        """,
        (category,),
    ).fetchall()

    conn.close()
    return rows
def get_expense_by_id(expense_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, amount, date, category, note FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()
    conn.close()
    return row
