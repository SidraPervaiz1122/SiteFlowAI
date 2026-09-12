from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from sqlalchemy.sql import func
from backend.app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    covered_area_sqft = Column(Numeric(12, 2, asdecimal=True), nullable=False)
    contract_boq_total_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    contingency_pct = Column(Numeric(5, 2, asdecimal=True), nullable=False)
    budget_with_contingency_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    cost_per_sqft_pkr = Column(Numeric(10, 2, asdecimal=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
