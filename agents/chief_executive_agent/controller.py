import asyncio
from typing import Any, Optional
from .memory import AgentMemory
from .decision_engine import DecisionEngine
from .prompts import SYSTEM_PROMPT


class ChiefExecutiveAgent:
    def __init__(self, company_id: str, openai_api_key: Optional[str] = None):
        self.company_id = company_id
        self.memory = AgentMemory(company_id)
        self.decision_engine = DecisionEngine()
        self.active_agent: Optional[str] = None
        self.task_queue: asyncio.Queue = asyncio.Queue()

    async def process_request(self, request: str, context: dict[str, Any]) -> dict[str, Any]:
        self.memory.add_to_context(request)
        decision = await self.decision_engine.analyze(request, context)
        agent = self._select_agent(decision)
        self.active_agent = agent
        return {
            "agent": agent,
            "decision": decision,
            "confidence": decision.get("confidence", 0.0),
        }

    def _select_agent(self, decision: dict) -> str:
        intent = decision.get("intent", "").lower()
        agent_map = {
            "reunion": "meeting_secretary",
            "analisis": "business_analyst",
            "documento": "document_intelligence",
            "cliente": "crm_agent",
            "agenda": "scheduling_agent",
            "legal": "legal_agent",
            "financiero": "financial_agent",
            "notificacion": "notification_agent",
            "venta": "sales_agent",
            "busqueda": "memory_agent",
        }
        for key, agent_name in agent_map.items():
            if key in intent:
                return agent_name
        return "memory_agent"

    async def delegate_task(self, agent_name: str, task: dict) -> Any:
        await self.task_queue.put({"agent": agent_name, "task": task})
        return {"status": "delegated", "agent": agent_name}
