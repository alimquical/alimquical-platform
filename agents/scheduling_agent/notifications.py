from typing import Any


class NotificationDispatcher:
    async def send(self, channel: str, to: str, message: str, **kwargs) -> dict[str, Any]:
        return {"channel": channel, "to": to, "status": "sent", "message_id": f"msg_{id(message)}"}
