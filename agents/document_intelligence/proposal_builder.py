from typing import Any


class ProposalBuilder:
    def create_proposal(self, client_name: str, services: list[dict], pricing: dict) -> dict[str, Any]:
        return {
            "client": client_name,
            "services": services,
            "total": pricing.get("total", 0),
            "valid_until": "2026-07-15",
            "payment_terms": "Net 30",
        }
