from typing import Any, Optional


class DecisionEngine:
    def __init__(self):
        self.confidence_threshold = 0.7

    async def analyze(self, request: str, context: dict[str, Any]) -> dict[str, Any]:
        request_lower = request.lower()

        intents = {
            "reunion": ["agendar", "reunión", "reunion", "cita", "junta"],
            "analisis": ["analizar", "analisis", "evaluar", "conclusion"],
            "documento": ["crear", "documento", "reporte", "informe", "pdf"],
            "cliente": ["cliente", "crm", "contacto", "proveedor"],
            "agenda": ["calendario", "recordatorio", "programar"],
            "legal": ["contrato", "legal", "acuerdo", "cláusula"],
            "financiero": ["presupuesto", "costo", "financiero", "pago"],
            "notificacion": ["whatsapp", "correo", "notificar", "telegram"],
            "venta": ["venta", "prospecto", "oportunidad", "pipeline"],
            "busqueda": ["buscar", "encontrar", "memoria", "documentación"],
        }

        detected_intents = []
        for intent, keywords in intents.items():
            if any(kw in request_lower for kw in keywords):
                detected_intents.append(intent)

        primary_intent = detected_intents[0] if detected_intents else "busqueda"
        confidence = min(0.5 + len(detected_intents) * 0.15, 0.95) if detected_intents else 0.3

        return {
            "intent": primary_intent,
            "confidence": confidence,
            "requires_clarification": confidence < self.confidence_threshold,
            "detected_intents": detected_intents,
        }
