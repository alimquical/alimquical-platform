from typing import Optional


class WhatsAppNotifier:
    def __init__(self, api_token: Optional[str] = None, phone_number_id: Optional[str] = None):
        self.api_token = api_token
        self.phone_number_id = phone_number_id

    async def send_message(self, to: str, message: str) -> dict:
        return {"to": to, "message": message, "status": "sent", "channel": "whatsapp"}
