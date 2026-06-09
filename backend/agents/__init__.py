from .base import BaseAgent
from .chief import ChiefAgent
from .meeting_agent import MeetingAgent
from .document_agent import DocumentAgent
from .crm_agent import CRMAgent
from .task_agent import TaskAgent
from .knowledge_agent import KnowledgeAgent
from typing import Optional


_agents: dict[str, BaseAgent] = {}


def register_agent(agent: BaseAgent):
    _agents[agent.role.value] = agent


def get_agent(role: str) -> Optional[BaseAgent]:
    return _agents.get(role)


def get_all_agents() -> list[BaseAgent]:
    return list(_agents.values())


def list_agents() -> list[dict]:
    return [{"name": a.name, "role": a.role.value, "description": a.description} for a in _agents.values()]


def init_agents():
    from .chief import ChiefAgent
    from .meeting_agent import MeetingAgent
    from .document_agent import DocumentAgent
    from .crm_agent import CRMAgent
    from .task_agent import TaskAgent
    from .calendar_agent import CalendarAgent
    from .notification_agent import NotificationAgent
    from .provider_agent import ProviderAgent
    from .knowledge_agent import KnowledgeAgent

    agents = [
        ChiefAgent(),
        MeetingAgent(),
        DocumentAgent(),
        CRMAgent(),
        TaskAgent(),
        CalendarAgent(),
        NotificationAgent(),
        ProviderAgent(),
        KnowledgeAgent(),
    ]
    for agent in agents:
        register_agent(agent)
