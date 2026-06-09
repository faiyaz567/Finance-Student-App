class FinancialProfile:
    def __init__(self, monthly_income, existing_debts):
        self.monthly_income = monthly_income
        self.existing_debts = existing_debts

    def total_debt(self, new_loan_emi=0):
        return self.existing_debts + new_loan_emi

    def dti_ratio(self, total_debt):
        return (total_debt / self.monthly_income) * 100


# polymorphism
class DTIAlertStrategy:
    def evaluate(self, profile, new_loan_emi):
        raise NotImplementedError


class StandardStrategy(DTIAlertStrategy):
    def evaluate(self, profile, new_loan_emi):
        total_debt = profile.total_debt(new_loan_emi)
        dti = profile.dti_ratio(total_debt)

        if dti <= 30:
            status = "SAFE"
        elif dti <= 40:
            status = "WARNING"
        else:
            status = "RED FLAG"

        return {
            "DTI %": round(dti, 2),
            "Status": status
        }


# inheritance
class DTIAnalyzer(FinancialProfile):
    def check(self, new_loan_emi, strategy):
        result = strategy.evaluate(self, new_loan_emi)

        print("=== DTI RATIO ANALYSIS ===\n")

        # FORMULA OUTPUT
        print("DTI Formula:")
        print("DTI (%) = (Total Monthly Debt / Monthly Income) × 100\n")

        print(f"Monthly Income: {self.monthly_income}")
        print(f"Existing Debts: {self.existing_debts}")
        print(f"New Loan EMI: {new_loan_emi}\n")

        for k, v in result.items():
            print(f"{k}: {v}")

        print("\n=== INTERPRETATION ===")
        if result["Status"] == "RED FLAG":
            print(" High risk: Debt burden too high.")
        elif result["Status"] == "WARNING":
            print(" Caution: Approaching risky debt level.")
        else:
            print(" Healthy Debt Level.")
