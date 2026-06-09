import csv
import os


class BalanceOverview:
    def __init__(self, income_file="income_data.csv", expense_file="expense_data.csv"):
        self.income_file = income_file
        self.expense_file = expense_file

    def get_total_income(self):
        total = 0

        if os.path.exists(self.income_file):
            with open(self.income_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        total += float(row["amount"])
                    except:
                        continue

        return total

    def get_total_expense(self):
        total = 0

        if os.path.exists(self.expense_file):
            with open(self.expense_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        total += float(row["amount"])
                    except:
                        continue

        return total

    def get_balance(self):
        return self.get_total_income() - self.get_total_expense()

    def show_balance(self):
        income = self.get_total_income()
        expense = self.get_total_expense()
        balance = income - expense

        print("\n====== BALANCE OVERVIEW ======")

        print("\n Income Sources:")
        if os.path.exists(self.income_file):
            with open(self.income_file, "r", newline="") as file:
                reader = csv.DictReader(file)

                has_data = False
                for row in reader:
                    has_data = True
                    print(f" + {row['source']} : {row['amount']} ({row['date']})")

                if not has_data:
                    print(" No income records found.")
        else:
            print(" No income file found.")

        print("\n  Expenses:")
        if os.path.exists(self.expense_file):
            with open(self.expense_file, "r", newline="") as file:
                reader = csv.DictReader(file)

                has_data = False
                for row in reader:
                    has_data = True
                    print(f" - {row['category']} : {row['amount']} ({row['date']})")

                if not has_data:
                    print(" No expense records found.")
        else:
            print(" No expense file found.")

       
        print("\n----------- RESULT -----------")
        print(f"Total Income : {income}")
        print(f"Total Expense: {expense}")
        print(f"Balance      : {balance}")
        print("------------------------------")