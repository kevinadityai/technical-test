from app.services.EmbeddingService import EmbeddingService


class SimpleRetrieverTool:
    def __init__(self, document_store, embedding_service=None):
        self.document_store = document_store
        self.embedding_service = embedding_service or EmbeddingService()

    def retrieve(self, state):
        query = state["question"]
        emb = self.embedding_service.embed(query)
        results = self.document_store.search(emb, query, limit=2)
        state["context"] = results
        return state