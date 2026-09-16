from fastapi import APIRouter, Depends, HTTPException

from aegis.models import RetrievalRequest, RetrievalResult
from aegis.retrieval.service import RetrievalService

router = APIRouter(prefix="/retrieval", tags=["retrieval"])

_service_instance = None


def get_retrieval_service() -> RetrievalService:
    global _service_instance
    if _service_instance is None:
        _service_instance = RetrievalService()
    return _service_instance


@router.post("/search", response_model=RetrievalResult)
def search_evidence(
    request: RetrievalRequest,
    service: RetrievalService = Depends(get_retrieval_service),
) -> RetrievalResult:
    try:
        return service.retrieve(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
