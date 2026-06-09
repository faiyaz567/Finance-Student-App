import csv
import os


class WhatIfSimulator:
    def __init__(self, expense_file="expense_data.csv"):
        self.expense_file = expense_file

        # Essential categories
        self.essentials = ["rent", "food", "transport"]

    #  LOAD MONTHLY EXPENSES 
    def get_monthly_expenses(self):
        totals = {}

        if not os.path.exists(self.expense_file):
            return totals

        with open(self.expense_file, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                category = row["category"]
                amount = float(row["amount"])

                totals[category] = totals.get(category, 0) + amount

        return totals

    #  SIMULATION 
    def simulate_purchase(self, purchase_amount, category="fun", monthly_budget=0):

        print("\nEnter your essential monthly expenses:")
        rent = float(input("Rent: "))
        food = float(input("Food: "))
        transport = float(input("Transport: "))

        # base expenses
        expenses = {
            "rent": rent,
            "food": food,
            "transport": transport
        }
        use_saved = input("Include previous saved expenses? (y/n): ").lower()

        if use_saved == "y":
            past_expenses = self.get_monthly_expenses()
            for cat, amt in past_expenses.items():
                expenses[cat] = expenses.get(cat, 0) + amt
        expenses[category] = expenses.get(category, 0) + float(purchase_amount)

        total_spent = sum(expenses.values())

        #  OUTPUT 
        print("\n--- WHAT IF YOU BUY THIS? ---")
        print(f"Purchase added to: {category}")
        print(f"Purchase amount  : {purchase_amount}")

        print("\n--- NEW MONTHLY SPENDING ---")
        for cat, amt in expenses.items():
            print(f"{cat}: {round(amt, 2)}")

        print(f"\nTotal spending: {round(total_spent, 2)}")

        #  ESSENTIAL CHECK 
        print("\n--- ESSENTIALS CHECK ---")
        risk = False

        for essential in self.essentials:
            amt = expenses.get(essential, 0)
            print(f"{essential}: {round(amt, 2)}")

            if monthly_budget > 0 and amt > monthly_budget * 0.5:
                print(f" WARNING: {essential} is consuming too much budget!")
                risk = True

        #  FINAL DECISION 
        if risk:
            print("\n RISK: Essentials are too high. Budget imbalance likely.")
        elif monthly_budget > 0 and total_spent > monthly_budget:
            print("\n OVER BUDGET: You will exceed your monthly budget.")
        else:
            print("\n SAFE: Purchase seems financially manageable.")