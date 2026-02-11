import sqlite3

DB_PATH = "data/expenses.db"


# Adds an expense.
def add_expense(amount, category, date, note):
    """Add one expense to the database."""
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date, note)
    )

    conn.commit()
    conn.close()

    print("Expense added!")


#removes the id specified
def delete_expense(expense_id):
    """Delete one expense by its id."""
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
)

    conn.commit()
    conn.close()

    print(f"Deleted expense {expense_id}")

#updates the specified id expense
def update_expense(expense_id, amount, category, date, note):
    conn = sqlite3.connect(DB_PATH)

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


#Returns all the rows in expenses
def get_all_expenses():    
    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute("SELECT * FROM expenses").fetchall()

    conn.close()
    return rows

def get_expenses_by_category(category):
    conn = sqlite3.connect(DB_PATH)
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
