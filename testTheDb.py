import expenses

expenses.add_expense(9.99, "Coffee", "2026-02-08", "Latte")

# Change the number to an id that exists in your database
expenses.delete_expense(1)
expenses.get_all_expenses()
expenses.update_expense(10, 12.50, "Coffee", "2026-02-09", "Big latte")

print("\nAll rows:")
for row in expenses.get_all_expenses():
    print(row)


