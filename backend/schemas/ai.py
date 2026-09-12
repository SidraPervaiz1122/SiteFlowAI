from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AiPreReviewOutput(BaseModel):
    readiness: str # Ready, Needs Attention, High Risk
    confidence_score: int = Field(ge=0, le=100)
    missing_evidence: List[str] = []
    potential_issues: List[str] = []
    suggested_checks: List[str] = []
    recommended_questions: List[str] = []

class AiReviewResponse(BaseModel):
    id: int
    check_request_id: int
    readiness: str
    confidence_score: int
    missing_evidence: Optional[str]
    potential_issues: Optional[str]
    suggested_checks: Optional[str]
    recommended_questions: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class AiObservationDraftRequest(BaseModel):
    check_request_id: int
    context_notes: Optional[str] = None
    observation_hint: Optional[str] = None

class AiObservationOutput(BaseModel):
    title: str
    description: str
    severity: str # LOW, MEDIUM, HIGH, CRITICAL
    category: str # QUALITY, SAFETY, SPECIFICATION, WORKMANSHIP, DOCUMENTATION
    recommended_action: str

class AiObservationResponse(BaseModel):
    id: int
    inspection_id: int
    title: str
    description: str
    severity: str
    category: str
    recommended_action: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class RagQueryRequest(BaseModel):
    query: str

class RagQueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[dict]
    is_fallback: bool = False
