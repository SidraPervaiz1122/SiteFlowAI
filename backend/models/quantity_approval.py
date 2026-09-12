from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class QuantityApproval(Base):
    __tablename__ = "quantity_approvals"

    id = Column(Integer, primary_key=True, index=True)
    quantity_measurement_id = Column(Integer, ForeignKey("quantity_measurements.id"), nullable=False)
    boq_item_id = Column(Integer, ForeignKey("boq_items.id"), nullable=False)
    approved_qty = Column(Numeric(14, 4, asdecimal=True), nullable=False)
    contract_rate_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    approved_amount_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    re_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="APPROVED", index=True, nullable=False) # APPROVED, REJECTED
    re_comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    measurement = relationship("QuantityMeasurement", back_populates="approvals")
    boq_item = relationship("BoqItem", back_populates="quantity_approvals")
    re = relationship("User")
    client_reviews = relationship("ClientReview", back_populates="quantity_approval", cascade="all, delete-orphan")
    ipc_items = relationship("IpcItem", back_populates="quantity_approval")
