from typing import Any


class CashFlowManager:
    def __init__(self):
        self.transactions = []

    def record_transaction(self, description: str, amount: float, type: str = "expense", category: str = "general") -> dict[str, Any]:
        transaction = {
            "id": f"txn_{len(self.transactions) + 1}",
            "description": description,
            "amount": amount,
            "type": type,
            "category": category,
            "date": "2026-06-15",
        }
        self.transactions.append(transaction)
        return transaction

    def get_balance(self) -> dict[str, Any]:
        income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        return {"income": income, "expenses": expenses, "balance": income - expenses}
