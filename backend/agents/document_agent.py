from sqlalchemy.orm import Session
from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse
from .memory import AgentMemory
from services.llm import llm
from core.database import SessionLocal

DOCUMENT_PROMPT = """Eres el DOCUMENT INTELLIGENCE AGENT de INTELLIWORK™.

Tus capacidades:
- Crear documentos profesionales (informes, actas, contratos, propuestas, cotizaciones)
- Editar y mejorar documentos existentes
- Clasificar documentos automáticamente
- Buscar documentos por contenido semántico
- Generar documentos completos desde especificaciones

Responde en español con formato profesional."""


class DocumentAgent(BaseAgent):
    role = AgentRole.DOCUMENT
    name = "Document Intelligence Agent"
    description = "Creación, edición y búsqueda inteligente de documentos"

    def get_system_prompt(self) -> str:
        return DOCUMENT_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        action = request.params.get("action", request.action)

        if action == "generate":
            return await self._generate(request.params)
        elif action == "classify":
            return await self._classify(request.params)
        else:
            return await self._chat(request)

    async def _generate(self, params: dict) -> AgentResponse:
        doc_type = params.get("doc_type", "informe")
        topic = params.get("topic", "")
        details = params.get("details", "")
        if not topic or not llm.is_available():
            return AgentResponse(success=False, error="Tema o LLM no disponible")
        prompt = f"Genera un {doc_type} profesional sobre: {topic}\n\nDetalles adicionales: {details}"
        result = llm.chat(self.get_system_prompt(), prompt)
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value, "doc_type": doc_type})

    async def _classify(self, params: dict) -> AgentResponse:
        content = params.get("content", "")
        if not content or not llm.is_available():
            return AgentResponse(success=False, error="Contenido o LLM no disponible")
        result = llm.chat(self.get_system_prompt() + "\n\nClasifica el siguiente documento por tipo y extrae palabras clave.", content)
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})

    async def _chat(self, request: AgentRequest) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt(), request.params.get("query", request.action))
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})
