from langgraph.graph import StateGraph, END
from app.services.EmbeddingService import EmbeddingService
from app.services.SimpleAnswerService import SimpleAnswerService
from app.tools.SimpleRetrieverTool import SimpleRetrieverTool
from app.schemas.Response import AskQuestionResponse, AddDocumentResponse
from app.utils.Http.HttpResponseUtils import response_success, response_error
from config.qdrantDb import create_document_store
import time


class WorkflowController:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.answer_service = SimpleAnswerService()
        self.document_store = create_document_store()
        self.retriever_tool = SimpleRetrieverTool(
            self.document_store, 
            self.embedding_service
        )
        self.chain = self._create_workflow()

    def _create_workflow(self):
        try:
            workflow = StateGraph(dict)
            workflow.add_node("retrieve", self.retriever_tool.retrieve)
            workflow.add_node("answer", self.answer_service.answer)
            workflow.set_entry_point("retrieve")
            workflow.add_edge("retrieve", "answer")
            workflow.add_edge("answer", END)
            chain = workflow.compile()

            return chain

        except Exception as e:
            raise e

    def ask_question(self, question: str):
        start = time.time()
        try:
            result = self.chain.invoke({"question": question})
            response_data = AskQuestionResponse(
                question=question,
                answer=result["answer"],
                context_used=result.get("context", []),
                latency_sec=round(time.time() - start, 3)
            )

            return response_success(response_data.model_dump())
        
        except Exception as e:
            response_error(str(e))

    def add_document(self, text: str):
        try:
            emb = self.embedding_service.embed(text)
            doc_id = self.document_store.get_document_count()
            self.document_store.add_document(doc_id, text, emb)
            response_data = AddDocumentResponse(id=doc_id, status="added")
            
            return response_success(response_data.model_dump())
        
        except Exception as e:
            response_error(str(e))


workflow_controller = WorkflowController()
