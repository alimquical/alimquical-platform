class PushNotifier:
    async def send_push(self, user_id: str, title: str, body: str) -> dict:
        return {"user_id": user_id, "title": title, "status": "sent", "channel": "push"}
