from flask import Flask, render_template, request, redirect, url_for
import expenses
from database import get_connection

app = Flask(__name__)

@app.get("/")
def home():
    return '<h1>Expense Tracker</h1><p>Go to <a href="/expenses">/expenses</a></p>'

@app.get("/expenses")
def list_expenses():
    category = request.args.get("category", "").strip()

    if category:
        rows = expenses.get_expenses_by_category(category)
        total = expenses.get_total_spent(category)
    else:
        rows = expenses.get_all_expenses()
        total = expenses.get_total_spent()

    category_totals = expenses.get_category_totals()

    return render_template(
        "Site.html",
        rows=rows,
        category=category,
        total=total,
        category_totals=category_totals
    )



@app.route("/expenses/new", methods=["GET", "POST"])
def new_expense():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"]
        note = request.form["note"] or None

        expenses.add_expense(amount, category, date, note)

        return redirect(url_for("list_expenses"))

    return render_template("new_expense.html")

@app.post("/expenses/<int:expense_id>/delete")
def delete_expense(expense_id):
    expenses.delete_expense(expense_id)
    return redirect(url_for("list_expenses"))


@app.route("/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
def edit_expense(expense_id):
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"]
        note = request.form["note"] or None

        expenses.update_expense(expense_id, amount, category, date, note)
        return redirect(url_for("list_expenses"))

    row = expenses.get_expense_by_id(expense_id)
    if row is None:
        return "Not found", 404

    return render_template("edit_expense.html", r=row)



if __name__ == "__main__":
    app.run(debug=True)
