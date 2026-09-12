from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    project_id: int
    title: str
    category: str
    filename: str
    file_path: str
    file_type: str
    file_size_bytes: int
    uploaded_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True
