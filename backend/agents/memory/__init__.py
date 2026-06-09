from typing import Optional, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from core.config import settings
from core.database import SessionLocal


class AgentMemory:
    def __init__(self, agent_name: str, company_id: str, db: Session):
        self.agent_name = agent_name
        self.company_id = company_id
        self.db = db
        self._short_term: list[dict] = []

    def remember(self, key: str, value: Any, ttl_seconds: int = 3600):
        self._short_term.append({
            "key": key,
            "value": value,
            "expires_at": datetime.now(timezone.utc).timestamp() + ttl_seconds,
        })

    def recall(self, key: str) -> Optional[Any]:
        now = datetime.now(timezone.utc).timestamp()
        for item in self._short_term:
            if item["key"] == key and item["expires_at"] > now:
                return item["value"]
        return None

    def forget(self, key: str):
        self._short_term = [m for m in self._short_term if m["key"] != key]

    def clear(self):
        self._short_term.clear()
