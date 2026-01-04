"""Ticket model."""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from tools.database.postgres import Base
import enum


class TicketStatus(str, enum.Enum):
    """Ticket status enumeration."""
    NEW = "NEW"
    ROUTING = "ROUTING"
    KNOWLEDGE_SEARCH = "KNOWLEDGE_SEARCH"
    SENTIMENT_ANALYSIS = "SENTIMENT_ANALYSIS"
    DECISION = "DECISION"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"
    CLOSED = "CLOSED"


class TicketPriority(str, enum.Enum):
    """Ticket priority enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class Ticket(Base):
    """Ticket model."""
    __tablename__ = "tickets"

    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(String(100), nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.NEW, nullable=False, index=True)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    assigned_to = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Ticket(ticket_id={self.ticket_id}, status={self.status}, priority={self.priority})>"



