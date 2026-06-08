from typing import Any, List


class AgentMemory:
    def __init__(self, company_id: str):
        self.company_id = company_id
        self.short_term: List[str] = []
        self.context: dict[str, Any] = {}

    def add_to_context(self, message: str) -> None:
        self.short_term.append(message)
        if len(self.short_term) > 50:
            self.short_term.pop(0)

    def get_recent_context(self, limit: int = 10) -> List[str]:
        return self.short_term[-limit:]

    def store_knowledge(self, key: str, value: Any) -> None:
        self.context[key] = value

    def retrieve_knowledge(self, key: str) -> Any:
        return self.context.get(key)

    def clear_short_term(self) -> None:
        self.short_term.clear()
