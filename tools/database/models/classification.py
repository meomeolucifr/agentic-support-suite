"""Classification model - Router agent results."""
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from tools.database.postgres import Base
import uuid


class Classification(Base):
    """Classification model - stores router agent results."""
    __tablename__ = "classifications"

    classification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.ticket_id"), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=False)
    reason = Column(String(1000), nullable=True)
    agent_version = Column(String(50), default="1.0.0", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    ticket = relationship("Ticket", backref="classifications")

    def __repr__(self):
        return f"<Classification(ticket_id={self.ticket_id}, category={self.category}, confidence={self.confidence})>"



