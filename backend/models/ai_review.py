from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class AiReview(Base):
    __tablename__ = "ai_reviews"

    id = Column(Integer, primary_key=True, index=True)
    check_request_id = Column(Integer, ForeignKey("check_requests.id"), nullable=False)
    readiness = Column(String(50), nullable=False) # Ready, Needs Attention, High Risk
    confidence_score = Column(Integer, nullable=False) # 0 to 100
    missing_evidence = Column(Text, nullable=True) # JSON array or bulleted text
    potential_issues = Column(Text, nullable=True) # JSON array or bulleted text
    suggested_checks = Column(Text, nullable=True) # JSON array or bulleted text
    recommended_questions = Column(Text, nullable=True) # JSON array or bulleted text
    raw_response = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    check_request = relationship("CheckRequest", back_populates="ai_reviews")

class AiObservation(Base):
    __tablename__ = "ai_observations"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), default="LOW", nullable=False)
    category = Column(String(50), default="QUALITY", nullable=False)
    recommended_action = Column(Text, nullable=True)
    is_applied = Column(Integer, default=0) # 1 if converted to actual observation by RE
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    inspection = relationship("Inspection", back_populates="ai_observations")
