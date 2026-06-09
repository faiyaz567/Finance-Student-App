import csv
import os
from datetime import datetime

class MonthlyBudget:
    def __init__(self, budget_file="budget_data.csv", expense_file="expense_data.csv"):
        self.budget_file = budget_file
        self.expense_file = expense_file
        self.budgets = []
        self.load_budgets()

    #  LOAD / SAVE BUDGETS 
    def load_budgets(self):
        if os.path.exists(self.budget_file):
            with open(self.budget_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                self.budgets = []
                for row in reader:
                    self.budgets.append({
                        "month": row["month"],   # format: YYYY-MM
                        "limit": float(row["limit"])
                    })
        else:
            self.budgets = []

    def save_budgets(self):
        with open(self.budget_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["month", "limit"])
            writer.writeheader()
            for b in self.budgets:
                writer.writerow(b)

    #  SET BUDGET FOR MONTH 
    def set_budget(self, year, month, limit):
        month_key = f"{year}-{str(month).zfill(2)}"
        for b in self.budgets:
            if b["month"] == month_key:
                b["limit"] = float(limit)
                self.save_budgets()
                print(f"Updated budget for {month_key}")
                return
        self.budgets.append({
            "month": month_key,
            "limit": float(limit)
        })

        self.save_budgets()
        print(f"Budget set for {month_key}")

    #  GET BUDGET 
    def get_budget(self, year, month):
        month_key = f"{year}-{str(month).zfill(2)}"

        for b in self.budgets:
            if b["month"] == month_key:
                return b["limit"]

        return None

    #  MONTHLY EXPENSE 
    def get_monthly_expense(self, year, month):
        total = 0

        if not os.path.exists(self.expense_file):
            return total

        with open(self.expense_file, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    d = datetime.strptime(row["date"], "%Y-%m-%d")
                except:
                    continue

                if d.year == year and d.month == month:
                    total += float(row["amount"])

        return total

    #  AUTO CHECK CURRENT MONTH 
    def check_current_month(self):
        now = datetime.now()
        year, month = now.year, now.month

        limit = self.get_budget(year, month)

        if limit is None or limit == 0:
            print("No valid budget set for this month.")
            return

        spent = self.get_monthly_expense(year, month)

        # Prevent insane percentage
        usage = (spent / limit) * 100
        display_usage = min(usage, 999)  

        print(f"\n--- Budget Status ({year}-{str(month).zfill(2)}) ---")
        print(f"Limit : {limit}")
        print(f"Spent : {spent}")

        # Smart display
        if usage > 999:
            print("Usage : 999%+ (EXTREME OVERSPENDING)")
        else:
            print(f"Usage : {display_usage:.2f}%")

        # Warnings
        if spent > limit:
            overspend = spent - limit
            print(f" Budget exceeded by {overspend}!")
        elif usage >= 80:
            print(" Warning: 80% of budget used.")
        else:
            print(" Budget is safe.")