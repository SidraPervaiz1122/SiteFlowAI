import json
from decimal import Decimal
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.boq_item import BoqItem
from backend.models.quantity_approval import QuantityApproval
from backend.models.client_review import ClientReview
from backend.models.check_request import CheckRequest
from backend.models.inspection import Inspection
from backend.models.ipc import Ipc
from backend.core.constants import (
    CONTRACT_BOQ_ITEM_COUNT,
    CONTRACT_BOQ_TOTAL_PKR,
    PROJECT_COVERED_AREA_SQFT,
    RECOMMENDED_CONTINGENCY_PCT,
    BUDGET_WITH_CONTINGENCY_PKR
)
from backend.core.money import to_decimal, round_currency, round_quantity
from backend.core.exceptions import IntegrityValidationError
from backend.schemas.boq import BoqValidationReport, BoqItemResponse
from backend.schemas.project import ProjectProgressSummary

def validate_boq_data(boq_data: List[dict]) -> BoqValidationReport:
    """Validate that imported/seeded BOQ matches exact 24 items and total PKR 5,135,535."""
    item_count = len(boq_data)
    total = Decimal("0.00")
    for item in boq_data:
        qty = to_decimal(item["contract_qty"])
        rate = to_decimal(item["rate_pkr"])
        expected_amount = round_currency(qty * rate)
        item_amount = round_currency(item["amount_pkr"])
        
        # Verify individual item math
        if abs(expected_amount - item_amount) > Decimal("0.05"):
            raise IntegrityValidationError(
                f"BOQ Item #{item.get('item_number')} calculation mismatch: {qty} * {rate} = {expected_amount}, given {item_amount}"
            )
        total += item_amount

    total = round_currency(total)
    diff = total - CONTRACT_BOQ_TOTAL_PKR
    is_valid = (item_count == CONTRACT_BOQ_ITEM_COUNT) and (abs(diff) < Decimal("0.01"))
    
    msg = "BOQ validation passed: exactly 24 items totaling PKR 5,135,535.00" if is_valid else f"Validation failed: Count {item_count} (exp {CONTRACT_BOQ_ITEM_COUNT}), Total {total} (exp {CONTRACT_BOQ_TOTAL_PKR})"
    
    return BoqValidationReport(
        is_valid=is_valid,
        item_count=item_count,
        calculated_total_pkr=total,
        expected_total_pkr=CONTRACT_BOQ_TOTAL_PKR,
        difference_pkr=diff,
        status_message=msg
    )

def get_boq_items_with_progress(db: Session, project_id: int = 1) -> List[BoqItemResponse]:
    """
    Returns all BOQ items with authoritative server-calculated progress,
    cumulative approved quantities, and remaining contract quantities.
    """
    items = db.query(BoqItem).filter(BoqItem.project_id == project_id).order_by(BoqItem.item_number).all()

    # Query all approved quantities that have been accepted by RE
    # Authoritative approved quantities are QuantityApproval with status='APPROVED'
    approvals = (
        db.query(QuantityApproval.boq_item_id, func.sum(QuantityApproval.approved_qty).label("total_approved"))
        .filter(QuantityApproval.status == "APPROVED")
        .group_by(QuantityApproval.boq_item_id)
        .all()
    )
    approved_map = {row[0]: to_decimal(row[1]) for row in approvals}

    result = []
    for item in items:
        contract_qty = to_decimal(item.contract_qty)
        rate = to_decimal(item.rate_pkr)
        approved_qty = approved_map.get(item.id, Decimal("0.0000"))
        remaining_qty = max(Decimal("0.0000"), contract_qty - approved_qty)
        approved_amount = round_currency(approved_qty * rate)

        progress_pct = Decimal("0.00")
        if contract_qty > Decimal("0"):
            progress_pct = round_currency((approved_qty / contract_qty) * Decimal("100.00"))

        status = "Not Started"
        if approved_qty >= contract_qty and contract_qty > Decimal("0"):
            status = "Fully Approved"
        elif approved_qty > Decimal("0"):
            status = "Partially Approved"
        else:
            # Check if any check request exists
            cr_count = db.query(CheckRequest).filter(CheckRequest.boq_item_id == item.id).count()
            if cr_count > 0:
                status = "In Progress"

        resp = BoqItemResponse(
            id=item.id,
            project_id=item.project_id,
            item_number=item.item_number,
            category=item.category,
            description=item.description,
            unit=item.unit,
            contract_qty=contract_qty,
            rate_pkr=rate,
            amount_pkr=round_currency(item.amount_pkr),
            remark=item.remark,
            is_active=item.is_active,
            approved_qty=round_quantity(approved_qty),
            remaining_qty=round_quantity(remaining_qty),
            approved_amount_pkr=approved_amount,
            progress_pct=progress_pct,
            status=status
        )
        result.append(resp)

    return result

def get_project_progress_summary(db: Session, project_id: int = 1) -> ProjectProgressSummary:
    """Calculates comprehensive executive progress and financial KPIs."""
    boq_items = get_boq_items_with_progress(db, project_id)

    contract_total = CONTRACT_BOQ_TOTAL_PKR
    approved_total = Decimal("0.00")

    for it in boq_items:
        approved_total += it.approved_amount_pkr

    approved_total = round_currency(approved_total)
    remaining_total = max(Decimal("0.00"), contract_total - approved_total)

    financial_progress = round_currency((approved_total / contract_total) * Decimal("100.00")) if contract_total > 0 else Decimal("0.00")

    # Counts
    pending_inspections = db.query(CheckRequest).filter(
        CheckRequest.status.in_(["SUBMITTED", "AI_PRE_REVIEW", "PENDING_INSPECTION", "INSPECTION_IN_PROGRESS"])
    ).count()

    pending_re_approvals = db.query(CheckRequest).filter(
        CheckRequest.status.in_(["INSPECTION_ACCEPTED", "QUANTITY_SUBMITTED"])
    ).count()

    pending_client_approvals = db.query(CheckRequest).filter(
        CheckRequest.status.in_(["RE_APPROVED", "CLIENT_REVIEW"])
    ).count()

    # IPC values
    ipcs = db.query(Ipc).filter(Ipc.project_id == project_id).all()
    ipc_cumulative = Decimal("0.00")
    ipc_current = Decimal("0.00")
    if ipcs:
        ipc_cumulative = round_currency(sum(to_decimal(i.total_current_amount_pkr) for i in ipcs))
        ipc_current = round_currency(to_decimal(ipcs[-1].total_current_amount_pkr))

    return ProjectProgressSummary(
        contract_value_pkr=contract_total,
        approved_value_pkr=approved_total,
        remaining_value_pkr=remaining_total,
        physical_progress_pct=financial_progress, # Weighted physical progress matches approved value
        financial_progress_pct=financial_progress,
        pending_inspections=pending_inspections,
        pending_re_approvals=pending_re_approvals,
        pending_client_approvals=pending_client_approvals,
        ipc_current_value_pkr=ipc_current,
        ipc_cumulative_value_pkr=ipc_cumulative
    )
