"""Decision models."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class DecisionRequest(BaseModel):
    """Request model for decision."""
    ticket_id: str
    router_result: Dict[str, Any]
    knowledge_result: Dict[str, Any]
    sentiment_result: Dict[str, Any]


class DecisionResponse(BaseModel):
    """Response model for decision."""
    ticket_id: str
    decision: str  # AUTO_RESOLVE, ESCALATE_TO_HUMAN, ESCALATE_TO_MANAGER
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    priority: Optional[str] = None
    sla_minutes: Optional[int] = None



