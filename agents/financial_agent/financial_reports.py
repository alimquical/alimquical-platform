from typing import Any


class FinancialReportGenerator:
    def generate_report(self, period: str, data: dict) -> dict[str, Any]:
        return {
            "period": period,
            "revenue": data.get("revenue", 0),
            "expenses": data.get("expenses", 0),
            "profit_margin": 0.15,
            "key_metrics": {"roi": 1.25, "cac": 500, "ltv": 5000},
        }

    def generate_invoice(self, client: str, items: list[dict], tax: float = 0.16) -> dict:
        subtotal = sum(item["amount"] for item in items)
        return {
            "client": client,
            "items": items,
            "subtotal": subtotal,
            "tax": subtotal * tax,
            "total": subtotal * (1 + tax),
        }
