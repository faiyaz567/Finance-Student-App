import matplotlib.pyplot as plt

class EMIPlanner:
    def __init__(self, principal, annual_rate, tenure_years):
        self.principal = principal
        self.annual_rate = annual_rate
        self.tenure_years = tenure_years

        self.monthly_rate = annual_rate / 12 / 100
        self.total_months = int(round(tenure_years * 12))

    def calculate_emi(self):
        P = self.principal
        r = self.monthly_rate
        n = self.total_months

        if r == 0:
            return P / n

        return (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)

    def amortization_schedule(self):
        emi = self.calculate_emi()
        balance = self.principal

        schedule = []
        total_interest = 0

        for month in range(1, self.total_months + 1):
            interest = balance * self.monthly_rate
            principal_paid = emi - interest
            balance -= principal_paid

            total_interest += interest

            schedule.append({
                "Month": month,
                "Balance": max(balance, 0),
                "Interest": interest,
                "Principal": principal_paid
            })

        return schedule, total_interest
    def summary(self):
        emi = self.calculate_emi()
        schedule, total_interest = self.amortization_schedule()

        print(f"\nMonthly EMI: {round(emi, 2)}")
        print(f"Total Interest Paid: {round(total_interest, 2)}")
        print(f"Total Payment: {round(emi * self.total_months, 2)}")

        print("\nFirst 12 months:")
        for row in schedule[:12]:
            print(row)

    def plot_graphs(self):
        schedule, _ = self.amortization_schedule()

        months = [row["Month"] for row in schedule]
        balance = [row["Balance"] for row in schedule]
        interest = [row["Interest"] for row in schedule]
        principal = [row["Principal"] for row in schedule]

        plt.figure()
        plt.plot(months, balance)
        plt.title("Loan Balance Over Time")
        plt.xlabel("Months")
        plt.ylabel("Remaining Balance")
        plt.show()

        plt.figure()
        plt.plot(months, interest)
        plt.plot(months, principal)
        plt.title("Interest vs Principal")
        plt.xlabel("Months")
        plt.ylabel("Amount")
        plt.show()