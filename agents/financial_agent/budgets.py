from typing import Any


class BudgetManager:
    def __init__(self):
        self.budgets = {}

    def create_budget(self, name: str, amount: float, category: str) -> dict[str, Any]:
        budget_id = f"bgt_{len(self.budgets) + 1}"
        budget = {"id": budget_id, "name": name, "amount": amount, "category": category, "spent": 0}
        self.budgets[budget_id] = budget
        return budget

    def get_remaining(self, budget_id: str) -> float:
        budget = self.budgets.get(budget_id)
        if budget:
            return budget["amount"] - budget["spent"]
        return 0.0
