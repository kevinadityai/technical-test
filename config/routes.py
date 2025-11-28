from config.setting import env
from routes.api import v1 as api_v1
from app.controllers.WorkflowController import workflow_controller


def setup_routes(app):
    app.include_router(
        api_v1.router,
        prefix="/api/v1",
        tags=["api_v1"],
    )

    @app.get("/status")
    async def status():
        return {
            "qdrant_ready": workflow_controller.document_store.is_using_qdrant(),
            "in_memory_docs_count": workflow_controller.document_store.get_document_count(),
            "graph_ready": workflow_controller.chain is not None
        }

    @app.get("/")
    async def read_root():
        return {
            "APP_ENV": env.APP_ENV,
            "APP_NAME": env.APP_NAME,
            "APP_VERSION": env.APP_VERSION,
        }
