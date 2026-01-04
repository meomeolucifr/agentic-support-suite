"""Similar case model - Historical cases for vector search."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from tools.database.postgres import Base
import uuid


class SimilarCase(Base):
    """Similar case model - stores historical resolved cases."""
    __tablename__ = "similar_cases"

    case_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id_original = Column(UUID(as_uuid=True), ForeignKey("tickets.ticket_id"), nullable=True)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True)
    issue_description = Column(Text, nullable=False)
    resolution = Column(Text, nullable=False)
    customer_satisfaction = Column(Integer, nullable=True)  # 1-10 scale
    vector_id = Column(String(200), nullable=True, index=True)  # ID in Chroma vector DB
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    original_ticket = relationship("Ticket", foreign_keys=[ticket_id_original], backref="similar_cases")

    def __repr__(self):
        return f"<SimilarCase(case_id={self.case_id}, category={self.category}, satisfaction={self.customer_satisfaction})>"



