import uuid
import qdrant_client
from qdrant_client.models import Distance, PointStruct

from .setting import env
from app.services.QdrantServices import Qdrant
from app.services.EmbeddingServices import embed


# Qdrant setup (assumes local instance)
try:
    qdrant = QdrantClient("http://localhost:6333")
    qdrant.recreate_collection(
        collection_name="demo_collection",
        vectors_config=VectorParams(size=128, distance=Distance.COSINE)
    )
    USING_QDRANT = True
except Exception as e:
    print("⚠️  Qdrant not available. Falling back to in-memory list.")
    USING_QDRANT = False



class QdrantDB:
    def __init__(self):
        self.client = qdrant_client.QdrantClient(
            url=env.qdrant_host,
            api_key=env.qdrant_api_key,
        )

    async def get_db(self, collection, distance=Distance.DOT):
        return Qdrant(
            self.client,
            collection_name=collection,
            distance_strategy=distance,
            embedding_function=embed.embed_query_intfloat
        )

    async def get_retriever_infloat(self, collection, **kwargs):
        db = await self.get_db(collection, Distance.COSINE)
        retriever = db.as_retriever(**kwargs)
        return retriever

db = QdrantDB()

def get_qdrant_db():
    return db


def get_qdrant_client():
    return db.client