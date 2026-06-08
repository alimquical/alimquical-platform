from datetime import datetime
from typing import Optional


class MeetingManager:
    def __init__(self):
        self.meetings = {}

    def schedule(self, title: str, date: datetime, duration: int = 60, participants: Optional[list] = None) -> dict:
        meeting_id = f"mtg_{datetime.now().timestamp()}"
        meeting = {
            "id": meeting_id,
            "title": title,
            "date": date.isoformat(),
            "duration": duration,
            "participants": participants or [],
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
        }
        self.meetings[meeting_id] = meeting
        return meeting

    def get_meeting(self, meeting_id: str) -> Optional[dict]:
        return self.meetings.get(meeting_id)

    def list_meetings(self, limit: int = 10) -> list:
        meetings = sorted(self.meetings.values(), key=lambda m: m["date"], reverse=True)
        return meetings[:limit]

    def update_status(self, meeting_id: str, status: str) -> Optional[dict]:
        if meeting_id in self.meetings:
            self.meetings[meeting_id]["status"] = status
            return self.meetings[meeting_id]
        return None
