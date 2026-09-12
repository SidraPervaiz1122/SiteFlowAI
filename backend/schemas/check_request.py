from pydantic import BaseModel
from decimal import Decimal
from typing import Optional, List
from datetime import datetime
from backend.schemas.evidence import EvidenceResponse
from backend.schemas.ai import AiReviewResponse
from backend.schemas.inspection import InspectionResponse

class CheckRequestCreate(BaseModel):
    boq_item_id: int
    title: str
    description: Optional[str] = None
    proposed_qty: Decimal
    contractor_notes: Optional[str] = None

class CheckRequestResponse(BaseModel):
    id: int
    project_id: int
    boq_item_id: int
    cr_number: str
    title: str
    description: Optional[str]
    proposed_qty: Decimal
    unit: str
    status: str
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    # Nested entities
    boq_item_category: Optional[str] = None
    boq_item_description: Optional[str] = None
    boq_item_rate_pkr: Optional[Decimal] = None
    evidences: List[EvidenceResponse] = []
    ai_reviews: List[AiReviewResponse] = []
    inspections: List[InspectionResponse] = []

    class Config:
        from_attributes = True
