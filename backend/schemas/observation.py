from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ObservationCreateRequest(BaseModel):
    title: str
    description: str
    severity: str = "LOW"
    category: str = "QUALITY"
    corrective_action: Optional[str] = None
    is_ai_generated: bool = False

class ObservationResponse(BaseModel):
    id: int
    inspection_id: int
    title: str
    description: str
    severity: str
    category: str
    corrective_action: Optional[str]
    is_ai_generated: bool
    accepted_by_re: bool
    created_at: datetime

    class Config:
        from_attributes = True
