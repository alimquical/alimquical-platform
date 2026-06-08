from typing import Optional


class OpportunityManager:
    def __init__(self):
        self.opportunities = {}

    def create(self, client_id: str, title: str, value: float, stage: str = "prospecting") -> dict:
        opp_id = f"opp_{len(self.opportunities) + 1}"
        opp = {
            "id": opp_id,
            "client_id": client_id,
            "title": title,
            "value": value,
            "stage": stage,
            "probability": self._get_probability(stage),
        }
        self.opportunities[opp_id] = opp
        return opp

    def _get_probability(self, stage: str) -> float:
        probabilities = {
            "prospecting": 0.1,
            "qualification": 0.25,
            "proposal": 0.5,
            "negotiation": 0.75,
            "closed_won": 1.0,
        }
        return probabilities.get(stage, 0.1)
