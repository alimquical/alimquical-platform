from .base import BaseAgent, AgentRole, AgentRequest, AgentResponse
from .memory import AgentMemory
from services.llm import llm

CHIEF_PROMPT = """Eres el CHIEF EXECUTIVE AGENT de INTELLIWORK™, el coordinador central del sistema.

Tu función es:
1. Recibir solicitudes del usuario y determinar qué agente especializado debe ejecutarlas.
2. Coordinar múltiples agentes cuando se requiere.
3. Proporcionar una visión unificada del estado del sistema.
4. Delegar tareas al agente correcto según la intención del usuario.

Agentes disponibles:
- meeting: Gestión de reuniones, transcripción, actas, compromisos.
- document: Gestión documental, creación, búsqueda, versionado.
- crm: Gestión de clientes, historial, oportunidades, seguimientos.
- task: Gestión de tareas, auto-detección, priorización.
- calendar: Agenda, calendario, Google Calendar, conflictos.
- notification: Notificaciones multicanal (WhatsApp, correo, push).
- provider: Gestión de proveedores, evaluaciones, riesgos.
- knowledge: Memoria corporativa, búsqueda histórica.

Responde en español de forma clara y concisa.
Si no puedes resolver la solicitud, indica qué agente debería hacerlo."""


class ChiefAgent(BaseAgent):
    role = AgentRole.CHIEF
    name = "Chief Executive Agent"
    description = "Coordinador central del sistema INTELLIWORK™"

    def get_system_prompt(self) -> str:
        return CHIEF_PROMPT

    async def process(self, request: AgentRequest) -> AgentResponse:
        if not llm.is_available():
            return AgentResponse(success=False, error="LLM no disponible. Configura OPENAI_API_KEY")

        query = request.params.get("query", request.action)
        context_info = ""
        if request.context:
            from agents import get_all_agents
            all_agents = get_all_agents()
            agents_status = "\n".join([f"- {a.name} ({a.role.value})" for a in all_agents])
            context_info = f"\n\nContexto:\nEmpresa: {request.context.company_id}\nUsuario: {request.context.user_id}\n\nAgentes registrados:\n{agents_status}"

        result = llm.chat(self.get_system_prompt() + context_info, query)
        if not result:
            return AgentResponse(success=False, error="Error al procesar solicitud con LLM")

        return AgentResponse(success=True, message=result, data={"agent": self.role.value})
