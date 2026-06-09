from sqlalchemy.orm import Session
from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse, AgentContext
from .memory import AgentMemory
from services.llm import llm
from core.database import SessionLocal

CRM_PROMPT = """Eres el CRM INTELLIGENCE AGENT de INTELLIWORK™.

Tus capacidades:
- Gestionar perfiles completos de clientes
- Analizar historial de interacciones y reuniones
- Identificar oportunidades comerciales
- Detectar seguimientos pendientes
- Responder preguntas contextuales sobre clientes
- Recomendar acciones basadas en el estado comercial

Responde en español de forma profesional."""


class CRMAgent(BaseAgent):
    role = AgentRole.CRM
    name = "CRM Intelligence Agent"
    description = "Gestión inteligente de clientes y oportunidades"

    def get_system_prompt(self) -> str:
        return CRM_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        action = request.params.get("action", request.action)
        context = request.context

        if action == "customer_summary":
            return await self._customer_summary(request.params, context)
        elif action == "pending_followups":
            return await self._pending_followups(context)
        elif action == "opportunities":
            return await self._opportunities(request.params, context)
        else:
            return await self._chat(request)

    async def _customer_summary(self, params: dict, context: AgentContext) -> AgentResponse:
        client_id = params.get("client_id", "")
        if not client_id or not context:
            return AgentResponse(success=False, error="Cliente o contexto requerido")
        db = SessionLocal()
        try:
            from models.client import Client
            from models.meeting import Meeting
            from models.task import Task
            client = db.query(Client).filter(Client.id == client_id, Client.company_id == context.company_id).first()
            if not client:
                return AgentResponse(success=False, error="Cliente no encontrado")
            meetings = db.query(Meeting).filter(Meeting.company_id == context.company_id).order_by(Meeting.date.desc()).limit(5).all()
            tasks = db.query(Task).filter(Task.company_id == context.company_id, Task.status != "done").limit(5).all()
            info = f"Cliente: {client.name}\nEmail: {client.email}\nTeléfono: {client.phone}\nEstado: {client.status.value}\nContactos: {client.deals_count}\nÚltimo contacto: {client.last_contact}\n\nReuniones recientes: {len(meetings)}\nTareas pendientes: {len(tasks)}"
            if llm.is_available():
                result = llm.chat(self.get_system_prompt(), f"Genera un resumen ejecutivo del cliente:\n{info}")
                return AgentResponse(success=True, message=result or info, data={"client_id": client_id})
            return AgentResponse(success=True, message=info)
        finally:
            db.close()

    async def _pending_followups(self, context: AgentContext) -> AgentResponse:
        if not context:
            return AgentResponse(success=False, error="Contexto requerido")
        db = SessionLocal()
        try:
            from models.task import Task
            pending = db.query(Task).filter(Task.company_id == context.company_id, Task.status == "todo").count()
            msg = f"Seguimientos pendientes: {pending}"
            if llm.is_available():
                result = llm.chat(self.get_system_prompt(), f"Genera recomendaciones basadas en: {msg}")
                return AgentResponse(success=True, message=result or msg, data={"pending": pending})
            return AgentResponse(success=True, message=msg)
        finally:
            db.close()

    async def _opportunities(self, params: dict, context: AgentContext) -> AgentResponse:
        if not context:
            return AgentResponse(success=False, error="Contexto requerido")
        db = SessionLocal()
        try:
            from models.client import Client
            leads = db.query(Client).filter(Client.company_id == context.company_id, Client.status == "lead").count()
            msg = f"Oportunidades identificadas: {leads} clientes en estado LEAD"
            if llm.is_available():
                result = llm.chat(self.get_system_prompt(), f"Analiza estas oportunidades:\n{msg}")
                return AgentResponse(success=True, message=result or msg, data={"leads": leads})
            return AgentResponse(success=True, message=msg)
        finally:
            db.close()

    async def _chat(self, request: AgentRequest) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt(), request.params.get("query", request.action))
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})
