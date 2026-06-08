from typing import Optional


class ClientManager:
    def __init__(self):
        self.clients = {}

    def add_client(self, name: str, email: str, phone: Optional[str] = None, company: Optional[str] = None) -> dict:
        client_id = f"cli_{len(self.clients) + 1}"
        client = {
            "id": client_id,
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "status": "lead",
            "created_at": "2026-06-15",
        }
        self.clients[client_id] = client
        return client

    def get_client(self, client_id: str) -> Optional[dict]:
        return self.clients.get(client_id)

    def update_status(self, client_id: str, status: str) -> Optional[dict]:
        if client_id in self.clients:
            self.clients[client_id]["status"] = status
            return self.clients[client_id]
        return None
