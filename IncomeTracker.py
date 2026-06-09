import csv
import os
from datetime import datetime

class IncomeTracker:
    def __init__(self, filename="income_data.csv"):
        self.filename = filename
        self.incomes = []
        self.load_data()

    # FILE HANDLING 
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                self.incomes = []
                for row in reader:
                    self.incomes.append({
                        "id": int(row["id"]),
                        "source": row["source"],
                        "amount": float(row["amount"]),
                        "date": row["date"]
                    })
        else:
            self.incomes = []

    def save_data(self):
        with open(self.filename, "w", newline="") as file:
            fieldnames = ["id", "source", "amount", "date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for entry in self.incomes:
                writer.writerow(entry)

    #  CORE FEATURES 
    def add_income(self, source, amount, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        new_id = 1 if not self.incomes else max(e["id"] for e in self.incomes) + 1

        entry = {
            "id": new_id,
            "source": source,
            "amount": float(amount),
            "date": date
        }

        self.incomes.append(entry)
        self.save_data()
        print("Income added and saved to CSV!")

    def view_income(self):
        if not self.incomes:
            print("No income records found.")
            return

        for entry in self.incomes:
            print(f"ID: {entry['id']} | {entry['date']} | {entry['source']} | {entry['amount']}")

    def edit_income(self, entry_id, new_source=None, new_amount=None, new_date=None):
        for entry in self.incomes:
            if entry["id"] == entry_id:
                if new_source:
                    entry["source"] = new_source
                if new_amount is not None:
                    entry["amount"] = float(new_amount)
                if new_date:
                    entry["date"] = new_date

                self.save_data()
                print("Income updated!")
                return

        print("Entry not found.")

    def delete_income(self, entry_id):
        for entry in self.incomes:
            if entry["id"] == entry_id:
                self.incomes.remove(entry)
                self.save_data()
                print("Income deleted!")
                return

        print("Entry not found.")

    #  MONTHLY SUMMARY 
    def monthly_summary(self, year, month):
         total = 0
         print(f"\nSummary for {year}-{str(month).zfill(2)}:")

         for entry in self.incomes:
             try:
              entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
             except:
                 print(f"Skipped invalid date: {entry['date']}")
                 continue

             if entry_date.year == year and entry_date.month == month:
                print(f"{entry['date']} | {entry['source']} | {entry['amount']}")
                total += entry["amount"]
         print(f"Total Income: {total}")