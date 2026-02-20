from flask import Flask, render_template, request, redirect, url_for,flash
import expenses
from database import get_connection

app = Flask(__name__)
app.secret_key = "dev"

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
    categories = expenses.get_categories()  # <- added

    return render_template(
        "Site.html",
        rows=rows,
        category=category,
        total=total,
        category_totals=category_totals,
        categories=categories,  # <- added
    )

@app.route("/expenses/new", methods=["GET", "POST"])
def new_expense():
    if request.method == "POST":
        raw_amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()
        note = request.form.get("note", "").strip() or None

        if not raw_amount:
            flash("Amount is required.")
            return redirect(url_for("new_expense"))

        try:
            amount = float(raw_amount)
        except ValueError:
            flash("Amount must be a number.")
            return redirect(url_for("new_expense"))

        if amount <= 0:
            flash("Amount must be greater than 0.")
            return redirect(url_for("new_expense"))

        if not category:
            flash("Category is required.")
            return redirect(url_for("new_expense"))

        if not date:
            flash("Date is required.")
            return redirect(url_for("new_expense"))

        expenses.add_expense(amount, category, date, note)
        flash("Expense added ✅")
        return redirect(url_for("list_expenses"))

    expenses.ensure_default_categories()
    categories = expenses.get_categories()
    return render_template("new_expense.html", categories=categories)

@app.post("/expenses/<int:expense_id>/delete")
def delete_expense(expense_id):
    expenses.delete_expense(expense_id)
    flash("Expense deleted ")
    return redirect(url_for("list_expenses"))

@app.route("/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
def edit_expense(expense_id):
    if request.method == "POST":
        raw_amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()
        note = request.form.get("note", "").strip() or None

        if not raw_amount:
            flash("Amount is required.")
            return redirect(url_for("edit_expense", expense_id=expense_id))

        try:
            amount = float(raw_amount)
        except ValueError:
            flash("Amount must be a number.")
            return redirect(url_for("edit_expense", expense_id=expense_id))

        if amount <= 0:
            flash("Amount must be greater than 0.")
            return redirect(url_for("edit_expense", expense_id=expense_id))

        if not category:
            flash("Category is required.")
            return redirect(url_for("edit_expense", expense_id=expense_id))

        if not date:
            flash("Date is required.")
            return redirect(url_for("edit_expense", expense_id=expense_id))

        expenses.update_expense(expense_id, amount, category, date, note)
        flash("Expense updated")
        return redirect(url_for("list_expenses"))

    row = expenses.get_expense_by_id(expense_id)
    if row is None:
        return "Not found", 404

    expenses.ensure_default_categories()
    categories = expenses.get_categories()
    return render_template("edit_expense.html", r=row, categories=categories)

@app.get("/categories")
def list_categories():
    expenses.ensure_default_categories()
    categories = expenses.get_categories()
    return render_template("categories.html", categories=categories)

@app.route("/categories", methods=["POST"])
def create_category():
    name = request.form.get("name", "").strip()
    try:
        expenses.add_category(name)
        flash("Category added!", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("list_categories"))


if __name__ == "__main__":
    app.run(debug=True)
