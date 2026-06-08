from typing import Any


class SummaryEngine:
    async def generate_executive_summary(self, meeting_data: dict[str, Any]) -> str:
        return "[Resumen ejecutivo generado por IA]"

    async def extract_action_items(self, transcript: str) -> list[dict[str, Any]]:
        return [
            {"task": "Revisar presupuesto", "assignee": None, "deadline": "2026-06-30"},
        ]
