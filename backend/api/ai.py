from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.dependencies import get_current_user
from backend.models.user import User
from backend.schemas.ai import RagQueryRequest, RagQueryResponse
from backend.ai.rag.hybrid_retriever import HybridRetriever
from backend.app.config import settings

router = APIRouter(prefix="/ai", tags=["AI Subsystem"])

@router.post("/query", response_model=RagQueryResponse)
def ask_project_rag(
    req: RagQueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = HybridRetriever.query(db, req.query)
    return RagQueryResponse(
        query=req.query,
        answer=result["answer"],
        sources=result["sources"],
        is_fallback=result.get("is_fallback", False)
    )

@router.get("/status")
def get_ai_status(current_user: User = Depends(get_current_user)):
    return {
        "provider": settings.AI_PROVIDER,
        "fallback_enabled": settings.AI_FALLBACK_ENABLED,
        "is_advisory_only": True,
        "mode": "deterministic_offline_ready" if not settings.OPENAI_API_KEY else "hybrid_connected"
    }
