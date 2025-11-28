from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config.setting import env
from app.services.DocumentStore import DocumentStore


def initialize_qdrant():
    try:
        qdrant = QdrantClient(env.QDRANT_URL)
        qdrant.recreate_collection(
            collection_name=env.COLLECTION_NAME,
            vectors_config=VectorParams(size=128, distance=Distance.COSINE)
        )
        return qdrant
    except Exception as e:
        print("Qdrant not available. Falling back to in-memory list.")
        return None


def create_document_store():
    qdrant = initialize_qdrant()
    return DocumentStore(qdrant, env.COLLECTION_NAME)
