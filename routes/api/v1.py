from fastapi import APIRouter

from app.schemas.Request import QuestionRequest, DocumentRequest
from app.controllers.WorkflowController import workflow_controller


router = APIRouter()


@router.post("/ask")
async def ask_question(req: QuestionRequest):
    return workflow_controller.ask_question(req.question)

@router.post("/add")
async def add_document(req: DocumentRequest):
    return workflow_controller.add_document(req.text)
