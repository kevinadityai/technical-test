import time
from fastapi import APIRouter, HTTPException
from qdrant_client.models import PointStruct

from app.schemas.Request import QuestionRequest, DocumentRequest
from app.controllers.WorkflowController import workflow_controller
from app.services.EmbeddingService import fake_embed
from config.qdrantDb import qdrant, USING_QDRANT, docs_memory
from config.setting import env


router = APIRouter()


@router.post("/ask")
def ask_question(req: QuestionRequest):
    start = time.time()
    try:
        result = workflow_controller.chain.invoke({"question": req.question})
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
def add_document(req: DocumentRequest):
    try:
        emb = fake_embed(req.text)
        doc_id = len(docs_memory)  # super unsafe ID!
        payload = {"text": req.text}

        if USING_QDRANT:
            qdrant.upsert(
                collection_name=env.COLLECTION_NAME,
                points=[PointStruct(id=doc_id, vector=emb, payload=payload)]
            )
        else:
            docs_memory.append(req.text)

        return {"id": doc_id, "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
