import json
import os
from pathlib import Path
from decimal import Decimal
from sqlalchemy.orm import Session
from backend.app.database import engine, SessionLocal, Base
from backend.models.user import User
from backend.models.project import Project
from backend.models.boq_item import BoqItem
from backend.models.check_request import CheckRequest
from backend.models.evidence import Evidence
from backend.models.inspection import Inspection
from backend.models.observation import Observation
from backend.models.rag_document import RagDocument
from backend.models.audit_log import AuditLog
from backend.core.enums import UserRole, WorkflowState, InspectionDecision, AuditAction
from backend.services.auth.auth_service import get_password_hash
from backend.services.boq.boq_service import validate_boq_data
from backend.core.constants import (
    CONTRACT_BOQ_TOTAL_PKR,
    PROJECT_COVERED_AREA_SQFT,
    RECOMMENDED_CONTINGENCY_PCT,
    BUDGET_WITH_CONTINGENCY_PKR
)
from backend.core.money import to_decimal, round_currency

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def seed_database(reset: bool = True):
    if reset:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # 1. Seed Demo Users
        users_data = [
            {
                "email": "contractor@example.com",
                "password": "Contractor@123",
                "full_name": "Tariq Mahmood (Contractor)",
                "role": UserRole.CONTRACTOR.value
            },
            {
                "email": "re@example.com",
                "password": "Engineer@123",
                "full_name": "Engr. Bilal Khan (Resident Engineer)",
                "role": UserRole.RE.value
            },
            {
                "email": "client@example.com",
                "password": "Client@123",
                "full_name": "Malik Zafar (Project Client)",
                "role": UserRole.CLIENT.value
            }
        ]

        user_map = {}
        for u in users_data:
            user = User(
                email=u["email"],
                password_hash=get_password_hash(u["password"]),
                full_name=u["full_name"],
                role=u["role"],
                is_active=1
            )
            db.add(user)
            db.flush()
            user_map[u["role"]] = user

        # 2. Seed Project
        project = Project(
            code="SITEFLOW-5M",
            name="SiteFlow 5 Marla Model Residence",
            description="5 Marla Single-Storey Model Residence, Islamabad/Rawalpindi 2026",
            covered_area_sqft=PROJECT_COVERED_AREA_SQFT,
            contract_boq_total_pkr=CONTRACT_BOQ_TOTAL_PKR,
            contingency_pct=RECOMMENDED_CONTINGENCY_PCT,
            budget_with_contingency_pkr=BUDGET_WITH_CONTINGENCY_PKR,
            cost_per_sqft_pkr=Decimal("6847.38")
        )
        db.add(project)
        db.flush()

        # 3. Seed Exact 24 BOQ Items
        boq_file = DATA_DIR / "boq" / "siteflow_boq.json"
        with open(boq_file, "r", encoding="utf-8") as f:
            boq_items_data = json.load(f)

        # Validate strictly before seeding
        report = validate_boq_data(boq_items_data)
        if not report.is_valid:
            raise ValueError(f"BOQ Seed validation failed: {report.status_message}")

        boq_map = {}
        for item in boq_items_data:
            boq_obj = BoqItem(
                project_id=project.id,
                item_number=item["item_number"],
                category=item["category"],
                description=item["description"],
                unit=item["unit"],
                contract_qty=to_decimal(item["contract_qty"]),
                rate_pkr=to_decimal(item["rate_pkr"]),
                amount_pkr=to_decimal(item["amount_pkr"]),
                remark=item.get("remark"),
                is_active=1
            )
            db.add(boq_obj)
            db.flush()
            boq_map[item["item_number"]] = boq_obj

        # 4. Seed Knowledge Documents for RAG
        assumptions_file = DATA_DIR / "project" / "assumptions.json"
        with open(assumptions_file, "r", encoding="utf-8") as f:
            assumptions_data = json.load(f)

        rag_doc1 = RagDocument(
            source_type="ASSUMPTION",
            title="5 Marla Architectural & Engineering Assumptions",
            content=json.dumps(assumptions_data, indent=2),
            keywords="assumptions dimensions plot 5 marla covered area single storey rcc rebar plaster"
        )
        db.add(rag_doc1)

        takeoff_file = DATA_DIR / "project" / "takeoff.json"
        with open(takeoff_file, "r", encoding="utf-8") as f:
            takeoff_data = json.load(f)

        rag_doc2 = RagDocument(
            source_type="TAKEOFF",
            title="Quantity Takeoff Breakdown",
            content=json.dumps(takeoff_data, indent=2),
            keywords="takeoff measured quantities bbs structural footings beams slabs"
        )
        db.add(rag_doc2)

        # 5. Initial Audit Log
        audit_init = AuditLog(
            project_id=project.id,
            actor_name="SYSTEM_SEED",
            actor_role="SYSTEM",
            action="PROJECT_INITIALIZED",
            entity_type="PROJECT",
            entity_id=project.code,
            new_value=json.dumps({"boq_items": 24, "total_pkr": str(CONTRACT_BOQ_TOTAL_PKR)})
        )
        db.add(audit_init)

        db.commit()
        print("Database successfully seeded:")
        print(f"- Project: {project.name} (Code: {project.code})")
        print(f"- Contract Total: PKR {CONTRACT_BOQ_TOTAL_PKR:,.2f}")
        print(f"- Users: {len(users_data)} accounts created")
        print(f"- BOQ Items: {len(boq_items_data)} items loaded")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
