from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class BoqItem(Base):
    __tablename__ = "boq_items"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    item_number = Column(Integer, index=True, nullable=False) # 1 to 24
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    unit = Column(String(20), nullable=False)
    contract_qty = Column(Numeric(14, 4, asdecimal=True), nullable=False)
    rate_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    amount_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    remark = Column(Text, nullable=True)
    is_active = Column(Integer, default=1)

    # Relationships
    project = relationship("Project")
    check_requests = relationship("CheckRequest", back_populates="boq_item")
    quantity_measurements = relationship("QuantityMeasurement", back_populates="boq_item")
    quantity_approvals = relationship("QuantityApproval", back_populates="boq_item")
