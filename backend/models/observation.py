from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), default="LOW", nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    category = Column(String(50), default="QUALITY", nullable=False) # QUALITY, SAFETY, SPECIFICATION, WORKMANSHIP, DOCUMENTATION
    corrective_action = Column(Text, nullable=True)
    is_ai_generated = Column(Boolean, default=False)
    accepted_by_re = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    inspection = relationship("Inspection", back_populates="observations")
