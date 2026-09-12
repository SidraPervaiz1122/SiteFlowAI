from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from backend.app.database import Base

class RagDocument(Base):
    __tablename__ = "rag_documents"

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String(50), nullable=False) # BOQ, ASSUMPTION, TAKEOFF, SITE_SPEC, AUDIT
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    keywords = Column(Text, nullable=True) # space/comma separated for hybrid search
    created_at = Column(DateTime(timezone=True), server_default=func.now())
