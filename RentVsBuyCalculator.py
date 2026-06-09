class RentVsBuyCalculator:
    def __init__(self, buy_price, rent_monthly_cost):
        self.buy_price = buy_price
        self.rent_monthly_cost = rent_monthly_cost

    def break_even_months(self):
        if self.rent_monthly_cost == 0:
            return float('inf')

        return self.buy_price / self.rent_monthly_cost

    def compare(self, months=36):
        break_even = self.break_even_months()

        total_rent_cost = self.rent_monthly_cost * months
        buy_cost = self.buy_price

        print("Rent vs Buy Comparison")
        print("----------------------")
        print(f"Buy Price: {buy_cost}")
        print(f"Monthly Rent Cost: {self.rent_monthly_cost}")
        print(f"Break-even point: {break_even:.2f} months")

        print(f"\nCost after {months} months:")
        print(f"- Buy option total: {buy_cost}")
        print(f"- Rent option total: {total_rent_cost}")

        if break_even <= months:
            print("\n Buying becomes cheaper after break-even point.")
        else:
            print("\n Renting is cheaper within this time frame.")