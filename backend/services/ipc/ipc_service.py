from datetime import date
from decimal import Decimal
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.ipc import Ipc, IpcItem
from backend.models.quantity_approval import QuantityApproval
from backend.models.client_review import ClientReview
from backend.models.check_request import CheckRequest
from backend.models.boq_item import BoqItem
from backend.models.user import User
from backend.core.enums import WorkflowState, UserRole, AuditAction
from backend.core.money import to_decimal, round_currency
from backend.core.exceptions import SiteFlowException, ForbiddenException
from backend.core.constants import CONTRACT_BOQ_TOTAL_PKR
from backend.services.audit.audit_service import record_audit
from backend.services.notifications.notification_service import notify_role

def get_eligible_approvals_for_ipc(db: Session, project_id: int = 1) -> List[QuantityApproval]:
    """
    Returns quantity approvals that are CLIENT_APPROVED / IPC_ELIGIBLE
    and have not yet been included in any generated IPC.
    """
    # Subquery of approvals already included in an IPC
    already_included_subq = db.query(IpcItem.quantity_approval_id)

    eligible = (
        db.query(QuantityApproval)
        .join(ClientReview, ClientReview.quantity_approval_id == QuantityApproval.id)
        .join(BoqItem, BoqItem.id == QuantityApproval.boq_item_id)
        .filter(
            BoqItem.project_id == project_id,
            QuantityApproval.status == "APPROVED",
            ClientReview.decision == "APPROVED",
            ~QuantityApproval.id.in_(already_included_subq)
        )
        .all()
    )
    return eligible

def generate_ipc(
    db: Session,
    project_id: int,
    period_start: date,
    period_end: date,
    created_by: User,
    notes: str = None
) -> Ipc:
    """
    Generates a new Interim Payment Certificate strictly from Client-approved quantities.
    Enforces amount = quantity * contract_rate. No arbitrary sums permitted.
    """
    if created_by.role not in [UserRole.RE.value, UserRole.CLIENT.value]:
        raise ForbiddenException("Only RE or Client can initiate IPC generation.")

    eligible_approvals = get_eligible_approvals_for_ipc(db, project_id)
    if not eligible_approvals:
        raise SiteFlowException("No Client-approved items eligible for IPC generation.")

    # Determine next IPC sequence number
    existing_count = db.query(Ipc).filter(Ipc.project_id == project_id).count()
    ipc_number = f"IPC-{existing_count + 1:03d}"

    # Calculate previous cumulative IPC total
    prev_cumulative = (
        db.query(func.coalesce(func.sum(Ipc.total_current_amount_pkr), Decimal("0.00")))
        .filter(Ipc.project_id == project_id)
        .scalar()
    )
    prev_cumulative_dec = to_decimal(prev_cumulative)

    current_total = Decimal("0.00")
    ipc_items_to_create = []

    for approval in eligible_approvals:
        qty = to_decimal(approval.approved_qty)
        rate = to_decimal(approval.contract_rate_pkr)
        item_amount = round_currency(qty * rate)
        current_total += item_amount

        ipc_item = IpcItem(
            boq_item_id=approval.boq_item_id,
            quantity_approval_id=approval.id,
            approved_qty=qty,
            contract_rate_pkr=rate,
            amount_pkr=item_amount
        )
        ipc_items_to_create.append((ipc_item, approval))

    current_total = round_currency(current_total)
    new_cumulative = round_currency(prev_cumulative_dec + current_total)

    ipc = Ipc(
        project_id=project_id,
        ipc_number=ipc_number,
        period_start=period_start,
        period_end=period_end,
        total_current_amount_pkr=current_total,
        cumulative_amount_pkr=new_cumulative,
        status="CERTIFIED",
        notes=notes,
        created_by_id=created_by.id
    )
    db.add(ipc)
    db.flush() # obtain ipc.id

    for item, approval in ipc_items_to_create:
        item.ipc_id = ipc.id
        db.add(item)
        # Update check request workflow status to IPC_INCLUDED
        if approval.measurement and approval.measurement.check_request:
            approval.measurement.check_request.status = WorkflowState.IPC_INCLUDED.value

    record_audit(
        db=db,
        actor=created_by,
        action=AuditAction.IPC_GENERATED.value,
        entity_type="IPC",
        entity_id=ipc.ipc_number,
        new_value={"total_current": str(current_total), "cumulative": str(new_cumulative), "items_count": len(ipc_items_to_create)},
        metadata={"period_start": str(period_start), "period_end": str(period_end)}
    )

    notify_role(
        db,
        UserRole.CLIENT,
        title=f"New IPC Generated: {ipc.ipc_number}",
        message=f"{ipc.ipc_number} has been generated with value PKR {current_total:,.2f}",
        link=f"/ipc/{ipc.id}"
    )
    notify_role(
        db,
        UserRole.CONTRACTOR,
        title=f"New IPC Generated: {ipc.ipc_number}",
        message=f"{ipc.ipc_number} has been generated with value PKR {current_total:,.2f}",
        link=f"/ipc/{ipc.id}"
    )

    db.commit()
    db.refresh(ipc)
    return ipc
