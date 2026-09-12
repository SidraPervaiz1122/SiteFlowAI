from sqlalchemy.orm import Session
from backend.models.quantity_approval import QuantityApproval
from backend.models.client_review import ClientReview
from backend.models.check_request import CheckRequest
from backend.models.user import User
from backend.core.enums import WorkflowState, UserRole, AuditAction
from backend.core.exceptions import (
    NotFoundException,
    ForbiddenException,
    WorkflowTransitionError
)
from backend.services.workflow.state_machine import WorkflowStateMachine
from backend.services.audit.audit_service import record_audit
from backend.services.notifications.notification_service import notify_role

def process_client_review(
    db: Session,
    quantity_approval_id: int,
    decision: str, # "APPROVED" or "REJECTED"
    client: User,
    comments: str = None
) -> ClientReview:
    """
    Client reviews work certified by RE.
    STRICT: RE is forbidden from executing this method.
    Once approved by Client, the work is marked IPC_ELIGIBLE.
    """
    if client.role != UserRole.CLIENT.value:
        raise ForbiddenException(f"Only Client can perform Client Review. Current role '{client.role}' is not authorized.")

    approval = db.query(QuantityApproval).filter(QuantityApproval.id == quantity_approval_id).first()
    if not approval:
        raise NotFoundException(f"Quantity approval {quantity_approval_id} not found")

    measurement = approval.measurement
    cr = measurement.check_request

    target_state = WorkflowState.CLIENT_APPROVED.value if decision == "APPROVED" else WorkflowState.CLIENT_REJECTED.value
    WorkflowStateMachine.validate_transition(cr.status, target_state, client.role)

    review = ClientReview(
        quantity_approval_id=approval.id,
        client_id=client.id,
        decision=decision,
        comments=comments
    )
    db.add(review)

    if decision == "APPROVED":
        cr.status = WorkflowState.CLIENT_APPROVED.value
        # Immediately mark as eligible for IPC
        cr.status = WorkflowState.IPC_ELIGIBLE.value
        action = AuditAction.CLIENT_APPROVED.value
    else:
        cr.status = WorkflowState.CLIENT_REJECTED.value
        action = AuditAction.CLIENT_REJECTED.value

    record_audit(
        db=db,
        actor=client,
        action=action,
        entity_type="CLIENT_REVIEW",
        entity_id=str(cr.cr_number),
        new_value={"decision": decision, "comments": comments, "approved_qty": str(approval.approved_qty)},
        metadata={"boq_item_id": approval.boq_item_id, "amount_pkr": str(approval.approved_amount_pkr)}
    )

    notify_role(
        db,
        UserRole.CONTRACTOR,
        title=f"Client Review: {decision}",
        message=f"Client has {decision.lower()} work for {cr.cr_number} ({approval.approved_amount_pkr} PKR).",
        link=f"/check-requests/{cr.id}"
    )

    db.commit()
    db.refresh(review)
    return review
