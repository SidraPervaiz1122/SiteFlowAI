from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class QuantityMeasurement(Base):
    __tablename__ = "quantity_measurements"

    id = Column(Integer, primary_key=True, index=True)
    check_request_id = Column(Integer, ForeignKey("check_requests.id"), nullable=False)
    boq_item_id = Column(Integer, ForeignKey("boq_items.id"), nullable=False)
    submitted_qty = Column(Numeric(14, 4, asdecimal=True), nullable=False)
    contractor_notes = Column(Text, nullable=True)
    status = Column(String(50), default="SUBMITTED", index=True, nullable=False) # SUBMITTED, RE_APPROVED, RE_REJECTED
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    check_request = relationship("CheckRequest", back_populates="quantity_measurements")
    boq_item = relationship("BoqItem", back_populates="quantity_measurements")
    created_by = relationship("User")
    approvals = relationship("QuantityApproval", back_populates="measurement", cascade="all, delete-orphan")
