from datetime import datetime, timezone
from sqlalchemy.orm import Session
from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse, AgentContext
from .memory import AgentMemory
from services.llm import llm
from core.database import SessionLocal
from models.meeting import Meeting

MEETING_PROMPT = """Eres el MEETING INTELLIGENCE AGENT de INTELLIWORK™.

Tus capacidades:
- Analizar transcripciones de reuniones
- Generar actas y resúmenes
- Extraer compromisos, tareas y fechas
- Identificar temas y participantes
- Detectar reuniones sin informe
- Sugerir acciones de seguimiento

Responde en español de forma profesional y estructurada."""


class MeetingAgent(BaseAgent):
    role = AgentRole.MEETING
    name = "Meeting Intelligence Agent"
    description = "Gestión inteligente de reuniones, transcripción y actas"

    def get_system_prompt(self) -> str:
        return MEETING_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        action = request.params.get("action", request.action)
        context = request.context

        if action == "analyze_transcript":
            return await self._analyze_transcript(request.params)
        elif action == "generate_minutes":
            return await self._generate_minutes(request.params)
        elif action == "check_pending_reports":
            return await self._check_pending_reports(context)
        elif action == "extract_tasks":
            return await self._extract_tasks(request.params)
        else:
            return await self._chat(request)

    async def _analyze_transcript(self, params: dict) -> AgentResponse:
        transcript = params.get("transcript", "")
        if not transcript:
            return AgentResponse(success=False, error="Transcripción requerida")
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt() + "\n\nAnaliza la siguiente transcripción de reunión:", transcript)
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})

    async def _generate_minutes(self, params: dict) -> AgentResponse:
        transcript = params.get("transcript", "")
        title = params.get("title", "Reunión")
        if not transcript:
            return AgentResponse(success=False, error="Transcripción requerida")
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        prompt = f"Genera un acta profesional para la reunión '{title}' con: resumen, participantes, temas tratados, compromisos, fechas y tareas asignadas."
        result = llm.chat(self.get_system_prompt(), f"{prompt}\n\nTranscripción:\n{transcript}")
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})

    async def _check_pending_reports(self, context: AgentContext) -> AgentResponse:
        if not context:
            return AgentResponse(success=False, error="Contexto requerido")
        db = SessionLocal()
        try:
            from models.company import Company
            company = db.query(Company).filter(Company.id == context.company_id).first()
            if not company:
                return AgentResponse(success=False, error="Empresa no encontrada")
            completed = db.query(Meeting).filter(Meeting.company_id == context.company_id, Meeting.status == "completed").count()
            no_summary = db.query(Meeting).filter(Meeting.company_id == context.company_id, Meeting.status == "completed", Meeting.summary.is_(None)).count()
            scheduled = db.query(Meeting).filter(Meeting.company_id == context.company_id, Meeting.status == "scheduled").count()
            msg = f"Reuniones completadas: {completed}\nSin informe: {no_summary}\nPróximas: {scheduled}"
            if llm.is_available():
                result = llm.chat(self.get_system_prompt(), f"Genera un reporte de estado sobre las reuniones:\n{msg}")
                return AgentResponse(success=True, message=result or msg, data={"completed": completed, "no_summary": no_summary, "scheduled": scheduled})
            return AgentResponse(success=True, message=msg)
        finally:
            db.close()

    async def _extract_tasks(self, params: dict) -> AgentResponse:
        text = params.get("text", "")
        if not text or not llm.is_available():
            return AgentResponse(success=False, error="Texto o LLM no disponible")
        result = llm.chat(self.get_system_prompt() + "\n\nExtrae todas las tareas, compromisos y fechas del siguiente texto. Devuelve una lista estructurada.", text)
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})

    async def _chat(self, request: AgentRequest) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt(), request.params.get("query", request.action))
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})
