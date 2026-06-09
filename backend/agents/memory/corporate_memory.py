from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from core.config import settings
from core.database import SessionLocal


class VectorMemory:
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None and settings.QDRANT_URL:
            from qdrant_client import QdrantClient
            self._client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
        return self._client

    def is_available(self) -> bool:
        return bool(settings.QDRANT_URL) and bool(self._get_client())

    def store(self, collection: str, doc_id: str, text: str, metadata: dict) -> bool:
        if not self.is_available():
            return False
        try:
            from qdrant_client.http import models
            client = self._get_client()
            from openai import OpenAI
            oai = OpenAI(api_key=settings.OPENAI_API_KEY)
            embedding = oai.embeddings.create(input=text, model="text-embedding-3-small").data[0].embedding
            client.upsert(
                collection_name=collection,
                points=[models.PointStruct(id=doc_id, vector=embedding, payload={"text": text, **metadata})],
            )
            return True
        except Exception:
            return False

    def search(self, collection: str, query: str, limit: int = 5) -> List[dict]:
        if not self.is_available():
            return []
        try:
            from openai import OpenAI
            oai = OpenAI(api_key=settings.OPENAI_API_KEY)
            embedding = oai.embeddings.create(input=query, model="text-embedding-3-small").data[0].embedding
            client = self._get_client()
            results = client.search(collection_name=collection, query_vector=embedding, limit=limit)
            return [{"id": r.id, "score": r.score, "text": r.payload.get("text", ""), **{k: v for k, v in r.payload.items() if k != "text"}} for r in results]
        except Exception:
            return []


class CorporateMemory:
    def __init__(self, company_id: str, db: Session):
        self.company_id = company_id
        self.db = db
        self.vector = VectorMemory()
        self._collection = f"company_{company_id}"

    def store_knowledge(self, doc_id: str, text: str, source_type: str, metadata: dict = None):
        meta = {"company_id": self.company_id, "source_type": source_type, "timestamp": datetime.now(timezone.utc).isoformat(), **(metadata or {})}
        return self.vector.store(self._collection, doc_id, text, meta)

    def query(self, question: str, limit: int = 5) -> List[dict]:
        return self.vector.search(self._collection, question, limit)

    def query_with_context(self, question: str, limit: int = 5) -> str:
        results = self.query(question, limit)
        if not results:
            return ""
        context = "\n\n".join([f"[{r.get('source_type', 'unknown')}] {r['text']}" for r in results])
        return context


vector_memory = VectorMemory()
