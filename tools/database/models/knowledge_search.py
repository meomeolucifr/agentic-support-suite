"""Knowledge search model - Knowledge agent results."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from tools.database.postgres import Base
import uuid


class KnowledgeSearch(Base):
    """Knowledge search model - stores knowledge agent results."""
    __tablename__ = "knowledge_searches"

    search_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.ticket_id"), nullable=False, index=True)
    query = Column(Text, nullable=False)
    similar_cases_found = Column(Integer, default=0, nullable=False)
    top_match_case_id = Column(String(100), nullable=True)
    similarity_score = Column(Float, nullable=True)
    solution = Column(Text, nullable=True)
    solution_confidence = Column(Float, nullable=True)
    solvable_without_escalation = Column(Boolean, default=True, nullable=False)
    similar_cases_data = Column(JSONB, nullable=True)  # Store full similar cases data
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    ticket = relationship("Ticket", backref="knowledge_searches")

    def __repr__(self):
        return f"<KnowledgeSearch(ticket_id={self.ticket_id}, similar_cases={self.similar_cases_found}, confidence={self.solution_confidence})>"



