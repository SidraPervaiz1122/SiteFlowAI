from pydantic import BaseModel
from decimal import Decimal
from typing import Optional, List
from datetime import date, datetime

class IpcGenerateRequest(BaseModel):
    period_start: date
    period_end: date
    notes: Optional[str] = None

class IpcItemResponse(BaseModel):
    id: int
    ipc_id: int
    boq_item_id: int
    quantity_approval_id: int
    item_number: int
    category: str
    description: str
    unit: str
    approved_qty: Decimal
    contract_rate_pkr: Decimal
    amount_pkr: Decimal

    class Config:
        from_attributes = True

class IpcResponse(BaseModel):
    id: int
    project_id: int
    ipc_number: str
    period_start: date
    period_end: date
    total_current_amount_pkr: Decimal
    cumulative_amount_pkr: Decimal
    status: str
    notes: Optional[str]
    created_by_id: int
    created_at: datetime
    items: List[IpcItemResponse] = []

    class Config:
        from_attributes = True

class IpcEligibilitySummary(BaseModel):
    eligible_items_count: int
    total_eligible_amount_pkr: Decimal
    items: List[dict] = []
