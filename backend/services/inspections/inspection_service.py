from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.inspection import Inspection
from backend.models.observation import Observation
from backend.models.ai_review import AiObservation
from backend.models.check_request import CheckRequest
from backend.models.user import User
from backend.core.enums import WorkflowState, UserRole, InspectionDecision, AuditAction
from backend.core.exceptions import NotFoundException, ForbiddenException, WorkflowTransitionError
from backend.services.workflow.state_machine import WorkflowStateMachine
from backend.services.audit.audit_service import record_audit
from backend.services.notifications.notification_service import notify_role
from backend.ai.client import AiClient

def get_or_create_inspection(db: Session, check_request_id: int, re: User) -> Inspection:
    if re.role != UserRole.RE.value:
        raise ForbiddenException("Only Resident Engineer (RE) can conduct inspections.")

    cr = db.query(CheckRequest).filter(CheckRequest.id == check_request_id).first()
    if not cr:
        raise NotFoundException(f"Check Request {check_request_id} not found")

    inspection = db.query(Inspection).filter(Inspection.check_request_id == check_request_id).first()
    if not inspection:
        # If in PENDING_INSPECTION, advance to INSPECTION_IN_PROGRESS
        if cr.status == WorkflowState.PENDING_INSPECTION.value:
            WorkflowStateMachine.validate_transition(cr.status, WorkflowState.INSPECTION_IN_PROGRESS.value, re.role)
            cr.status = WorkflowState.INSPECTION_IN_PROGRESS.value

        inspection = Inspection(
            check_request_id=cr.id,
            inspector_id=re.id
        )
        db.add(inspection)
        db.commit()
        db.refresh(inspection)

        record_audit(
            db=db,
            actor=re,
            action=AuditAction.INSPECTION_STARTED.value,
            entity_type="INSPECTION",
            entity_id=str(inspection.id),
            metadata={"check_request_id": cr.id, "cr_number": cr.cr_number}
        )

    return inspection

def draft_ai_observation(
    db: Session,
    inspection_id: int,
    re: User,
    hint: Optional[str] = None
) -> AiObservation:
    if re.role != UserRole.RE.value:
        raise ForbiddenException("Only Resident Engineer (RE) can request AI observation drafts.")

    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise NotFoundException(f"Inspection {inspection_id} not found")

    cr = inspection.check_request
    boq = cr.boq_item

    draft = AiClient.draft_observation(
        item_number=boq.item_number,
        category=boq.category,
        description=boq.description,
        hint=hint
    )

    ai_obs = AiObservation(
        inspection_id=inspection.id,
        title=draft.title,
        description=draft.description,
        severity=draft.severity,
        category=draft.category,
        recommended_action=draft.recommended_action
    )
    db.add(ai_obs)
    db.commit()
    db.refresh(ai_obs)
    return ai_obs

def add_observation(
    db: Session,
    inspection_id: int,
    title: str,
    description: str,
    re: User,
    severity: str = "LOW",
    category: str = "QUALITY",
    corrective_action: Optional[str] = None,
    is_ai_generated: bool = False
) -> Observation:
    if re.role != UserRole.RE.value:
        raise ForbiddenException("Only Resident Engineer (RE) can record observations.")

    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise NotFoundException(f"Inspection {inspection_id} not found")

    obs = Observation(
        inspection_id=inspection.id,
        title=title,
        description=description,
        severity=severity,
        category=category,
        corrective_action=corrective_action,
        is_ai_generated=is_ai_generated,
        accepted_by_re=True
    )
    db.add(obs)

    record_audit(
        db=db,
        actor=re,
        action=AuditAction.OBSERVATION_CREATED.value,
        entity_type="OBSERVATION",
        entity_id=title,
        new_value={"severity": severity, "category": category, "is_ai": is_ai_generated}
    )

    db.commit()
    db.refresh(obs)
    return obs

def decide_inspection(
    db: Session,
    inspection_id: int,
    decision: str, # ACCEPT, REJECT, CONDITIONAL
    re: User,
    inspector_notes: Optional[str] = None,
    checklist_results: Optional[str] = None
) -> Inspection:
    if re.role != UserRole.RE.value:
        raise ForbiddenException("Only Resident Engineer (RE) can decide inspections.")

    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise NotFoundException(f"Inspection {inspection_id} not found")

    cr = inspection.check_request

    target_state = WorkflowState.INSPECTION_ACCEPTED.value if decision in ["ACCEPT", "CONDITIONAL"] else WorkflowState.INSPECTION_REJECTED.value
    WorkflowStateMachine.validate_transition(cr.status, target_state, re.role)

    inspection.decision = decision
    inspection.inspector_notes = inspector_notes
    inspection.checklist_results = checklist_results
    inspection.inspected_at = datetime.now(timezone.utc)

    cr.status = target_state

    record_audit(
        db=db,
        actor=re,
        action=AuditAction.INSPECTION_DECIDED.value,
        entity_type="INSPECTION",
        entity_id=str(inspection.id),
        new_value={"decision": decision, "notes": inspector_notes},
        metadata={"cr_number": cr.cr_number}
    )

    notify_role(
        db,
        UserRole.CONTRACTOR,
        title=f"Inspection Decision: {decision}",
        message=f"RE marked inspection for {cr.cr_number} as {decision}.",
        link=f"/check-requests/{cr.id}"
    )

    db.commit()
    db.refresh(inspection)
    return inspection
