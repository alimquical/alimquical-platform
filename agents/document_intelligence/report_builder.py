from typing import Any


class ReportBuilder:
    def create_meeting_report(self, meeting_data: dict[str, Any]) -> dict[str, Any]:
        return {
            "title": f"Reporte: {meeting_data.get('title', 'Sin título')}",
            "sections": ["Resumen", "Participantes", "Acuerdos", "Próximos pasos"],
            "generated_at": "2026-06-15T00:00:00",
        }

    def create_financial_report(self, financial_data: dict) -> dict:
        return {"title": "Reporte Financiero", "period": "Q2 2026"}
