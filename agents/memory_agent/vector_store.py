from typing import Optional


class VectorStore:
    def __init__(self, qdrant_url: Optional[str] = None, api_key: Optional[str] = None):
        self.qdrant_url = qdrant_url
        self.api_key = api_key

    async def store_embedding(self, collection: str, vector: list[float], payload: dict) -> str:
        return f"vec_{id(payload)}"

    async def search_similar(self, collection: str, vector: list[float], limit: int = 5) -> list[dict]:
        return []
