import os
import time
import random
import json
from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

app = FastAPI(title="Learning RAG Demo")

# Pretend this is a real embedding model
def fake_embed(text: str):
    # Seed based on input so it's "deterministic"
    random.seed(abs(hash(text)) % 10000)
    return [random.random() for _ in range(128)]  # Small vector for demo

# Super basic in-memory "storage" fallback
docs_memory = []

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

# LangGraph state = plain dict
def simple_retrieve(state):
    query = state["question"]
    results = []
    emb = fake_embed(query)

    if USING_QDRANT:
        hits = qdrant.search(collection_name="demo_collection", query_vector=emb, limit=2)
        for hit in hits:
            results.append(hit.payload["text"])
    else:
        for doc in docs_memory:
            if query.lower() in doc.lower():
                results.append(doc)
        if not results and docs_memory:
            results = [docs_memory[0]]  # Just grab first

    state["context"] = results
    return state

def simple_answer(state):
    ctx = state["context"]
    if ctx:
        answer = f"I found this: '{ctx[0][:100]}...'"
    else:
        answer = "Sorry, I don't know."
    state["answer"] = answer
    return state
