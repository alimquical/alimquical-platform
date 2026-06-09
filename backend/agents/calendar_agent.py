from sqlalchemy.orm import Session
from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse, AgentContext
from .memory import AgentMemory
from services.llm import llm
from core.database import SessionLocal

CALENDAR_PROMPT = """Eres el CALENDAR AGENT de INTELLIWORK™.

Tus capacidades:
- Gestionar la agenda y calendario
- Detectar conflictos de horarios
- Sugerir horarios óptimos para reuniones
- Recordar eventos próximos
- Integrar con Google Calendar
- Confirmar asistencia

Responde en español de forma clara."""


class CalendarAgent(BaseAgent):
    role = AgentRole.CALENDAR
    name = "Calendar Agent"
    description = "Gestión de agenda, calendario y conflictos"

    def get_system_prompt(self) -> str:
        return CALENDAR_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        action = request.params.get("action", request.action)
        context = request.context

        if action == "check_conflicts":
            return await self._check_conflicts(request.params, context)
        elif action == "suggest_slot":
            return await self._suggest_slot(request.params, context)
        elif action == "upcoming":
            return await self._upcoming(context)
        else:
            return await self._chat(request)

    async def _check_conflicts(self, params: dict, context: AgentContext) -> AgentResponse:
        date_str = params.get("date", "")
        time_str = params.get("time", "")
        if not context:
            return AgentResponse(success=False, error="Contexto requerido")
        db = SessionLocal()
        try:
            from models.meeting import Meeting
            conflicts = db.query(Meeting).filter(Meeting.company_id == context.company_id, Meeting.status == "scheduled").count()
            msg = f"Reuniones programadas: {conflicts}"
            if llm.is_available():
                result = llm.chat(self.get_system_prompt(), f"Analiza conflictos de agenda:\n{msg}")
                return AgentResponse(success=True, message=result or msg, data={"scheduled": conflicts})
            return AgentResponse(success=True, message=msg)
        finally:
            db.close()

    async def _suggest_slot(self, params: dict, context: AgentContext) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        duration = params.get("duration", "1 hora")
        result = llm.chat(self.get_system_prompt(), f"Sugiere horarios disponibles para una reunión de {duration}")
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})

    async def _upcoming(self, context: AgentContext) -> AgentResponse:
        if not context:
            return AgentResponse(success=False, error="Contexto requerido")
        db = SessionLocal()
        try:
            from models.meeting import Meeting
            from datetime import datetime, timezone
            upcoming = db.query(Meeting).filter(Meeting.company_id == context.company_id, Meeting.date >= datetime.now(timezone.utc)).order_by(Meeting.date).limit(10).all()
            if not upcoming:
                return AgentResponse(success=True, message="No hay eventos próximos")
            events = "\n".join([f"- {m.title} ({m.date})" for m in upcoming])
            if llm.is_available():
                result = llm.chat(self.get_system_prompt(), f"Resumen de agenda próxima:\n{events}")
                return AgentResponse(success=True, message=result or events, data={"upcoming_count": len(upcoming)})
            return AgentResponse(success=True, message=events)
        finally:
            db.close()

    async def _chat(self, request: AgentRequest) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt(), request.params.get("query", request.action))
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})
