"""Decision model - Decision engine results."""
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from tools.database.postgres import Base
import uuid
import enum


class DecisionType(str, enum.Enum):
    """Decision type enumeration."""
    AUTO_RESOLVE = "AUTO_RESOLVE"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    ESCALATE_TO_MANAGER = "ESCALATE_TO_MANAGER"


class Decision(Base):
    """Decision model - stores decision engine results."""
    __tablename__ = "decisions"

    decision_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.ticket_id"), nullable=False, index=True)
    final_decision = Column(Enum(DecisionType), nullable=False)
    confidence = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=True)
    context = Column(JSONB, nullable=True)  # Full context for human agents
    assigned_to = Column(String(100), nullable=True)
    priority = Column(String(20), nullable=True)  # LOW, MEDIUM, HIGH, URGENT
    sla_minutes = Column(Integer, nullable=True)  # SLA in minutes
    ai_confidence = Column(String(500), nullable=True)  # AI's confidence explanation
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    ticket = relationship("Ticket", backref="decisions")

    def __repr__(self):
        return f"<Decision(ticket_id={self.ticket_id}, decision={self.final_decision}, confidence={self.confidence})>"



