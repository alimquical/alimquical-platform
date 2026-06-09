from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class AgentRole(Enum):
    CHIEF = "chief"
    MEETING = "meeting"
    DOCUMENT = "document"
    CRM = "crm"
    TASK = "task"
    CALENDAR = "calendar"
    NOTIFICATION = "notification"
    PROVIDER = "provider"
    SALES = "sales"
    FINANCIAL = "financial"
    KNOWLEDGE = "knowledge"


@dataclass
class AgentContext:
    company_id: str
    user_id: str
    user_role: str


@dataclass
class AgentRequest:
    action: str
    params: dict = field(default_factory=dict)
    context: Optional[AgentContext] = None


@dataclass
class AgentResponse:
    success: bool
    message: str = ""
    data: dict = field(default_factory=dict)
    error: Optional[str] = None


class AgentTool:
    name: str = ""
    description: str = ""

    def execute(self, params: dict, context: AgentContext) -> dict:
        raise NotImplementedError


class BaseAgent:
    role: AgentRole = AgentRole.CHIEF
    name: str = ""
    description: str = ""

    def __init__(self):
        self._tools: list[AgentTool] = []
        self._memory: Optional[AgentMemory] = None

    def get_system_prompt(self) -> str:
        raise NotImplementedError

    def get_tools(self) -> list[AgentTool]:
        return self._tools

    async def process(self, request: AgentRequest) -> AgentResponse:
        raise NotImplementedError

    def register_tool(self, tool: AgentTool):
        self._tools.append(tool)
