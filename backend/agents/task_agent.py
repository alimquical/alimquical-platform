from sqlalchemy.orm import Session
from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse, AgentContext
from .memory import AgentMemory
from services.llm import llm
from core.database import SessionLocal

TASK_PROMPT = """Eres el TASK INTELLIGENCE AGENT de INTELLIWORK™.

Tus capacidades:
- Crear y asignar tareas manuales y automáticas
- Priorizar tareas según urgencia e importancia
- Detectar tareas desde reuniones, conversaciones y documentos
- Recordar responsables y fechas límite
- Identificar tareas vencidas
- Sugerir reasignaciones

Responde en español de forma clara y operativa."""


class TaskAgent(BaseAgent):
    role = AgentRole.TASK
    name = "Task Intelligence Agent"
    description = "Gestión inteligente de tareas y priorización"

    def get_system_prompt(self) -> str:
        return TASK_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        action = request.params.get("action", request.action)
        context = request.context

        if action == "detect_from_text":
            return await self._detect_from_text(request.params)
        elif action == "overdue_tasks":
            return await self._overdue_tasks(context)
        elif action == "prioritize":
            return await self._prioritize(context)
        else:
            return await self._chat(request)

    async def _detect_from_text(self, params: dict) -> AgentResponse:
        text = params.get("text", "")
        if not text or not llm.is_available():
            return AgentResponse(success=False, error="Texto o LLM no disponible")
        result = llm.chat(self.get_system_prompt() + "\n\nExtrae y estructura todas las tareas, responsables y fechas del siguiente texto:", text)
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})

    async def _overdue_tasks(self, context: AgentContext) -> AgentResponse:
        if not context:
            return AgentResponse(success=False, error="Contexto requerido")
        db = SessionLocal()
        try:
            from models.task import Task
            from datetime import datetime, timezone
            overdue = db.query(Task).filter(Task.company_id == context.company_id, Task.due_date < datetime.now(timezone.utc), Task.status != "done").count()
            total = db.query(Task).filter(Task.company_id == context.company_id, Task.status != "done").count()
            msg = f"Tareas vencidas: {overdue}\nTareas pendientes totales: {total}"
            if llm.is_available():
                result = llm.chat(self.get_system_prompt(), f"Genera alerta sobre:\n{msg}")
                return AgentResponse(success=True, message=result or msg, data={"overdue": overdue, "pending": total})
            return AgentResponse(success=True, message=msg)
        finally:
            db.close()

    async def _prioritize(self, context: AgentContext) -> AgentResponse:
        if not context:
            return AgentResponse(success=False, error="Contexto requerido")
        db = SessionLocal()
        try:
            from models.task import Task
            tasks = db.query(Task).filter(Task.company_id == context.company_id, Task.status == "todo").order_by(Task.priority.desc()).limit(10).all()
            if not tasks:
                return AgentResponse(success=True, message="No hay tareas pendientes")
            task_list = "\n".join([f"- {t.title} (prioridad: {t.priority.value})" for t in tasks])
            if llm.is_available():
                result = llm.chat(self.get_system_prompt(), f"Prioriza y recomienda acciones para:\n{task_list}")
                return AgentResponse(success=True, message=result or task_list, data={"task_count": len(tasks)})
            return AgentResponse(success=True, message=task_list)
        finally:
            db.close()

    async def _chat(self, request: AgentRequest) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt(), request.params.get("query", request.action))
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})
