from decimal import Decimal
from typing import Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.boq_item import BoqItem
from backend.models.quantity_measurement import QuantityMeasurement
from backend.models.quantity_approval import QuantityApproval
from backend.models.check_request import CheckRequest
from backend.models.user import User
from backend.core.money import to_decimal, round_currency, round_quantity
from backend.core.exceptions import (
    NotFoundException,
    QuantityOverApprovalError,
    WorkflowTransitionError,
    ForbiddenException
)
from backend.core.enums import WorkflowState, UserRole, AuditAction
from backend.services.workflow.state_machine import WorkflowStateMachine
from backend.services.audit.audit_service import record_audit
from backend.services.notifications.notification_service import notify_role
from backend.schemas.quantity import QuantityCalculationContext

def calculate_boq_item_quantities(db: Session, boq_item_id: int) -> Tuple[Decimal, Decimal, Decimal]:
    """
    Returns (contract_qty, previously_approved_qty, remaining_qty) with exact Decimal precision.
    Authoritative calculation strictly on the backend.
    """
    boq_item = db.query(BoqItem).filter(BoqItem.id == boq_item_id).first()
    if not boq_item:
        raise NotFoundException(f"BOQ item with ID {boq_item_id} not found")

    contract_qty = to_decimal(boq_item.contract_qty)

    # Previously approved: SUM of all QuantityApproval with status='APPROVED' for this BOQ item
    prev_approved_query = (
        db.query(func.coalesce(func.sum(QuantityApproval.approved_qty), Decimal("0.0000")))
        .filter(
            QuantityApproval.boq_item_id == boq_item_id,
            QuantityApproval.status == "APPROVED"
        )
        .scalar()
    )
    previously_approved_qty = to_decimal(prev_approved_query)
    remaining_qty = max(Decimal("0.0000"), contract_qty - previously_approved_qty)

    return (contract_qty, previously_approved_qty, remaining_qty)

def get_quantity_context(db: Session, boq_item_id: int, submitted_qty: Decimal = Decimal("0.00")) -> QuantityCalculationContext:
    boq_item = db.query(BoqItem).filter(BoqItem.id == boq_item_id).first()
    if not boq_item:
        raise NotFoundException(f"BOQ item with ID {boq_item_id} not found")

    contract_qty, prev_approved, remaining = calculate_boq_item_quantities(db, boq_item_id)
    rate = to_decimal(boq_item.rate_pkr)
    recommended_amount = round_currency(to_decimal(submitted_qty) * rate)

    return QuantityCalculationContext(
        boq_item_id=boq_item_id,
        contract_qty=contract_qty,
        contract_rate_pkr=rate,
        previously_approved_qty=prev_approved,
        remaining_qty=remaining,
        submitted_qty=to_decimal(submitted_qty),
        recommended_amount_pkr=recommended_amount
    )

def submit_quantity(
    db: Session,
    check_request_id: int,
    submitted_qty: Decimal,
    contractor: User,
    contractor_notes: str = None
) -> QuantityMeasurement:
    """
    Contractor submits measured quantity for an inspected and accepted check request.
    """
    if contractor.role != UserRole.CONTRACTOR.value:
        raise ForbiddenException("Only Contractor can submit measured quantities.")

    cr = db.query(CheckRequest).filter(CheckRequest.id == check_request_id).first()
    if not cr:
        raise NotFoundException(f"Check Request {check_request_id} not found")

    # Workflow validation: Must be INSPECTION_ACCEPTED or resubmitted from RE_REJECTED
    WorkflowStateMachine.validate_transition(cr.status, WorkflowState.QUANTITY_SUBMITTED.value, contractor.role)

    submitted_dec = to_decimal(submitted_qty)
    if submitted_dec <= Decimal("0"):
        raise ValueError("Submitted quantity must be greater than zero.")

    # Create measurement record
    measurement = QuantityMeasurement(
        check_request_id=cr.id,
        boq_item_id=cr.boq_item_id,
        submitted_qty=submitted_dec,
        contractor_notes=contractor_notes,
        status="SUBMITTED",
        created_by_id=contractor.id
    )
    db.add(measurement)

    # Transition Check Request state
    cr.status = WorkflowState.QUANTITY_SUBMITTED.value

    # Audit log
    record_audit(
        db=db,
        actor=contractor,
        action=AuditAction.QUANTITY_SUBMITTED.value,
        entity_type="QUANTITY_MEASUREMENT",
        entity_id=str(cr.cr_number),
        new_value=str(submitted_dec),
        metadata={"boq_item_id": cr.boq_item_id, "check_request_id": cr.id}
    )

    notify_role(
        db,
        UserRole.RE,
        title="Quantity Submitted for Approval",
        message=f"Contractor submitted {submitted_dec} {cr.unit} for {cr.cr_number}",
        link=f"/check-requests/{cr.id}"
    )

    db.commit()
    db.refresh(measurement)
    return measurement

