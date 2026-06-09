from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse
from .memory import AgentMemory
from services.llm import llm

PROVIDER_PROMPT = """Eres el PROVIDER INTELLIGENCE AGENT de INTELLIWORK™.

Tus capacidades:
- Gestionar perfiles completos de proveedores
- Evaluar desempeño y riesgos
- Detectar dependencias críticas
- Identificar oportunidades de negociación
- Analizar acuerdos y contratos
- Recomendar acciones estratégicas

Responde en español de forma profesional y analítica."""


class ProviderAgent(BaseAgent):
    role = AgentRole.PROVIDER
    name = "Provider Intelligence Agent"
    description = "Gestión inteligente de proveedores"

    def get_system_prompt(self) -> str:
        return PROVIDER_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        action = request.params.get("action", request.action)

        if action == "evaluate":
            return await self._evaluate(request.params)
        elif action == "risk_analysis":
            return await self._risk_analysis(request.params)
        else:
            return await self._chat(request)

    async def _evaluate(self, params: dict) -> AgentResponse:
        provider_name = params.get("name", "")
        history = params.get("history", "")
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt(), f"Evalúa al proveedor {provider_name}:\n{history}")
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})

    async def _risk_analysis(self, params: dict) -> AgentResponse:
        context = params.get("context", "")
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt() + "\n\nAnaliza riesgos y dependencias:", context)
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})

    async def _chat(self, request: AgentRequest) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt(), request.params.get("query", request.action))
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})
