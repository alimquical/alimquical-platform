from typing import Any


class LegalReviewer:
    def review_contract(self, contract: dict) -> dict[str, Any]:
        return {
            "contract_id": contract.get("id"),
            "issues": [],
            "risk_level": "low",
            "recommendations": ["Revisar cláusula de confidencialidad"],
        }

    def check_compliance(self, document: str, regulation: str = "ISO 9001") -> dict[str, Any]:
        return {"compliant": True, "findings": [], "regulation": regulation}
