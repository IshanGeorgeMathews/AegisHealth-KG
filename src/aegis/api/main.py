from fastapi import FastAPI

from aegis.api.routes import retrieval
from aegis.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="AegisHealth-KG API",
    description="API for the autonomous digital advocate system.",
    version="0.1.0",
)

app.include_router(retrieval.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
