from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class ClientReview(Base):
    __tablename__ = "client_reviews"

    id = Column(Integer, primary_key=True, index=True)
    quantity_approval_id = Column(Integer, ForeignKey("quantity_approvals.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    decision = Column(String(50), nullable=False) # APPROVED, REJECTED
    comments = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    quantity_approval = relationship("QuantityApproval", back_populates="client_reviews")
    client = relationship("User")
