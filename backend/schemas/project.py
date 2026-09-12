from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProjectResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    covered_area_sqft: Decimal
    contract_boq_total_pkr: Decimal
    contingency_pct: Decimal
    budget_with_contingency_pkr: Decimal
    cost_per_sqft_pkr: Decimal

    class Config:
        from_attributes = True

class ProjectProgressSummary(BaseModel):
    contract_value_pkr: Decimal
    approved_value_pkr: Decimal
    remaining_value_pkr: Decimal
    physical_progress_pct: Decimal
    financial_progress_pct: Decimal
    pending_inspections: int
    pending_re_approvals: int
    pending_client_approvals: int
    ipc_current_value_pkr: Decimal
    ipc_cumulative_value_pkr: Decimal
