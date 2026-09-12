import json
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.schemas.boq import BoqItemResponse, BoqValidationReport
from backend.services.boq.boq_service import get_boq_items_with_progress, validate_boq_data
from backend.app.dependencies import get_current_user
from backend.models.user import User
from backend.models.boq_item import BoqItem
from backend.core.exceptions import ContractImmutabilityError

router = APIRouter(prefix="/boq", tags=["Bill of Quantities"])

@router.get("", response_model=List[BoqItemResponse])
def get_boq_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_boq_items_with_progress(db, project_id=1)

@router.get("/validate", response_model=BoqValidationReport)
def validate_contract_boq(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    json_path = Path(__file__).resolve().parent.parent / "data" / "boq" / "siteflow_boq.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return validate_boq_data(data)

@router.get("/{item_id}", response_model=BoqItemResponse)
def get_boq_item_detail(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = get_boq_items_with_progress(db, project_id=1)
    for it in items:
        if it.id == item_id or it.item_number == item_id:
            return it
    raise HTTPException(status_code=404, detail="BOQ item not found")

@router.post("")
def create_boq_item():
    raise HTTPException(status_code=403, detail="Contractual BOQ items are immutable during normal execution.")

@router.put("/{item_id}")
def update_boq_item(item_id: int):
    raise HTTPException(status_code=403, detail="Contractual BOQ quantities, rates, and descriptions are strictly immutable.")

@router.delete("/{item_id}")
def delete_boq_item(item_id: int):
    raise HTTPException(status_code=403, detail="Contractual BOQ items cannot be deleted.")
