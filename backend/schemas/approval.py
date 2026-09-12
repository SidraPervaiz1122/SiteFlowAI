from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime

class ReQuantityApprovalRequest(BaseModel):
    quantity_measurement_id: int
    approved_qty: Decimal
    re_comments: Optional[str] = None
    status: str = "APPROVED" # APPROVED or REJECTED

class QuantityApprovalResponse(BaseModel):
    id: int
    quantity_measurement_id: int
    boq_item_id: int
    approved_qty: Decimal
    contract_rate_pkr: Decimal
    approved_amount_pkr: Decimal
    re_id: int
    status: str
    re_comments: Optional[str]
    created_at: datetime
    
    # Metadata for UI
    cr_number: Optional[str] = None
    boq_item_description: Optional[str] = None
    boq_item_unit: Optional[str] = None
    client_review_status: Optional[str] = None

    class Config:
        from_attributes = True
