import requests
from IncomeTracker import IncomeTracker
from ExpenseLogger import ExpenseLogger
from BalanceOverview import BalanceOverview


class StudentBudgetChatbot:
    def __init__(self):
        self.income  = IncomeTracker()
        self.expense = ExpenseLogger()
        self.balance = BalanceOverview()

        # API KEY HERE
        self.api_key = "AIzaSyBrEAfagVcNnowZxx4v_8uzd8exFasrS10"
        #

        # tries each model in order until one works
        self.models = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
        ]

        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/"
        self.active_model = None   # will be set on first successful call

        self.system_prompt = """
You are Budget Buddy — a casual, warm, and super helpful student finance assistant. 🎓💸

YOUR PERSONALITY:
- Talk like a friendly older sibling who happens to be great with money
- Keep it simple, short, and encouraging — never lecture or judge
- Use emojis naturally (not excessively)
- Responses should be SHORT (2–4 sentences) unless the user asks for something detailed like an EMI calculation
- Always make the student feel good — even if they overspent, stay positive and helpful

WHAT YOU CAN DO (guide users through each of these):
1. LOG INCOME     → tell them: add income <amount> <source>       example: add income 5000 scholarship
2. LOG EXPENSE    → tell them: add expense <amount> <category>    example: add expense 200 food
3. CHECK BALANCE  → use the live data in square brackets to tell them their current financial status
4. SAVING TIPS    → give practical, student-friendly money-saving advice
5. EMI CALCULATOR → calculate monthly installments if they give you loan amount, duration, and interest rate
6. BUDGET ADVICE  → suggest how to split their income across categories

VALID EXPENSE CATEGORIES (always remind users if they ask):
  food, transport, rent, books, fun

COMMAND GUIDE (show this clearly whenever a user wants to log data):
  To add income  → type:  add income <amount> <source>
  To add expense → type:  add expense <amount> <category>
  Example: add income 8000 part-time job
  Example: add expense 150 transport

LIVE DATA RULE:
- The student's current financial data is always included in square brackets at the end of their message
- Always reference this data when talking about their balance, income, or expenses
- Be specific — say the actual numbers, don't be vague

ONBOARDING (first interaction or when user seems new):
- Briefly introduce yourself and list what you can help with
- Invite them to try a feature — "Want to log your first income? Just type: add income 5000 allowance 😊"

ALWAYS end your reply with either:
- A helpful follow-up question  (e.g. "Want me to suggest a budget plan based on your income?")
- A gentle nudge to try a feature (e.g. "Try logging an expense and I'll track it for you! 📝")
"""

        # bake system prompt into first exchange
        self.history = [
            {
                "role":  "user",
                "parts": [{"text": "Hi, who are you?"}]
            },
            {
                "role":  "model",
                "parts": [{"text": (
                    self.system_prompt +
                    "\n\nHey hey! 👋 I'm Budget Buddy — your personal finance pal made just for students!\n\n"
                    "Here's what I can help you with:\n"
                    "  💵  Log your income and expenses\n"
                    "  📊  Check your balance anytime\n"
                    "  💡  Get saving tips that actually work for students\n"
                    "  🔢  Calculate EMIs for loans or installments\n"
                    "  🎯  Plan a budget that fits your lifestyle\n\n"
                    "To get started, try logging your income:\n"
                    "  👉  add income 5000 allowance\n\n"
                    "Or just ask me anything — I'm all yours! 😊"
                )}]
            }
        ]

    def get_balance_summary(self):
        total_income  = self.balance.get_total_income()
        total_expense = self.balance.get_total_expense()
        balance       = self.balance.get_balance()
        return (
            f"Total Income: {total_income}, "
            f"Total Expenses: {total_expense}, "
            f"Current Balance: {balance}"
        )

    def call_model(self, model_name, body):
        url = f"{self.base_url}{model_name}:generateContent?key={self.api_key}"
        response = requests.post(url, json=body)
        return response.json()

    def ask_ai(self, user_message):
        full_message = f"{user_message}\n\n[Student's live data — {self.get_balance_summary()}]"

        self.history.append({
            "role":  "user",
            "parts": [{"text": full_message}]
        })

        body = {"contents": self.history}

        # if we already found a working model, use it directly
        if self.active_model:
            models_to_try = [self.active_model]
        else:
            models_to_try = self.models

        for model in models_to_try:
            try:
                data = self.call_model(model, body)

                if "candidates" in data:
                    reply = data["candidates"][0]["content"]["parts"][0]["text"]
                    self.active_model = model   # remember what worked
                    self.history.append({
                        "role":  "model",
                        "parts": [{"text": reply}]
                    })
                    return reply

                # check if it's a quota/not-found error → try next model
                error_msg = data.get("error", {}).get("message", "")
                if "quota" in error_msg.lower() or "not found" in error_msg.lower():
                    continue   # try next model

                # some other error → show it and stop
                print(f"Bot: ❌ Oops! Something went wrong: {error_msg}")
                self.history.pop()
                return None

            except Exception as e:
                continue

        # all models failed
        self.history.pop()
        print("Bot: 😬 All AI models are busy right now. Try again in a moment, or grab a fresh API key from https://aistudio.google.com")
        return None

    def handle_add_income(self, text):
        try:
            parts  = text.strip().split()
            amount = float(parts[2])
            source = parts[3]
            self.income.add_income(source, amount)
            print(f"Bot: 🎉 Sweet! Added {amount} from '{source}' to your income. Keep it coming!")
        except:
            print("Bot: 🤔 Hmm, that didn't quite work. Try this format:")
            print("       add income 5000 salary")

    def handle_add_expense(self, text):
        try:
            parts    = text.strip().split()
            amount   = float(parts[2])
            category = parts[3]
            self.expense.add_expense(category, amount)
            print(f"Bot: ✅ Got it! Logged {amount} under '{category}'. Every taka tracked is a win 💪")
        except:
            print("Bot: 🤔 Let me help you fix that. Here's the right format:")
            print("       add expense 300 food")
            print("     Valid categories: food, transport, rent, books, fun")

    def start(self):
        print("\n" + "="*55)
        print("   💰  Budget Buddy — Student Finance Assistant  💰")
        print("="*55)
        print("\nHey there! Welcome to Budget Buddy 👋")
        print("I'm here to help you manage your money the easy way.\n")
        print("Here's what you can do:")
        print("  💬  Chat with me — ask anything about your finances")
        print("  💵  Log income  →  add income 5000 salary")
        print("  🛒  Log expense →  add expense 300 food")
        print("  🚪  Quit        →  exit\n")
        print("-"*55 + "\n")

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("\nBot: Take care and keep saving! 💸 See you next time! 👋\n")
                break

            elif user_input.lower().startswith("add income"):
                self.handle_add_income(user_input)

            elif user_input.lower().startswith("add expense"):
                self.handle_add_expense(user_input)

            else:
                print("Bot: thinking... 🤔")
                reply = self.ask_ai(user_input)
                if reply:
                    print(f"Bot: {reply}\n")