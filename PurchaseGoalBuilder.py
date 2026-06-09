import csv
import os
from datetime import datetime


class PurchaseGoal:
    def __init__(self, filename="goals_data.csv"):
        self.filename = filename
        self.goals = []
        self.load_goals()

    # LOAD GOALS
    def load_goals(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                self.goals = list(reader)
        else:
            self.goals = []

    # SAVE GOALS
    def save_goals(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["item", "target_price", "deadline"])
            writer.writeheader()
            writer.writerows(self.goals)

    # ADD GOAL
    def add_goal(self, item, target_price, deadline):
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except:
            print(" Invalid date format! Use YYYY-MM-DD")
            return

        goal = {
            "item": item,
            "target_price": float(target_price),
            "deadline": deadline
        }

        self.goals.append(goal)
        self.save_goals()
        print(f" Goal saved: {item}")

    # VIEW GOALS
    def view_goals(self):
        if not self.goals:
            print("No goals found.")
            return

        print("\n--- SAVED GOALS ---")
        for g in self.goals:
            print(f"{g['item']} | {g['target_price']} | {g['deadline']}")

    # CALCULATE PLAN
    def calculate_goal_plan(self, item):
        today = datetime.now()

        for g in self.goals:
            if g["item"].lower() == item.lower():

                target = float(g["target_price"])
                deadline = datetime.strptime(g["deadline"], "%Y-%m-%d")

                if deadline <= today:
                    print(" Deadline already passed!")
                    return

                days_left = (deadline - today).days

                # Avoid division by zero
                if days_left <= 0:
                    print(" No time left!")
                    return

                weeks_left = days_left / 7
                months_left = days_left / 30

                daily = target / days_left
                weekly = target / weeks_left if weeks_left >= 1 else None
                monthly = target / months_left if months_left >= 1 else None

                print("\n--- GOAL PLAN ---")
                print(f"Item     : {g['item']}")
                print(f"Target   : {target}")
                print(f"Deadline : {g['deadline']}")
                print(f"Days Left: {days_left}")

                print("\n Saving Plan:")
                print(f" Per day   : {daily:.2f}")

                if weekly:
                    print(f" Per week  : {weekly:.2f}")
                else:
                    print(" Per week  : Not applicable (too few days)")

                if monthly:
                    print(f" Per month : {monthly:.2f}")
                else:
                    print(" Per month : Not applicable (too few days)")

                return

        print(" Goal not found.")