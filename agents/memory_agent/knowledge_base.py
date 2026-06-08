from typing import Any, Optional


class KnowledgeBase:
    def __init__(self):
        self.documents = {}

    def add_document(self, title: str, content: str, tags: Optional[list[str]] = None) -> dict[str, Any]:
        doc_id = f"doc_{len(self.documents) + 1}"
        doc = {"id": doc_id, "title": title, "content": content, "tags": tags or []}
        self.documents[doc_id] = doc
        return doc

    def search(self, query: str) -> list[dict[str, Any]]:
        results = []
        query_lower = query.lower()
        for doc in self.documents.values():
            if query_lower in doc["title"].lower() or query_lower in doc["content"].lower():
                results.append(doc)
        return results
