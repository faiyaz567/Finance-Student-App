class RunningCostTracker:
    def __init__(self, monthly_km):
        self.monthly_km = monthly_km

        # monthly expense categories
        self.fuel = 0
        self.servicing = 0
        self.tyres = 0
        self.tolls = 0

    def set_costs(self, fuel, servicing, tyres, tolls):
        self.fuel = fuel
        self.servicing = servicing
        self.tyres = tyres
        self.tolls = tolls

    def total_monthly_cost(self):
        return self.fuel + self.servicing + self.tyres + self.tolls

    def cost_per_km(self):
        if self.monthly_km == 0:
            return 0
        return self.total_monthly_cost() / self.monthly_km

    def report(self):
        total = self.total_monthly_cost()
        cpk = self.cost_per_km()

        print("=== MONTHLY RUNNING COST REPORT ===\n")

        print(f"Fuel Cost: {self.fuel}")
        print(f"Servicing Cost: {self.servicing}")
        print(f"Tyres Cost: {self.tyres}")
        print(f"Tolls: {self.tolls}\n")

        print(f"Total Monthly Cost: {total}")
        print(f"Monthly Distance (km): {self.monthly_km}")
        print(f"Cost per km: {round(cpk, 2)}")

        print("\n=== INSIGHT ===")
        if cpk > 20:
            print(" High running cost per km")
        elif cpk > 10:
            print(" Moderate running cost")
        else:
            print(" Efficient usage cost")
