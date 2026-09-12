import json
from typing import Optional, Any
from sqlalchemy.orm import Session
from backend.models.audit_log import AuditLog
from backend.models.user import User

def record_audit(
    db: Session,
    actor: Optional[User],
    action: str,
    entity_type: str,
    entity_id: str,
    old_value: Optional[Any] = None,
    new_value: Optional[Any] = None,
    metadata: Optional[dict] = None,
    project_id: Optional[int] = 1,
    commit: bool = False
) -> AuditLog:
    """Record an immutable audit log entry."""
    actor_id = actor.id if actor else None
    actor_name = actor.full_name if actor else "SYSTEM"
    actor_role = actor.role if actor else "SYSTEM"

    old_str = json.dumps(old_value, default=str) if isinstance(old_value, (dict, list)) else (str(old_value) if old_value is not None else None)
    new_str = json.dumps(new_value, default=str) if isinstance(new_value, (dict, list)) else (str(new_value) if new_value is not None else None)
    meta_str = json.dumps(metadata, default=str) if metadata else None

    log_entry = AuditLog(
        project_id=project_id,
        actor_id=actor_id,
        actor_name=actor_name,
        actor_role=actor_role,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        old_value=old_str,
        new_value=new_str,
        metadata_json=meta_str
    )
    db.add(log_entry)
    if commit:
        db.commit()
        db.refresh(log_entry)
    return log_entry
