import matplotlib.pyplot as plt
import csv


class PriorityQueueBudget:
    def __init__(self, budget):
        self.budget = budget
        self.items = []

    def add_item(self, name, cost, priority):
        self.items.append((priority, name, cost))

    def priority_label(self, p):
        return {
            1: "Essential",
            2: "Important",
            3: "Optional"
        }.get(p, "Unknown")

    def get_sorted_items(self):
        return sorted(self.items, key=lambda x: (x[0], x[2]))

    def plan_purchases(self):
        remaining_budget = self.budget
        bought = []
        skipped = []

        for priority, name, cost in self.get_sorted_items():
            if cost <= remaining_budget:
                bought.append((name, cost, priority))
                remaining_budget -= cost
            else:
                skipped.append((name, cost, priority))

        return bought, skipped, remaining_budget

    def show_plan(self):
        if not self.items:
            print("\n⚠ No items added yet. Please add items first.")
            return

        bought, skipped, remaining = self.plan_purchases()

        print("\n========== PURCHASE PLAN ==========")

        total_spent = sum(cost for _, cost, _ in bought)
        usage = (total_spent / self.budget) * 100 if self.budget > 0 else 0

      
      
        print("\nItems to BUY:")
        if bought:
            for name, cost, priority in bought:
                print(f" + {name} | ৳{cost} | {self.priority_label(priority)}")
        else:
            print(" None")


        
        print("\n------------- SUMMARY -------------")
        print(f"Budget         : {self.budget}")
        print(f"Total Spent    : {total_spent}")
        print(f"Remaining      : {remaining}")
        print(f"Usage          : {usage:.2f}%")
        print("-----------------------------------")

        self.show_pie_chart(total_spent, remaining)

    def show_pie_chart(self, spent, remaining):
        if spent == 0 and remaining == 0:
            print("No data to display.")
            return

        labels = ["Spent", "Remaining"]
        values = [spent, remaining]

        plt.figure()
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Budget Usage")
        plt.show()

    def export_csv(self, filename="budget_plan.csv"):
        bought, skipped, remaining = self.plan_purchases()

        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Name", "Cost", "Priority"])

            for name, cost, priority in bought:
                writer.writerow(["BUY", name, cost, self.priority_label(priority)])

            for name, cost, priority in skipped:
                writer.writerow(["SKIP", name, cost, self.priority_label(priority)])

        print(f"\n Plan exported successfully to '{filename}'")


# ---------------- MAIN PROGRAM ---------------- #

def run_priority_queue():
    while True:
        user_input = input("\nEnter Budget (or 'b' to go back): ")

        if user_input.lower() == 'b':
            return

        try:
            budget = float(user_input)
            if budget <= 0:
                print(" Budget must be greater than 0.")
                continue
            break
        except ValueError:
            print(" Invalid input. Please enter a number.")

    planner = PriorityQueueBudget(budget)

    while True:
        print("\n--- Priority Queue Planner ---")
        print("1. Add Item")
        print("2. Show Plan")
        print("3. Export CSV")
        print("4. Back")

        choice = input("Choice: ")

        if choice == "1":
            name = input("Item Name: ")

            try:
                cost = float(input("Cost: "))
                if cost <= 0:
                    print("⚠ Cost must be positive.")
                    continue
            except ValueError:
                print("⚠ Invalid cost.")
                continue

            try:
                priority = int(input("Priority (1=Essential, 2=Important, 3=Optional): "))
                if priority not in [1, 2, 3]:
                    print("⚠ Invalid priority.")
                    continue
            except ValueError:
                print("⚠ Invalid priority.")
                continue

            planner.add_item(name, cost, priority)
            print(" Item added successfully!")

        elif choice == "2":
            planner.show_plan()

        elif choice == "3":
            planner.export_csv()

        elif choice == "4":
            print("Returning to main menu...")
            break

        else:
            print(" Invalid choice.")


# Run
if __name__ == "__main__":
    run_priority_queue()