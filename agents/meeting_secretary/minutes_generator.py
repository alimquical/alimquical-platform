from typing import Optional


class MinutesGenerator:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.api_key = openai_api_key

    async def generate(self, transcript: str, title: str) -> dict:
        minutes = {
            "title": title,
            "date": "2026-06-15",
            "summary": "[Resumen generado por IA - Integrar con OpenAI]",
            "key_points": ["Punto 1", "Punto 2", "Punto 3"],
            "action_items": ["Acción 1", "Acción 2"],
            "decisions": ["Decisión 1"],
            "next_steps": ["Siguiente paso 1"],
        }
        return minutes
