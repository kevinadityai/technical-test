from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


class DocumentStore:
    def __init__(self, qdrant_client: Optional[QdrantClient], collection_name: str):
        self.qdrant = qdrant_client
        self.collection_name = collection_name
        self.using_qdrant = qdrant_client is not None
        self.docs_memory = []

    def add_document(self, doc_id: int, text: str, embedding: List[float]) -> None:
        payload = {"text": text}
        
        if self.using_qdrant:
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(id=doc_id, vector=embedding, payload=payload)]
            )
        else:
            self.docs_memory.append(text)

    def search(self, query_embedding: List[float], query_text: str, limit: int = 2) -> List[str]:
        results = []
        
        if self.using_qdrant:
            hits = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )
            for hit in hits:
                results.append(hit.payload["text"])
        else:
            for doc in self.docs_memory:
                if query_text.lower() in doc.lower():
                    results.append(doc)
            if not results and self.docs_memory:
                results = [self.docs_memory[0]]
        
        return results

    def get_document_count(self) -> int:
        return len(self.docs_memory) if not self.using_qdrant else 0

    def is_using_qdrant(self) -> bool:
        return self.using_qdrant
