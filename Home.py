from IncomeTracker import IncomeTracker
from ExpenseLogger import ExpenseLogger
from BalanceOverview import BalanceOverview
from StudentBudgetChatbot import StudentBudgetChatbot
from MonthlyBudgetLimit import MonthlyBudget
from SpendingBreakdown import ExpenseAnalyzer
from DebtToIncomeRatioAlert import DTIAnalyzer, StandardStrategy
from WhatIfIBuyNow import WhatIfSimulator
from PurchaseGoalBuilder import PurchaseGoal
from EMIPlanner import EMIPlanner
from RentVsBuyCalculator import RentVsBuyCalculator
from MonthlyRunningCost import RunningCostTracker
from PostpurchaseBudgetRebalancer import PostPurchaseBudgetRebalancer
from PriorityQueue import PriorityQueueBudget
from ExportCSV import DataExporter
from datetime import datetime

def stay_or_back():
    choice = input("\nPress Enter to continue or type 'b' to go back: ")
    return choice.lower() != "b"


# MAIN MENU
def main_menu():
    print("\n========================================")
    print("          FINANCE APP")
    print("========================================")
    print("1. Chatbot")
    print("2. Manual Mode")
    print("3. Tools & Calculators")
    print("4. Exit")
    print("========================================")


# MANUAL MODE
def manual_mode():
    income = IncomeTracker()
    expense = ExpenseLogger()
    balance = BalanceOverview()

    while True:
        print("\n--- MANUAL MODE ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Balance")
        print("4. Back")

        choice = input("Choice: ")

        if choice == "1":
            src = input("Source: ")
            amt = float(input("Amount: "))
            income.add_income(src, amt)
            balance.show_balance()
            if not stay_or_back():
                break

        elif choice == "2":
            cat = input("Category: ")
            amt = float(input("Amount: "))
            expense.add_expense(cat, amt)
            balance.show_balance()
            if not stay_or_back():
                break

        elif choice == "3":
            balance.show_balance()

        elif choice == "4":
            break


# TOOLS MENU
def tools_menu():
    while True:
        print("\n===================================")
        print("       FINANCE APP TOOLS")
        print("===================================")

        print("\n1. Monthly Budget Limit")
        print("2. Spending Breakdown")
        print("3. Debt-to-Income Alert")
        print("4. What If I Buy Now")
        print("5. Purchase Goal")
        print("6. EMI Planner")
        print("7. Rent vs Buy")
        print("8. Running Cost")
        print("9. Post Purchase Rebalance")
        print("10. Priority Queue")
        print("11. Export CSV")
        print("0. Back")

        choice = input("Choice: ")

        if choice == "1":
            run_monthly_budget()
        elif choice == "2":
            run_spending_breakdown()
        elif choice == "3":
            run_dti_alert()
        elif choice == "4":
            run_what_if()
        elif choice == "5":
            run_purchase_goal()
        elif choice == "6":
            run_emi()
        elif choice == "7":
            run_rent_vs_buy()
        elif choice == "8":
            run_running_cost()
        elif choice == "9":
            run_post_purchase()
        elif choice == "10":
            run_priority_queue()
        elif choice == "11":
            run_export_csv()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


# TOOL FUNCTIONS 

def run_monthly_budget():
    budget = MonthlyBudget()

    while True:
        limit = input("\nEnter monthly budget (b to back): ")
        if limit.lower() == "b":
            return

        budget.set_budget(datetime.now().year, datetime.now().month, float(limit))
        budget.check_current_month()

        if not stay_or_back():
            break


def run_spending_breakdown():
    analyzer = ExpenseAnalyzer()

    while True:
        analyzer.show_bar_chart()
        if not stay_or_back():
            break


def run_dti_alert():
    while True:
        income = input("Income (b to back): ")
        if income.lower() == "b":
            return

        debts = float(input("Debts: "))
        new_emi = float(input("New EMI: "))

        user = DTIAnalyzer(float(income), debts)
        strategy = StandardStrategy()
        user.check(new_emi, strategy)

        if not stay_or_back():
            break


def run_what_if():
    sim = WhatIfSimulator()

    while True:
        amount = input("Amount (b to back): ")
        if amount.lower() == "b":
            return

        category = input("Category: ")
        budget = float(input("Monthly budget: "))

        sim.simulate_purchase(float(amount), category, budget)

        if not stay_or_back():
            break


