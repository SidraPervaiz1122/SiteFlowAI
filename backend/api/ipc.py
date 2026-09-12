from typing import List
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.dependencies import get_current_user, require_re_or_client_user
from backend.models.user import User
from backend.models.ipc import Ipc
from backend.schemas.ipc import (
    IpcResponse,
    IpcGenerateRequest,
    IpcEligibilitySummary,
    IpcItemResponse
)
from backend.services.ipc.ipc_service import (
    get_eligible_approvals_for_ipc,
    generate_ipc
)
from backend.core.money import to_decimal, round_currency

router = APIRouter(prefix="/ipc", tags=["Interim Payment Certificates"])

def build_ipc_response(ipc: Ipc) -> IpcResponse:
    items_resp = []
    for it in ipc.items:
        boq = it.boq_item
        items_resp.append(IpcItemResponse(
            id=it.id,
            ipc_id=it.ipc_id,
            boq_item_id=it.boq_item_id,
            quantity_approval_id=it.quantity_approval_id,
            item_number=boq.item_number if boq else 0,
            category=boq.category if boq else "",
            description=boq.description if boq else "",
            unit=boq.unit if boq else "",
            approved_qty=it.approved_qty,
            contract_rate_pkr=it.contract_rate_pkr,
            amount_pkr=it.amount_pkr
        ))

    return IpcResponse(
        id=ipc.id,
        project_id=ipc.project_id,
        ipc_number=ipc.ipc_number,
        period_start=ipc.period_start,
        period_end=ipc.period_end,
        total_current_amount_pkr=ipc.total_current_amount_pkr,
        cumulative_amount_pkr=ipc.cumulative_amount_pkr,
        status=ipc.status,
        notes=ipc.notes,
        created_by_id=ipc.created_by_id,
        created_at=ipc.created_at,
        items=items_resp
    )

@router.get("/eligible", response_model=IpcEligibilitySummary)
def check_ipc_eligibility(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    eligible = get_eligible_approvals_for_ipc(db, project_id=1)
    total_amount = Decimal("0.00")
    items_data = []

    for app in eligible:
        amt = to_decimal(app.approved_amount_pkr)
        total_amount += amt
        boq = app.boq_item
        items_data.append({
            "approval_id": app.id,
            "boq_item_id": app.boq_item_id,
            "item_number": boq.item_number if boq else None,
            "category": boq.category if boq else None,
            "description": boq.description if boq else None,
            "approved_qty": str(app.approved_qty),
            "rate_pkr": str(app.contract_rate_pkr),
            "amount_pkr": str(amt)
        })

    return IpcEligibilitySummary(
        eligible_items_count=len(eligible),
        total_eligible_amount_pkr=round_currency(total_amount),
        items=items_data
    )

@router.get("", response_model=List[IpcResponse])
def list_ipcs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ipcs = db.query(Ipc).order_by(Ipc.created_at.desc()).all()
    return [build_ipc_response(i) for i in ipcs]

@router.get("/{ipc_id}", response_model=IpcResponse)
def get_ipc_detail(
    ipc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ipc = db.query(Ipc).filter(Ipc.id == ipc_id).first()
    if not ipc:
        raise HTTPException(status_code=404, detail="IPC not found")
    return build_ipc_response(ipc)

@router.post("/generate", response_model=IpcResponse)
def create_ipc(
    req: IpcGenerateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_re_or_client_user)
):
    ipc = generate_ipc(
        db=db,
        project_id=1,
        period_start=req.period_start,
        period_end=req.period_end,
        created_by=user,
        notes=req.notes
    )
    return build_ipc_response(ipc)
