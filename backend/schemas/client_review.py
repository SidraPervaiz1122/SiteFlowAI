from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClientReviewRequest(BaseModel):
    quantity_approval_id: int
    decision: str # APPROVED, REJECTED
    comments: Optional[str] = None

class ClientReviewResponse(BaseModel):
    id: int
    quantity_approval_id: int
    client_id: int
    decision: str
    comments: Optional[str]
    reviewed_at: datetime

    class Config:
        from_attributes = True
