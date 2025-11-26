from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config.setting import env


docs_memory = []


try:
    qdrant = QdrantClient(env.QDRANT_URL)
    qdrant.recreate_collection(
        collection_name=env.COLLECTION_NAME,
        vectors_config=VectorParams(size=128, distance=Distance.COSINE)
    )
    USING_QDRANT = True
    
except Exception as e:
    print("Qdrant not available. Falling back to in-memory list.")
    qdrant = None
    USING_QDRANT = False
