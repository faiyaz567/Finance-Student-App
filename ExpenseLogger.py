import csv
import os
from datetime import datetime

class ExpenseLogger:
    def __init__(self, filename="expense_data.csv"):
        self.filename = filename
        self.expenses = []
        self.categories = ["food", "transport", "rent", "books", "fun"]
        self.load_data()

    #  FILE HANDLING 
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                self.expenses = []
                for row in reader:
                    self.expenses.append({
                        "id": int(row["id"]),
                        "category": row["category"],
                        "amount": float(row["amount"]),
                        "date": row["date"]
                    })
        else:
            self.expenses = []

    def save_data(self):
        with open(self.filename, "w", newline="") as file:
            fieldnames = ["id", "category", "amount", "date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for entry in self.expenses:
                writer.writerow(entry)

    #  CORE FEATURES 
    def add_expense(self, category, amount, date=None):
        if category not in self.categories:
            print("Invalid category!")
            return

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        new_id = 1 if not self.expenses else max(e["id"] for e in self.expenses) + 1

        entry = {
            "id": new_id,
            "category": category,
            "amount": float(amount),
            "date": date
        }

        self.expenses.append(entry)
        self.save_data()
        print("Expense added and saved!")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
            return

        for e in self.expenses:
            print(f"ID: {e['id']} | {e['date']} | {e['category']} | {e['amount']}")

    def edit_expense(self, entry_id, new_category=None, new_amount=None, new_date=None):
        for e in self.expenses:
            if e["id"] == entry_id:
                if new_category:
                    if new_category in self.categories:
                        e["category"] = new_category
                    else:
                        print("Invalid category!")
                        return
                if new_amount is not None:
                    e["amount"] = float(new_amount)
                if new_date:
                    e["date"] = new_date

                self.save_data()
                print("Expense updated!")
                return

        print("Entry not found.")

    def delete_expense(self, entry_id):
        for e in self.expenses:
            if e["id"] == entry_id:
                self.expenses.remove(e)
                self.save_data()
                print("Expense deleted!")
                return

        print("Entry not found.")

    #  MONTHLY SUMMARY 
    def monthly_summary(self, year, month):
        total = 0
        print(f"\nExpense Summary for {year}-{str(month).zfill(2)}:")

        for e in self.expenses:
            try:
                d = datetime.strptime(e["date"], "%Y-%m-%d")
            except:
                print(f"Skipped invalid date: {e['date']}")
                continue

            if d.year == year and d.month == month:
                print(f"{e['date']} | {e['category']} | {e['amount']}")
                total += e["amount"]

        print(f"Total Expenses: {total}")