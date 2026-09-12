import re
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.models.boq_item import BoqItem
from backend.models.check_request import CheckRequest
from backend.models.quantity_approval import QuantityApproval
from backend.models.inspection import Inspection
from backend.models.observation import Observation
from backend.core.money import format_currency, format_quantity, to_decimal
from backend.services.quantities.quantity_service import calculate_boq_item_quantities
from backend.core.constants import CONTRACT_BOQ_TOTAL_PKR, PROJECT_COVERED_AREA_SQFT

class HybridRetriever:
    """
    Practical hybrid keyword and context retriever across project contracts,
    takeoff notes, BOQ, and real-time database state.
    """

    @classmethod
    def query(cls, db: Session, query_text: str) -> Dict[str, Any]:
        q = query_text.lower().strip()
        sources = []
        answer_parts = []

        # 1. Total Contract Value / Cost per sqft
        if any(term in q for term in ["contract total", "total value", "total cost", "total boq", "budget"]):
            sources.append({"type": "CONTRACT_SPEC", "title": "Contract Total & Budget"})
            return {
                "answer": (
                    f"The contractual BOQ total is {format_currency(CONTRACT_BOQ_TOTAL_PKR)} for a covered area of "
                    f"{PROJECT_COVERED_AREA_SQFT} sq.ft. (approx. PKR 6,847.38 per sq.ft.). With a recommended 5% "
                    f"contingency allowance (PKR 256,776.75), the total budget is PKR 5,392,311.75."
                ),
                "sources": sources,
                "is_fallback": True
            }

        # 2. Specific BOQ Item Rate or Quantity
        items = db.query(BoqItem).all()
        matched_item = None
        for item in items:
            cat = item.category.lower()
            desc = item.description.lower()
            if cat in q or any(word in q for word in desc.split() if len(word) > 4):
                matched_item = item
                break
            # Match by item number
            if f"item {item.item_number}" in q or f"item #{item.item_number}" in q or f"#{item.item_number}" in q:
                matched_item = item
                break

        if matched_item:
            sources.append({"type": "BOQ", "title": f"BOQ Item #{matched_item.item_number} - {matched_item.category}"})
            contract_qty, prev_approved, remaining = calculate_boq_item_quantities(db, matched_item.id)

            if any(term in q for term in ["remaining", "balance", "left"]):
                return {
                    "answer": (
                        f"For BOQ Item #{matched_item.item_number} ({matched_item.category} - {matched_item.description}):\n"
                        f"• Contract Quantity: {format_quantity(contract_qty)} {matched_item.unit}\n"
                        f"• Previously Approved: {format_quantity(prev_approved)} {matched_item.unit}\n"
                        f"• Remaining Quantity: {format_quantity(remaining)} {matched_item.unit}\n"
                        f"• Contract Rate: {format_currency(matched_item.rate_pkr)} per {matched_item.unit}"
                    ),
                    "sources": sources,
                    "is_fallback": True
                }
            elif any(term in q for term in ["rate", "price", "cost"]):
                return {
                    "answer": (
                        f"The contractual rate for BOQ Item #{matched_item.item_number} ({matched_item.category} - "
                        f"{matched_item.description}) is {format_currency(matched_item.rate_pkr)} per {matched_item.unit}. "
                        f"Total contract amount for this item is {format_currency(matched_item.amount_pkr)}."
                    ),
                    "sources": sources,
                    "is_fallback": True
                }
            else:
                return {
                    "answer": (
                        f"BOQ Item #{matched_item.item_number}: {matched_item.category} — {matched_item.description}\n"
                        f"• Unit: {matched_item.unit}\n"
                        f"• Contract Quantity: {format_quantity(contract_qty)}\n"
                        f"• Contract Rate: {format_currency(matched_item.rate_pkr)}\n"
                        f"• Total Amount: {format_currency(matched_item.amount_pkr)}\n"
                        f"• Remaining Quantity: {format_quantity(remaining)} {matched_item.unit}"
                    ),
                    "sources": sources,
                    "is_fallback": True
                }

        # 3. Pending Inspections / Check Requests
        if any(term in q for term in ["pending inspection", "pending check request", "inspections pending"]):
            pending_crs = db.query(CheckRequest).filter(
                CheckRequest.status.in_(["SUBMITTED", "AI_PRE_REVIEW", "PENDING_INSPECTION", "INSPECTION_IN_PROGRESS"])
            ).all()
            sources.append({"type": "DATABASE", "title": "Check Requests Status"})
            if not pending_crs:
                return {
                    "answer": "There are currently no pending site inspections awaiting review.",
                    "sources": sources,
                    "is_fallback": True
                }
            details = "\n".join([f"• {cr.cr_number}: {cr.title} ({cr.proposed_qty} {cr.unit}) - Status: {cr.status}" for cr in pending_crs])
            return {
                "answer": f"Currently pending site inspections ({len(pending_crs)} total):\n{details}",
                "sources": sources,
                "is_fallback": True
            }

        # 4. Check Request Specific Details (e.g. CR-001)
        cr_match = re.search(r'cr-00\d|cr-\d+', q)
        if cr_match:
            cr_num = cr_match.group(0).upper()
            cr = db.query(CheckRequest).filter(CheckRequest.cr_number == cr_num).first()
            if cr:
                sources.append({"type": "DATABASE", "title": f"Check Request {cr.cr_number}"})
                ev_names = [e.filename for e in cr.evidences]
                ev_summary = f"{len(ev_names)} attached files: {', '.join(ev_names)}" if ev_names else "No evidence attached"
                return {
                    "answer": (
                        f"Check Request {cr.cr_number}: {cr.title}\n"
                        f"• Status: {cr.status}\n"
                        f"• Proposed Quantity: {format_quantity(cr.proposed_qty)} {cr.unit}\n"
                        f"• Attached Evidence: {ev_summary}"
                    ),
                    "sources": sources,
                    "is_fallback": True
                }

        # 5. Latest Observation
        if any(term in q for term in ["latest observation", "recent observation", "observations"]):
            obs = db.query(Observation).order_by(Observation.created_at.desc()).first()
            if obs:
                sources.append({"type": "DATABASE", "title": "Site Observations"})
                return {
                    "answer": (
                        f"Latest recorded site observation:\n"
                        f"• Title: {obs.title} [{obs.severity} / {obs.category}]\n"
                        f"• Description: {obs.description}\n"
                        f"• Corrective Action: {obs.corrective_action or 'None recorded'}"
                    ),
                    "sources": sources,
                    "is_fallback": True
                }
            else:
                return {
                    "answer": "No site observations have been recorded yet.",
                    "sources": sources,
                    "is_fallback": True
                }

        # Guardrail Fallback: If not found, do not hallucinate
        return {
            "answer": "I could not find sufficient project information to answer that reliably.",
            "sources": [],
            "is_fallback": True
        }
