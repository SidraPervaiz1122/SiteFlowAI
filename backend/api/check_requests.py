import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.dependencies import get_current_user, require_contractor_user
from backend.models.user import User
from backend.models.check_request import CheckRequest
from backend.models.evidence import Evidence
from backend.schemas.check_request import CheckRequestCreate, CheckRequestResponse
from backend.schemas.evidence import EvidenceResponse
from backend.services.check_requests.check_request_service import (
    create_check_request,
    attach_evidence,
    submit_check_request
)
from backend.app.config import settings

router = APIRouter(prefix="/check-requests", tags=["Check Requests"])

def build_cr_response(cr: CheckRequest) -> CheckRequestResponse:
    boq = cr.boq_item
    resp = CheckRequestResponse(
        id=cr.id,
        project_id=cr.project_id,
        boq_item_id=cr.boq_item_id,
        cr_number=cr.cr_number,
        title=cr.title,
        description=cr.description,
        proposed_qty=cr.proposed_qty,
        unit=cr.unit,
        status=cr.status,
        created_by_id=cr.created_by_id,
        created_at=cr.created_at,
        updated_at=cr.updated_at,
        boq_item_category=boq.category if boq else None,
        boq_item_description=boq.description if boq else None,
        boq_item_rate_pkr=boq.rate_pkr if boq else None,
        evidences=[EvidenceResponse.model_validate(e) for e in cr.evidences],
        ai_reviews=cr.ai_reviews,
        inspections=cr.inspections
    )
    return resp

@router.get("", response_model=List[CheckRequestResponse])
def list_check_requests(
    status: Optional[str] = None,
    boq_item_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(CheckRequest).order_by(CheckRequest.created_at.desc())
    if status:
        query = query.filter(CheckRequest.status == status)
    if boq_item_id:
        query = query.filter(CheckRequest.boq_item_id == boq_item_id)
    crs = query.all()
    return [build_cr_response(cr) for cr in crs]

@router.post("", response_model=CheckRequestResponse)
def create_cr(
    req: CheckRequestCreate,
    db: Session = Depends(get_db),
    contractor: User = Depends(require_contractor_user)
):
    cr = create_check_request(
        db=db,
        project_id=1,
        boq_item_id=req.boq_item_id,
        title=req.title,
        proposed_qty=req.proposed_qty,
        contractor=contractor,
        description=req.description
    )
    return build_cr_response(cr)

@router.get("/{cr_id}", response_model=CheckRequestResponse)
def get_cr_detail(
    cr_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cr = db.query(CheckRequest).filter(CheckRequest.id == cr_id).first()
    if not cr:
        raise HTTPException(status_code=404, detail="Check Request not found")
    return build_cr_response(cr)

@router.post("/{cr_id}/evidence", response_model=EvidenceResponse)
def upload_cr_evidence(
    cr_id: int,
    file: UploadFile = File(...),
    caption: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cr = db.query(CheckRequest).filter(CheckRequest.id == cr_id).first()
    if not cr:
        raise HTTPException(status_code=404, detail="Check Request not found")

    # Save file to uploads folder
    safe_filename = f"CR_{cr_id}_{os.path.basename(file.filename)}"
    destination = os.path.join(settings.UPLOADS_DIR, safe_filename)
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(destination)
    evidence = attach_evidence(
        db=db,
        check_request_id=cr.id,
        filename=file.filename,
        file_path=destination,
        file_type=file.content_type or "application/octet-stream",
        file_size_bytes=file_size,
        uploaded_by=current_user,
        caption=caption
    )
    return EvidenceResponse.model_validate(evidence)

@router.post("/{cr_id}/submit", response_model=CheckRequestResponse)
def submit_cr(
    cr_id: int,
    db: Session = Depends(get_db),
    contractor: User = Depends(require_contractor_user)
):
    cr = submit_check_request(db, cr_id, contractor)
    return build_cr_response(cr)
