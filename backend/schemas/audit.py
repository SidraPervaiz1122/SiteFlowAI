from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    link: Optional[str]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    project_id: Optional[int]
    actor_id: Optional[int]
    actor_name: str
    actor_role: str
    action: str
    entity_type: str
    entity_id: str
    old_value: Optional[str]
    new_value: Optional[str]
    metadata_json: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
