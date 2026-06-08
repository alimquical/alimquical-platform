from typing import Optional


class LeadManager:
    def __init__(self):
        self.leads = {}

    def add_lead(self, name: str, email: str, source: str = "web", score: int = 0) -> dict:
        lead_id = f"lead_{len(self.leads) + 1}"
        lead = {
            "id": lead_id,
            "name": name,
            "email": email,
            "source": source,
            "score": score,
            "status": "new",
            "created_at": "2026-06-15",
        }
        self.leads[lead_id] = lead
        return lead

    def qualify_lead(self, lead_id: str, score: int) -> Optional[dict]:
        if lead_id in self.leads:
            self.leads[lead_id]["score"] = score
            self.leads[lead_id]["status"] = "qualified" if score >= 50 else "nurturing"
            return self.leads[lead_id]
        return None
