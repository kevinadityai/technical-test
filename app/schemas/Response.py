from pydantic import BaseModel
from typing import List, Optional


class AskQuestionResponse(BaseModel):
    question: str
    answer: str
    context_used: List[str]
    latency_sec: float


class AddDocumentResponse(BaseModel):
    id: int
    status: str