def run_purchase_goal():
    planner = PurchaseGoal()

    while True:
        print("\n--- Purchase Goal ---")
        print("1. Add Goal")
        print("2. View Goals")
        print("3. Calculate")
        print("4. Back")

        choice = input("Choice: ")

        if choice == "1":
            item = input("Item: ")
            price = float(input("Price: "))
            deadline = input("Deadline: ")
            planner.add_goal(item, price, deadline)

        elif choice == "2":
            planner.view_goals()

        elif choice == "3":
            item = input("Item: ")
            planner.calculate_goal_plan(item)

        elif choice == "4":
            break

        if not stay_or_back():
            break


def run_emi():
    while True:
        principal = input("\nLoan amount (b to back): ")
        if principal.lower() == "b":
            return

        rate = float(input("Interest rate: "))
        years = float(input("Years: "))

        loan = EMIPlanner(float(principal), rate, years)
        loan.summary()

        if input("Show graphs? (y/n): ").lower() == "y":
            loan.plot_graphs()

        if not stay_or_back():
            break


def run_rent_vs_buy():
    calc = RentVsBuyCalculator(0, 0)

    while True:
        buy = input("Buy price (b to back): ")
        if buy.lower() == "b":
            return

        rent = float(input("Monthly rent: "))
        months = int(input("Months: "))

        calc = RentVsBuyCalculator(float(buy), rent)
        calc.compare(months)

        if not stay_or_back():
            break


def run_running_cost():
    tracker = RunningCostTracker(0)

    while True:
        km = input("KM (b to back): ")
        if km.lower() == "b":
            return

        fuel = float(input("Fuel: "))
        servicing = float(input("Servicing: "))
        tyres = float(input("Tyres: "))
        tolls = float(input("Tolls: "))

        tracker = RunningCostTracker(float(km))
        tracker.set_costs(fuel, servicing, tyres, tolls)
        tracker.report()

        if not stay_or_back():
            break


def run_post_purchase():
    while True:
        income = input("Income (b to back): ")
        if income.lower() == "b":
            return

        purchase = float(input("Purchase amount: "))

        categories = {
            "rent": float(input("Rent: ")),
            "food": float(input("Food: ")),
            "dining": float(input("Dining: ")),
            "subscriptions": float(input("Subs: ")),
            "transport": float(input("Transport: "))
        }

        rebalancer = PostPurchaseBudgetRebalancer(float(income), categories)
        rebalancer.apply_purchase(purchase)
        rebalancer.show_plan()

        if not stay_or_back():
            break


def run_priority_queue():
    budget_input = input("Budget (or 'b' to back): ")
    if budget_input.lower() == "b":
        return

    try:
        budget = float(budget_input)
    except:
        print("Invalid budget.")
        return

    planner = PriorityQueueBudget(budget)

    while True:
        print("\n--- Priority Queue Planner ---")
        print("1. Add Item")
        print("2. Show Plan")
        print("3. Back")

        choice = input("Choice: ")
        if choice == "1":
            name = input("Name (b to back): ")
            if name.lower() == "b":
                continue

            cost_input = input("Cost (b to back): ")
            if cost_input.lower() == "b":
                continue

            try:
                cost = float(cost_input)
            except:
                print("Invalid cost.")
                continue

            priority_input = input("Priority (1=essential, 2=important, 3=optional): ")
            if priority_input.lower() == "b":
                continue

            try:
                priority = int(priority_input)
            except:
                print("Invalid priority.")
                continue

            planner.add_item(name, cost, priority)
        elif choice == "2":
            planner.show_plan()
        elif choice == "3":
            break

        else:
            print("Invalid choice.")


def run_export_csv():
    exporter = DataExporter()

    print("\n1. Income\n2. Expenses\n3. All")
    choice = input("Choice: ")
    print("\n--- Export CSV ---")
    if choice == "1":
        exporter.export_income()
    elif choice == "2":
        exporter.export_expenses()
    elif choice == "3":
        exporter.export_all()


# MAIN 
def main():
    print("🎓 Welcome to Finance App")

    while True:
        main_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            StudentBudgetChatbot().start()

        elif choice == "2":
            manual_mode()

        elif choice == "3":
            tools_menu()

        elif choice == "4":
            print("Goodbye 👋")
            break

        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()