import csv
import os
from datetime import datetime

class DataExporter:
    def __init__(self, income_file="income_data.csv", expense_file="expense_data.csv"):
        self.income_file = income_file
        self.expense_file = expense_file

    #  EXPORT INCOME 
    def export_income(self, output_file=None):
        if output_file is None:
            output_file = f"income_export_{datetime.now().strftime('%Y%m%d')}.csv"

        if not os.path.exists(self.income_file):
            print("No income data found.")
            return

        with open(self.income_file, "r", newline="") as infile:
            reader = csv.DictReader(infile)
            data = list(reader)

        with open(output_file, "w", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=["id", "source", "amount", "date"])
            writer.writeheader()
            writer.writerows(data)

        print(f"Income exported to {output_file}")

    #EXPORT EXPENSE 
    def export_expenses(self, output_file=None):
        if output_file is None:
            output_file = f"expense_export_{datetime.now().strftime('%Y%m%d')}.csv"

        if not os.path.exists(self.expense_file):
            print("No expense data found.")
            return

        with open(self.expense_file, "r", newline="") as infile:
            reader = csv.DictReader(infile)
            data = list(reader)

        with open(output_file, "w", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=["id", "category", "amount", "date"])
            writer.writeheader()
            writer.writerows(data)

        print(f"Expenses exported to {output_file}")

    #EXPORT BOTH
    def export_all(self):
        self.export_income()
        self.export_expenses()
