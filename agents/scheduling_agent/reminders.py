from datetime import datetime
from typing import Optional


class ReminderManager:
    def __init__(self):
        self.reminders = {}

    def set_reminder(self, event_id: str, minutes_before: int = 30, channel: str = "push") -> dict:
        reminder_id = f"rem_{datetime.now().timestamp()}"
        reminder = {
            "id": reminder_id,
            "event_id": event_id,
            "minutes_before": minutes_before,
            "channel": channel,
            "active": True,
        }
        self.reminders[reminder_id] = reminder
        return reminder
