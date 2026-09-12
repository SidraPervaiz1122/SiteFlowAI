from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.dependencies import get_current_user, require_contractor_user
from backend.models.user import User
from backend.models.quantity_measurement import QuantityMeasurement
from backend.schemas.quantity import (
    QuantitySubmitRequest,
    QuantityMeasurementResponse,
    QuantityCalculationContext
)
from backend.services.quantities.quantity_service import (
    submit_quantity,
    get_quantity_context
)

router = APIRouter(prefix="/quantities", tags=["Quantities"])

@router.get("/context/{boq_item_id}", response_model=QuantityCalculationContext)
def get_boq_quantity_context(
    boq_item_id: int,
    submitted_qty: Decimal = Decimal("0.00"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_quantity_context(db, boq_item_id, submitted_qty)

@router.post("/submit", response_model=QuantityMeasurementResponse)
def submit_contractor_quantity(
    req: QuantitySubmitRequest,
    db: Session = Depends(get_db),
    contractor: User = Depends(require_contractor_user)
):
    measurement = submit_quantity(
        db=db,
        check_request_id=req.check_request_id,
        submitted_qty=req.submitted_qty,
        contractor=contractor,
        contractor_notes=req.contractor_notes
    )
    return QuantityMeasurementResponse.model_validate(measurement)

@router.get("/measurements", response_model=List[QuantityMeasurementResponse])
def list_measurements(
    check_request_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(QuantityMeasurement).order_by(QuantityMeasurement.created_at.desc())
    if check_request_id:
        query = query.filter(QuantityMeasurement.check_request_id == check_request_id)
    return [QuantityMeasurementResponse.model_validate(m) for m in query.all()]
