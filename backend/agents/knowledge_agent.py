from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse, AgentContext
from .memory import AgentMemory
from .memory.corporate_memory import CorporateMemory, VectorMemory
from services.llm import llm
from sqlalchemy.orm import Session
from core.database import SessionLocal

KNOWLEDGE_PROMPT = """Eres el KNOWLEDGE AGENT de INTELLIWORK™, la memoria corporativa del sistema.

Tienes acceso a una base vectorial que almacena toda la información histórica:
- Reuniones (transcripciones, actas, compromisos)
- Documentos (contratos, informes, propuestas)
- Clientes (perfiles, historial, interacciones)
- Decisiones y acuerdos
- Proyectos y tareas

Tu función es responder preguntas sobre información pasada usando el contexto disponible.
Responde en español citando las fuentes cuando sea posible."""


class KnowledgeAgent(BaseAgent):
    role = AgentRole.KNOWLEDGE
    name = "Knowledge Agent"
    description = "Memoria corporativa y búsqueda histórica"

    def get_system_prompt(self) -> str:
        return KNOWLEDGE_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        query = request.params.get("query", request.action)
        context = request.context
        if not context:
            return AgentResponse(success=False, error="Contexto requerido")

        db = SessionLocal()
        try:
            memory = CorporateMemory(context.company_id, db)
            context_docs = memory.query_with_context(query)

            full_prompt = self.get_system_prompt()
            if context_docs:
                full_prompt += f"\n\nContexto histórico encontrado:\n{context_docs}"

            if llm.is_available():
                result = llm.chat(full_prompt, query)
                if result:
                    return AgentResponse(success=True, message=result, data={"agent": self.role.value})
            return AgentResponse(success=False, error="LLM no disponible")
        finally:
            db.close()
