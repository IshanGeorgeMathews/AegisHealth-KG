from fastapi import FastAPI
from aegis.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="AegisHealth-KG API",
    description="API for the autonomous digital advocate system.",
    version="0.1.0",
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
