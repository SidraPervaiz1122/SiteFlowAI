from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.dependencies import get_current_user, require_re_user
from backend.models.user import User
from backend.models.inspection import Inspection
from backend.schemas.inspection import InspectionResponse, InspectionDecisionRequest
from backend.schemas.observation import ObservationResponse, ObservationCreateRequest
from backend.schemas.ai import AiObservationResponse, AiObservationDraftRequest
from backend.services.inspections.inspection_service import (
    get_or_create_inspection,
    draft_ai_observation,
    add_observation,
    decide_inspection
)

router = APIRouter(prefix="/inspections", tags=["Inspections"])

@router.post("/start/{check_request_id}", response_model=InspectionResponse)
def start_inspection(
    check_request_id: int,
    db: Session = Depends(get_db),
    re: User = Depends(require_re_user)
):
    inspection = get_or_create_inspection(db, check_request_id, re)
    return InspectionResponse.model_validate(inspection)

@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return InspectionResponse.model_validate(inspection)

@router.post("/{inspection_id}/ai-draft", response_model=AiObservationResponse)
def generate_ai_observation(
    inspection_id: int,
    hint: Optional[str] = None,
    db: Session = Depends(get_db),
    re: User = Depends(require_re_user)
):
    ai_obs = draft_ai_observation(db, inspection_id, re, hint)
    return AiObservationResponse.model_validate(ai_obs)

@router.post("/{inspection_id}/observations", response_model=ObservationResponse)
def create_observation(
    inspection_id: int,
    req: ObservationCreateRequest,
    db: Session = Depends(get_db),
    re: User = Depends(require_re_user)
):
    obs = add_observation(
        db=db,
        inspection_id=inspection_id,
        title=req.title,
        description=req.description,
        re=re,
        severity=req.severity,
        category=req.category,
        corrective_action=req.corrective_action,
        is_ai_generated=req.is_ai_generated
    )
    return ObservationResponse.model_validate(obs)

@router.post("/{inspection_id}/decide", response_model=InspectionResponse)
def make_inspection_decision(
    inspection_id: int,
    req: InspectionDecisionRequest,
    db: Session = Depends(get_db),
    re: User = Depends(require_re_user)
):
    inspection = decide_inspection(
        db=db,
        inspection_id=inspection_id,
        decision=req.decision,
        re=re,
        inspector_notes=req.inspector_notes,
        checklist_results=req.checklist_results
    )
    return InspectionResponse.model_validate(inspection)
