from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.dependencies import get_current_user, require_client_user
from backend.models.user import User
from backend.models.client_review import ClientReview
from backend.schemas.client_review import ClientReviewRequest, ClientReviewResponse
from backend.services.approvals.client_review_service import process_client_review

router = APIRouter(prefix="/client-reviews", tags=["Client Reviews"])

@router.get("", response_model=List[ClientReviewResponse])
def list_client_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reviews = db.query(ClientReview).order_by(ClientReview.reviewed_at.desc()).all()
    return [ClientReviewResponse.model_validate(r) for r in reviews]

@router.post("", response_model=ClientReviewResponse)
def submit_client_review(
    req: ClientReviewRequest,
    db: Session = Depends(get_db),
    client: User = Depends(require_client_user)
):
    review = process_client_review(
        db=db,
        quantity_approval_id=req.quantity_approval_id,
        decision=req.decision,
        client=client,
        comments=req.comments
    )
    return ClientReviewResponse.model_validate(review)
