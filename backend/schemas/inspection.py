from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from backend.schemas.observation import ObservationResponse

class InspectionDecisionRequest(BaseModel):
    decision: str # ACCEPT, REJECT, CONDITIONAL
    inspector_notes: Optional[str] = None
    checklist_results: Optional[str] = None # JSON string

class InspectionResponse(BaseModel):
    id: int
    check_request_id: int
    inspector_id: int
    decision: Optional[str]
    inspector_notes: Optional[str]
    checklist_results: Optional[str]
    inspected_at: Optional[datetime]
    created_at: datetime
    observations: List[ObservationResponse] = []

    class Config:
        from_attributes = True
