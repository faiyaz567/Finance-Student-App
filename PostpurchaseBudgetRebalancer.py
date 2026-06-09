import pandas as pd
import numpy as np


class PostPurchaseBudgetRebalancer:
    def __init__(self, monthly_income, categories):
        """
        categories = dict like:
        {
            "rent": 15000,
            "food": 10000,
            "dining": 5000,
            "subscriptions": 2000,
            "transport": 3000
        }
        """
        self.monthly_income = monthly_income
        self.categories = categories

        # DataFrame
        self.df = pd.DataFrame(list(categories.items()), columns=["Category", "Budget"])

    def apply_purchase(self, purchase_amount):
        print("\n Post-Purchase Budget Rebalancing")
        print("-----------------------------------")

        remaining_income = self.monthly_income - purchase_amount

        if remaining_income < 0:
            print(" WARNING: Purchase exceeds monthly income!")
            remaining_income = 0

        print(f"Income after purchase: {remaining_income}")

        if self.monthly_income == 0:
            reduction_ratio = 0
        else:
            reduction_ratio = remaining_income / self.monthly_income
        flexible = ["dining", "subscriptions", "entertainment"]

        adjusted_budgets = []

        for _, row in self.df.iterrows():
            category = row["Category"]
            budget = row["Budget"]

            if category in flexible:
                new_budget = budget * reduction_ratio * 0.8
            else:
                new_budget = budget

            adjusted_budgets.append(new_budget)

        self.df["Adjusted Budget"] = np.round(adjusted_budgets, 2)

    def show_plan(self):
        print("\n Budget Rebalance Plan")
        print(self.df)

    def export_csv(self, filename="rebalance_plan.csv"):
        self.df.to_csv(filename, index=False)
        print(f"\n Saved to {filename}")
