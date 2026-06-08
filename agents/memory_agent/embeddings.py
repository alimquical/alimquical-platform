from typing import Optional


class EmbeddingService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create_embedding(self, text: str) -> list[float]:
        return [0.0] * 1536

    async def create_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 1536 for _ in texts]
