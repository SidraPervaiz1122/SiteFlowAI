from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime

class QuantitySubmitRequest(BaseModel):
    check_request_id: int
    submitted_qty: Decimal
    contractor_notes: Optional[str] = None

class QuantityMeasurementResponse(BaseModel):
    id: int
    check_request_id: int
    boq_item_id: int
    submitted_qty: Decimal
    contractor_notes: Optional[str]
    status: str
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class QuantityCalculationContext(BaseModel):
    boq_item_id: int
    contract_qty: Decimal
    contract_rate_pkr: Decimal
    previously_approved_qty: Decimal
    remaining_qty: Decimal
    submitted_qty: Decimal
    recommended_amount_pkr: Decimal
