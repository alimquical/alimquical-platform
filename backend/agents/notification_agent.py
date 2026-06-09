from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse
from .memory import AgentMemory
from services.llm import llm

NOTIFICATION_PROMPT = """Eres el NOTIFICATION AGENT de INTELLIWORK™.

Tus capacidades:
- Enviar notificaciones multicanal (WhatsApp, correo, push, Telegram)
- Recordar eventos y tareas próximas
- Alertar sobre seguimientos pendientes
- Confirmar reuniones
- Notificar cambios importantes

Canales configurados:
- WhatsApp: via API de WhatsApp Business
- Correo: via SMTP
- Push: via Service Worker
- Telegram: via Bot API

Responde en español con formato de notificación."""


class NotificationAgent(BaseAgent):
    role = AgentRole.NOTIFICATION
    name = "Notification Agent"
    description = "Sistema centralizado de notificaciones multicanal"

    def get_system_prompt(self) -> str:
        return NOTIFICATION_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        action = request.params.get("action", request.action)

        if action == "send":
            return await self._send(request.params)
        elif action == "remind":
            return await self._remind(request.params)
        else:
            return await self._chat(request)

    async def _send(self, params: dict) -> AgentResponse:
        channel = params.get("channel", "push")
        message = params.get("message", "")
        recipient = params.get("recipient", "")
        if not message:
            return AgentResponse(success=False, error="Mensaje requerido")
        if llm.is_available():
            result = llm.chat(self.get_system_prompt(), f"Prepara notificación para canal {channel}: {message}")
            return AgentResponse(success=True, message=result or "", data={"channel": channel, "recipient": recipient})
        return AgentResponse(success=True, message=f"Notificación preparada para {channel}")

    async def _remind(self, params: dict) -> AgentResponse:
        about = params.get("about", "")
        if llm.is_available():
            result = llm.chat(self.get_system_prompt(), f"Genera recordatorio sobre: {about}")
            return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})
        return AgentResponse(success=True, message=f"Recordatorio: {about}")

    async def _chat(self, request: AgentRequest) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible")
        result = llm.chat(self.get_system_prompt(), request.params.get("query", request.action))
        return AgentResponse(success=True, message=result or "", data={"agent": self.role.value})
