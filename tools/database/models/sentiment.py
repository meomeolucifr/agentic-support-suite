"""Sentiment model - Sentiment agent results."""
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from tools.database.postgres import Base
import uuid
import enum


class SentimentLevel(str, enum.Enum):
    """Sentiment level enumeration."""
    CALM = "CALM"
    NEUTRAL = "NEUTRAL"
    UPSET = "UPSET"
    ANGRY = "ANGRY"


class Sentiment(Base):
    """Sentiment model - stores sentiment agent results."""
    __tablename__ = "sentiment_analysis"

    sentiment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.ticket_id"), nullable=False, index=True)
    score = Column(Float, nullable=False)  # 0.0 to 1.0
    level = Column(Enum(SentimentLevel), nullable=False)
    urgency = Column(String(20), nullable=True)  # LOW, MEDIUM, HIGH
    churn_risk = Column(Boolean, default=False, nullable=False)
    requires_human = Column(Boolean, default=False, nullable=False)
    recommended_handler = Column(String(50), nullable=True)  # BOT, HUMAN, MANAGER
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    ticket = relationship("Ticket", backref="sentiment_analyses")

    def __repr__(self):
        return f"<Sentiment(ticket_id={self.ticket_id}, score={self.score}, level={self.level}, churn_risk={self.churn_risk})>"



