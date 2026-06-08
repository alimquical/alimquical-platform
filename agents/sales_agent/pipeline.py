from typing import Any, Optional


class PipelineManager:
    def __init__(self):
        self.deals = {}

    def add_deal(self, lead_id: str, title: str, value: float, stage: str = "prospecting") -> dict[str, Any]:
        deal_id = f"deal_{len(self.deals) + 1}"
        deal = {
            "id": deal_id,
            "lead_id": lead_id,
            "title": title,
            "value": value,
            "stage": stage,
            "probability": self._get_probability(stage),
        }
        self.deals[deal_id] = deal
        return deal

    def _get_probability(self, stage: str) -> float:
        probs = {"prospecting": 0.1, "qualification": 0.25, "proposal": 0.5, "negotiation": 0.75, "closed_won": 1.0}
        return probs.get(stage, 0.1)

    def get_pipeline_value(self) -> dict[str, Any]:
        total = sum(d["value"] * d["probability"] for d in self.deals.values())
        return {"total_weighted": total, "deals_count": len(self.deals)}
