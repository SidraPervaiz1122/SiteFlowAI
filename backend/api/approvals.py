from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.dependencies import get_current_user, require_re_user
from backend.models.user import User
from backend.models.quantity_approval import QuantityApproval
from backend.schemas.approval import ReQuantityApprovalRequest, QuantityApprovalResponse
from backend.services.quantities.quantity_service import process_re_quantity_approval

router = APIRouter(prefix="/approvals", tags=["Approvals"])

def build_approval_response(appr: QuantityApproval) -> QuantityApprovalResponse:
    boq = appr.boq_item
    cr = appr.measurement.check_request if appr.measurement else None
    client_review = appr.client_reviews[0] if appr.client_reviews else None

    return QuantityApprovalResponse(
        id=appr.id,
        quantity_measurement_id=appr.quantity_measurement_id,
        boq_item_id=appr.boq_item_id,
        approved_qty=appr.approved_qty,
        contract_rate_pkr=appr.contract_rate_pkr,
        approved_amount_pkr=appr.approved_amount_pkr,
        re_id=appr.re_id,
        status=appr.status,
        re_comments=appr.re_comments,
        created_at=appr.created_at,
        cr_number=cr.cr_number if cr else None,
        boq_item_description=boq.description if boq else None,
        boq_item_unit=boq.unit if boq else None,
        client_review_status=client_review.decision if client_review else "PENDING"
    )

@router.get("", response_model=List[QuantityApprovalResponse])
def list_approvals(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(QuantityApproval).order_by(QuantityApproval.created_at.desc())
    if status:
        query = query.filter(QuantityApproval.status == status)
    approvals = query.all()
    return [build_approval_response(a) for a in approvals]

@router.post("/re", response_model=QuantityApprovalResponse)
def re_approve_quantity(
    req: ReQuantityApprovalRequest,
    db: Session = Depends(get_db),
    re: User = Depends(require_re_user)
):
    approval = process_re_quantity_approval(
        db=db,
        quantity_measurement_id=req.quantity_measurement_id,
        approved_qty=req.approved_qty,
        re=re,
        re_comments=req.re_comments,
        status_decision=req.status
    )
    return build_approval_response(approval)