def process_re_quantity_approval(
    db: Session,
    quantity_measurement_id: int,
    approved_qty: Decimal,
    re: User,
    re_comments: str = None,
    status_decision: str = "APPROVED"
) -> QuantityApproval:
    """
    Resident Engineer (RE) reviews and authoritatively approves/rejects the measured quantity.
    Atomic check: Current Approved Qty <= Remaining Qty.
    RE cannot perform Client approval.
    """
    if re.role != UserRole.RE.value:
        raise ForbiddenException("Only Resident Engineer (RE) can approve measured quantities.")

    measurement = db.query(QuantityMeasurement).filter(QuantityMeasurement.id == quantity_measurement_id).first()
    if not measurement:
        raise NotFoundException(f"Quantity measurement {quantity_measurement_id} not found")

    cr = db.query(CheckRequest).filter(CheckRequest.id == measurement.check_request_id).first()
    boq_item = db.query(BoqItem).filter(BoqItem.id == measurement.boq_item_id).first()

    target_state = WorkflowState.RE_APPROVED.value if status_decision == "APPROVED" else WorkflowState.RE_REJECTED.value
    WorkflowStateMachine.validate_transition(cr.status, target_state, re.role)

    approved_dec = to_decimal(approved_qty)
    contract_rate = to_decimal(boq_item.rate_pkr)

    if status_decision == "APPROVED":
        if approved_dec <= Decimal("0"):
            raise ValueError("Approved quantity must be greater than zero.")

        # ATOMIC VALIDATION: Calculate remaining quantity strictly within transaction
        contract_qty, prev_approved, remaining = calculate_boq_item_quantities(db, boq_item.id)

        if approved_dec > remaining:
            raise QuantityOverApprovalError(
                submitted_qty=approved_dec,
                remaining_qty=remaining,
                boq_item_id=boq_item.id
            )

        approved_amount = round_currency(approved_dec * contract_rate)
    else:
        approved_dec = Decimal("0.0000")
        approved_amount = Decimal("0.00")

    approval = QuantityApproval(
        quantity_measurement_id=measurement.id,
        boq_item_id=boq_item.id,
        approved_qty=approved_dec,
        contract_rate_pkr=contract_rate,
        approved_amount_pkr=approved_amount,
        re_id=re.id,
        status=status_decision,
        re_comments=re_comments
    )
    db.add(approval)

    # Update measurement status and CR workflow status
    measurement.status = f"RE_{status_decision}"
    cr.status = target_state

    record_audit(
        db=db,
        actor=re,
        action=AuditAction.RE_QUANTITY_APPROVED.value if status_decision == "APPROVED" else AuditAction.RE_QUANTITY_REJECTED.value,
        entity_type="QUANTITY_APPROVAL",
        entity_id=str(cr.cr_number),
        new_value={"approved_qty": str(approved_dec), "amount_pkr": str(approved_amount)},
        metadata={"boq_item_id": boq_item.id, "re_comments": re_comments}
    )

    if status_decision == "APPROVED":
        # Automatically advance CR to CLIENT_REVIEW
        cr.status = WorkflowState.CLIENT_REVIEW.value
        notify_role(
            db,
            UserRole.CLIENT,
            title="Work Ready for Client Review",
            message=f"RE approved {approved_dec} {boq_item.unit} for {cr.cr_number}. Awaiting your final review.",
            link=f"/approvals"
        )

    db.commit()
    db.refresh(approval)
    return approval
