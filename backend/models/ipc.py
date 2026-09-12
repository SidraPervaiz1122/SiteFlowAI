from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class Ipc(Base):
    __tablename__ = "ipcs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    ipc_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. IPC-001
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    total_current_amount_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    cumulative_amount_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    status = Column(String(50), default="CERTIFIED", nullable=False)
    notes = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project")
    created_by = relationship("User")
    items = relationship("IpcItem", back_populates="ipc", cascade="all, delete-orphan")

class IpcItem(Base):
    __tablename__ = "ipc_items"

    id = Column(Integer, primary_key=True, index=True)
    ipc_id = Column(Integer, ForeignKey("ipcs.id"), nullable=False)
    boq_item_id = Column(Integer, ForeignKey("boq_items.id"), nullable=False)
    quantity_approval_id = Column(Integer, ForeignKey("quantity_approvals.id"), nullable=False)
    approved_qty = Column(Numeric(14, 4, asdecimal=True), nullable=False)
    contract_rate_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)
    amount_pkr = Column(Numeric(14, 2, asdecimal=True), nullable=False)

    # Relationships
    ipc = relationship("Ipc", back_populates="items")
    boq_item = relationship("BoqItem")
    quantity_approval = relationship("QuantityApproval", back_populates="ipc_items")
