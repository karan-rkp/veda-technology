
# ==========================================
# SIMPLE EXPENSE TRACKER
# Python Programming Track - Task 23
# ==========================================

import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DATA_FILE = Path("expenses.csv")

FIELDNAMES = ["date", "category", "description", "amount"]


# ------------------------------------------
# LOAD EXPENSES
# ------------------------------------------
def load_expenses():

    expenses = []

    if not DATA_FILE.exists():
        return expenses

    try:
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    date = datetime.strptime(row["date"], "%Y-%m-%d")
                    category = row["category"].strip()
                    description = row["description"].strip()
                    amount = float(row["amount"])

                    if amount <= 0 or not category or not description:
                        continue

                    expenses.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "category": category,
                        "description": description,
                        "amount": amount
                    })

                except (ValueError, KeyError, TypeError):
                    print("Warning: Skipping an invalid expense record.")

    except (OSError, csv.Error) as error:
        print(f"Error reading expense file: {error}")

    return expenses


# ------------------------------------------
# SAVE EXPENSES
# ------------------------------------------
def save_expenses(expenses):

    try:
        with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(expenses)

        return True

    except (OSError, csv.Error) as error:
        print(f"Error saving expenses: {error}")
        return False


# ------------------------------------------
# ADD EXPENSE
# ------------------------------------------
def add_expense(expenses):

    print("\n========== ADD NEW EXPENSE ==========")

    date_input = input(
        "Enter date (YYYY-MM-DD, blank for today): "
    ).strip()

    if not date_input:
        date_input = datetime.today().strftime("%Y-%m-%d")

    try:
        date = datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid date! Use YYYY-MM-DD format.")
        return

    category = input("Enter category (Food/Travel/Bills etc.): ").strip()
    description = input("Enter description: ").strip()

    if not category or not description:
        print("Category and description cannot be empty.")
        return

    try:
        amount = float(input("Enter amount (₹): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid numeric amount.")
        return

    expense = {
        "date": date.strftime("%Y-%m-%d"),
        "category": category.title(),
        "description": description,
        "amount": amount
    }

    expenses.append(expense)

    if save_expenses(expenses):
        print("\nExpense added successfully!")
        print(f"Amount: ₹{amount:,.2f}")
    else:
        # Roll back in-memory change if saving fails
        expenses.pop()
        print("Expense was not saved.")


# ------------------------------------------
# VIEW ALL EXPENSES
# ------------------------------------------
def view_expenses(expenses):

    print("\n========== ALL EXPENSES ==========")

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("-" * 78)
    print(
        f"{'Date':<13}{'Category':<16}"
        f"{'Description':<25}{'Amount (₹)':>14}"
    )
    print("-" * 78)

    for expense in sorted(expenses, key=lambda item: item["date"]):
        print(
            f"{expense['date']:<13}"
            f"{expense['category']:<16}"
            f"{expense['description'][:24]:<25}"
            f"{expense['amount']:>14,.2f}"
        )

    print("-" * 78)
    print(f"Total Spending: ₹{sum(e['amount'] for e in expenses):,.2f}")


# ------------------------------------------
# CATEGORY-WISE SUMMARY
# ------------------------------------------
def category_summary(expenses):

    print("\n========== CATEGORY-WISE SUMMARY ==========")

    if not expenses:
        print("No expense data available.")
        return

    totals = defaultdict(float)

    for expense in expenses:
        totals[expense["category"]] += expense["amount"]

    for category, total in sorted(totals.items()):
        print(f"{category:<20} ₹{total:,.2f}")

    print("-" * 40)
    print(f"{'Total Spending':<20} ₹{sum(totals.values()):,.2f}")


# ------------------------------------------
# TOTAL SPENDING REPORT
# ------------------------------------------
def total_report(expenses):

    print("\n========== TOTAL SPENDING REPORT ==========")

    if not expenses:
        print("No expense data available.")
        return

    total = sum(expense["amount"] for expense in expenses)
    average = total / len(expenses)

    print(f"Number of expenses : {len(expenses)}")
    print(f"Total spending     : ₹{total:,.2f}")
    print(f"Average expense    : ₹{average:,.2f}")
    print(f"Highest expense    : ₹{max(e['amount'] for e in expenses):,.2f}")
    print(f"Lowest expense     : ₹{min(e['amount'] for e in expenses):,.2f}")


# ------------------------------------------
# MAIN MENU
# ------------------------------------------
def main():

    expenses = load_expenses()

    print("\n======================================")
    print("         SIMPLE EXPENSE TRACKER")
    print("======================================")
    print(f"Loaded {len(expenses)} expense record(s).")

    while True:

        print("\n--------------- MENU ----------------")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category-wise Summary")
        print("4. Total Spending Report")
        print("5. Exit")
        print("-------------------------------------")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            category_summary(expenses)

        elif choice == "4":
            total_report(expenses)

        elif choice == "5":
            print("\nThank you for using Expense Tracker!")
            print("Your saved expenses will be available next time.")
            break

        else:
            print("Invalid choice! Please select 1-5.")


# ------------------------------------------
# START PROGRAM
# ------------------------------------------
if __name__ == "__main__":
    main()
