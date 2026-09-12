import os
import json
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.check_request import CheckRequest
from backend.models.boq_item import BoqItem
from backend.models.evidence import Evidence
from backend.models.ai_review import AiReview
from backend.models.user import User
from backend.core.enums import WorkflowState, UserRole, AuditAction
from backend.core.exceptions import NotFoundException, ForbiddenException, WorkflowTransitionError
from backend.core.money import to_decimal
from backend.services.workflow.state_machine import WorkflowStateMachine
from backend.services.audit.audit_service import record_audit
from backend.services.notifications.notification_service import notify_role
from backend.ai.client import AiClient

def create_check_request(
    db: Session,
    project_id: int,
    boq_item_id: int,
    title: str,
    proposed_qty: Decimal,
    contractor: User,
    description: Optional[str] = None
) -> CheckRequest:
    if contractor.role != UserRole.CONTRACTOR.value:
        raise ForbiddenException("Only Contractor can create Check Requests.")

    boq_item = db.query(BoqItem).filter(BoqItem.id == boq_item_id).first()
    if not boq_item:
        raise NotFoundException(f"BOQ Item {boq_item_id} not found")

    count = db.query(CheckRequest).filter(CheckRequest.project_id == project_id).count()
    cr_number = f"CR-{count + 1:03d}"

    proposed_dec = to_decimal(proposed_qty)

    cr = CheckRequest(
        project_id=project_id,
        boq_item_id=boq_item_id,
        cr_number=cr_number,
        title=title,
        description=description,
        proposed_qty=proposed_dec,
        unit=boq_item.unit,
        status=WorkflowState.DRAFT.value,
        created_by_id=contractor.id
    )
    db.add(cr)

    record_audit(
        db=db,
        actor=contractor,
        action=AuditAction.CR_CREATED.value,
        entity_type="CHECK_REQUEST",
        entity_id=cr_number,
        new_value={"title": title, "proposed_qty": str(proposed_dec), "boq_item_id": boq_item_id}
    )

    db.commit()
    db.refresh(cr)
    return cr

def attach_evidence(
    db: Session,
    check_request_id: int,
    filename: str,
    file_path: str,
    file_type: str,
    file_size_bytes: int,
    uploaded_by: User,
    caption: Optional[str] = None,
    inspection_id: Optional[int] = None
) -> Evidence:
    cr = db.query(CheckRequest).filter(CheckRequest.id == check_request_id).first()
    if not cr:
        raise NotFoundException(f"Check Request {check_request_id} not found")

    evidence = Evidence(
        check_request_id=check_request_id,
        inspection_id=inspection_id,
        filename=filename,
        file_path=file_path,
        file_type=file_type,
        file_size_bytes=file_size_bytes,
        caption=caption,
        uploaded_by_id=uploaded_by.id
    )
    db.add(evidence)

    record_audit(
        db=db,
        actor=uploaded_by,
        action=AuditAction.EVIDENCE_UPLOADED.value,
        entity_type="EVIDENCE",
        entity_id=filename,
        metadata={"check_request_id": check_request_id, "file_size": file_size_bytes}
    )

    db.commit()
    db.refresh(evidence)
    return evidence

def submit_check_request(
    db: Session,
    check_request_id: int,
    contractor: User
) -> CheckRequest:
    if contractor.role != UserRole.CONTRACTOR.value:
        raise ForbiddenException("Only Contractor can submit Check Requests.")

    cr = db.query(CheckRequest).filter(CheckRequest.id == check_request_id).first()
    if not cr:
        raise NotFoundException(f"Check Request {check_request_id} not found")

    WorkflowStateMachine.validate_transition(cr.status, WorkflowState.SUBMITTED.value, contractor.role)

    cr.status = WorkflowState.SUBMITTED.value

    # Auto trigger AI pre-review
    boq_item = cr.boq_item
    evidence_names = [e.filename for e in cr.evidences]

    ai_output = AiClient.get_pre_review(
        item_number=boq_item.item_number,
        category=boq_item.category,
        description=boq_item.description,
        contract_qty=to_decimal(boq_item.contract_qty),
        proposed_qty=to_decimal(cr.proposed_qty),
        evidence_count=len(evidence_names),
        evidence_names=evidence_names
    )

    ai_review = AiReview(
        check_request_id=cr.id,
        readiness=ai_output.readiness,
        confidence_score=ai_output.confidence_score,
        missing_evidence=json.dumps(ai_output.missing_evidence),
        potential_issues=json.dumps(ai_output.potential_issues),
        suggested_checks=json.dumps(ai_output.suggested_checks),
        recommended_questions=json.dumps(ai_output.recommended_questions)
    )
    db.add(ai_review)

    # Transition to PENDING_INSPECTION
    cr.status = WorkflowState.PENDING_INSPECTION.value

    record_audit(
        db=db,
        actor=contractor,
        action=AuditAction.CR_SUBMITTED.value,
        entity_type="CHECK_REQUEST",
        entity_id=cr.cr_number,
        new_value={"status": cr.status, "ai_readiness": ai_output.readiness}
    )

    notify_role(
        db,
        UserRole.RE,
        title=f"New Check Request: {cr.cr_number}",
        message=f"{cr.title} ({cr.proposed_qty} {cr.unit}) submitted for inspection. AI Status: {ai_output.readiness}",
        link=f"/check-requests/{cr.id}"
    )

    db.commit()
    db.refresh(cr)
    return cr
