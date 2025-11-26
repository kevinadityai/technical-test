from config.setting import env
from routes.api import v1 as api_v1


def setup_routes(app):
    app.include_router(
        api_v1.router,
        prefix="/api/v1",
        tags=["api_v1"],
    )

    @app.get("/status")
    async def status():
        return {
            "qdrant_ready": USING_QDRANT,
            "in_memory_docs_count": len(docs_memory),
            "graph_ready": chain is not None
        }

    @app.get("/")
    async def read_root():
        return {
            "APP_ENV": env.APP_ENV,
            "APP_NAME": env.APP_NAME,
            "APP_VERSION": env.APP_VERSION,
        }
