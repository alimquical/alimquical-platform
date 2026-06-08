class EmailNotifier:
    async def send_email(self, to: str, subject: str, body: str) -> dict:
        return {"to": to, "subject": subject, "status": "sent", "channel": "email"}
