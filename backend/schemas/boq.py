from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class BoqItemResponse(BaseModel):
    id: int
    project_id: int
    item_number: int
    category: str
    description: str
    unit: str
    contract_qty: Decimal
    rate_pkr: Decimal
    amount_pkr: Decimal
    remark: Optional[str]
    is_active: int

    # Dynamic derived progress fields (calculated server-side!)
    approved_qty: Decimal = Decimal("0.00")
    remaining_qty: Decimal = Decimal("0.00")
    approved_amount_pkr: Decimal = Decimal("0.00")
    progress_pct: Decimal = Decimal("0.00")
    status: str = "Not Started"

    class Config:
        from_attributes = True

class BoqValidationReport(BaseModel):
    is_valid: bool
    item_count: int
    calculated_total_pkr: Decimal
    expected_total_pkr: Decimal
    difference_pkr: Decimal
    status_message: str
