from typing import Any


class RiskDetector:
    def detect_risks(self, analysis: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {"type": "schedule", "severity": "medium", "description": "Posible retraso en entregables"},
        ]

    def detect_opportunities(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {"type": "upsell", "value": 50000, "confidence": 0.75},
        ]
