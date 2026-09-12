from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EvidenceResponse(BaseModel):
    id: int
    check_request_id: int
    inspection_id: Optional[int]
    filename: str
    file_path: str
    file_type: str
    file_size_bytes: int
    caption: Optional[str]
    uploaded_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True
