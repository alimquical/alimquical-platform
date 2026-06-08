from datetime import datetime, timedelta
from typing import Optional


class CalendarManager:
    def __init__(self):
        self.events = {}

    def create_event(self, title: str, start: datetime, end: Optional[datetime] = None, description: Optional[str] = None) -> dict:
        event_id = f"evt_{datetime.now().timestamp()}"
        if not end:
            end = start + timedelta(hours=1)
        event = {
            "id": event_id,
            "title": title,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "description": description,
        }
        self.events[event_id] = event
        return event

    def list_events(self, date: Optional[datetime] = None) -> list:
        if date:
            return [e for e in self.events.values() if e["start"].startswith(date.strftime("%Y-%m-%d"))]
        return list(self.events.values())
