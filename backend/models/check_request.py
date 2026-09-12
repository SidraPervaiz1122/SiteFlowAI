from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class CheckRequest(Base):
    __tablename__ = "check_requests"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    boq_item_id = Column(Integer, ForeignKey("boq_items.id"), nullable=False)
    cr_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. CR-001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    proposed_qty = Column(Numeric(14, 4, asdecimal=True), nullable=False)
    unit = Column(String(20), nullable=False)
    status = Column(String(50), default="DRAFT", index=True, nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    project = relationship("Project")
    boq_item = relationship("BoqItem", back_populates="check_requests")
    created_by = relationship("User", foreign_keys=[created_by_id])
    evidences = relationship("Evidence", back_populates="check_request", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="check_request", cascade="all, delete-orphan")
    ai_reviews = relationship("AiReview", back_populates="check_request", cascade="all, delete-orphan")
    quantity_measurements = relationship("QuantityMeasurement", back_populates="check_request")
