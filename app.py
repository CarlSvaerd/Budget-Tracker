import expenses
from datetime import datetime, date


def get_int(prompt):
    while True:
        text = input(prompt).strip()
        try:
            return int(text)
        except ValueError:
            print("Please enter a whole number (example: 3).")


def get_float(prompt):
    while True:
        text = input(prompt).strip().replace(",", ".")
        try:
            value = float(text)
            if value < 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a number (example: 12.50).")


def get_date(prompt):
    while True:
        text = input(prompt).strip()

        # shortcuts for today
        if text == "" or text.strip() in ("t", "today","T","Today"):
            return date.today().isoformat() 

        try:
            # Enforce YYYY-MM-DD
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Please enter a date like YYYY-MM-DD, or press Enter for today")

def get_yes_no(prompt):
    while True:
        ans = input(prompt).strip()
        if ans in ("y", "yes","Yes","YES"):
            return True
        if ans in ("n", "no","No","NO"):
            return False
        print("Please type y/n.")


def print_expenses(rows):
    if not rows:
        print("\nNo expenses found.")
        return

    print("\nID | Amount | Category | Date       | Note")
    print("-" * 55)

    total = 0.0
    for (id_, amount, category, date, note) in rows:
        total += float(amount)
        note = note if note is not None else ""
        print(f"{id_:>2} | {amount:>6.2f} | {category:<8} | {date} | {note}")

    print("-" * 55)
    print(f"Total spent: {total:.2f}")


def menu():
    print("\n=== Expense Tracker ===")
    print("1) Add expense")
    print("2) List all expenses")
    print("3) List expenses by category")
    print("4) Update expense")
    print("5) Delete expense")
    print("6) Exit")


while True:
    menu()
    choice = input("Choose: ").strip()

    if choice == "1":
        amount = get_float("Amount: ")
        category = input("Category: ").strip()
        date = get_date("Date (YYYY-MM-DD): ")
        note = input("Note (optional): ").strip()
        if note == "":
            note = None
        expenses.add_expense(amount, category, date, note)

    elif choice == "2":
        rows = expenses.get_all_expenses()
        print_expenses(rows)

    elif choice == "3":
        category = input("Category to search: ").strip()
        rows = expenses.get_expenses_by_category(category)
        print_expenses(rows)

    elif choice == "4":
        expense_id = get_int("ID to update: ")
        amount = get_float("New amount: ")
        category = input("New category: ").strip()
        date = get_date("New date (YYYY-MM-DD): ")
        note = input("New note (optional): ").strip()
        if note == "":
            note = None
        expenses.update_expense(expense_id, amount, category, date, note)

    elif choice == "5":
        expense_id = get_int("ID to delete: ")
        if get_yes_no(f"Are you sure you want to delete {expense_id}? (y/n): "):
            expenses.delete_expense(expense_id)
        else:
            print("Delete cancelled.")

    elif choice == "6":
        print("Bye!")
        break

    else:
        print("Invalid choice. Try 1-6.")
