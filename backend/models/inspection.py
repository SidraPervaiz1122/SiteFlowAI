from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    check_request_id = Column(Integer, ForeignKey("check_requests.id"), nullable=False)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    decision = Column(String(50), nullable=True) # ACCEPT, REJECT, CONDITIONAL
    inspector_notes = Column(Text, nullable=True)
    checklist_results = Column(Text, nullable=True) # JSON serialized checklist items
    inspected_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    check_request = relationship("CheckRequest", back_populates="inspections")
    inspector = relationship("User")
    observations = relationship("Observation", back_populates="inspection", cascade="all, delete-orphan")
    ai_observations = relationship("AiObservation", back_populates="inspection", cascade="all, delete-orphan")
    evidences = relationship("Evidence", back_populates="inspection")
