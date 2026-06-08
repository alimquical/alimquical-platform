from typing import Any


class BusinessAnalyzer:
    async def analyze_meeting(self, transcript: str, summary: str) -> dict[str, Any]:
        return {
            "key_topics": ["Topic 1", "Topic 2"],
            "sentiment": "positive",
            "engagement_score": 0.85,
            "recommendations": ["Recomendación 1"],
        }

    async def analyze_trends(self, data: list[dict]) -> dict[str, Any]:
        return {
            "trends": ["Tendencia 1"],
            "growth_rate": 0.12,
            "seasonal_patterns": [],
        }
