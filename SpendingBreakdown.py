import csv
import os
from datetime import datetime
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


# ABSTRACTION 
class ExpenseBase(ABC):
    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def analyze(self):
        pass


#  ENCAPSULATION AND INHERITANCE
class ExpenseAnalyzer(ExpenseBase):
    def __init__(self, file="expense_data.csv"):
        self._file = file   
        self._data = []
        self.load_data()

    
    def load_data(self):
        if not os.path.exists(self._file):
            self._data = []
            return

        with open(self._file, "r", newline="") as f:
            reader = csv.DictReader(f)
            self._data = list(reader)

   
    def get_current_month_data(self):
        now = datetime.now()
        month_data = []

        for row in self._data:
            try:
                d = datetime.strptime(row["date"], "%Y-%m-%d")
                if d.year == now.year and d.month == now.month:
                    month_data.append(row)
            except:
                continue

        return month_data

    # POLYMORPHISM
    def analyze(self):
        data = self.get_current_month_data()

        breakdown = {}

        for item in data:
            category = item["category"]
            amount = float(item["amount"])

            breakdown[category] = breakdown.get(category, 0) + amount

        return breakdown

    # VISUALIZATION 
    def show_bar_chart(self):
        breakdown = self.analyze()

        if not breakdown:
            print("No data for this month.")
            return

        categories = list(breakdown.keys())
        values = list(breakdown.values())

        plt.bar(categories, values)
        plt.title("Monthly Spending Breakdown")
        plt.xlabel("Category")
        plt.ylabel("Amount Spent")

        plt.show()



class ExpenseTextReport(ExpenseAnalyzer):
    def analyze(self):
        data = self.get_current_month_data()
        breakdown = {}

        for item in data:
            breakdown[item["category"]] = breakdown.get(item["category"], 0) + float(item["amount"])

        print("\n--- TEXT REPORT ---")
        for k, v in breakdown.items():
            print(f"{k}: {v}")

        return breakdown
