"""Sentiment analysis models."""
from pydantic import BaseModel, Field
from typing import Optional


class SentimentAnalysisRequest(BaseModel):
    """Request model for sentiment analysis."""
    ticket_id: str
    text: str = Field(..., min_length=1)


class SentimentAnalysisResponse(BaseModel):
    """Response model for sentiment analysis."""
    ticket_id: str
    score: float = Field(..., ge=0.0, le=1.0)
    level: str  # CALM, NEUTRAL, UPSET, ANGRY
    urgency: Optional[str] = None
    churn_risk: bool = False
    requires_human: bool = False
    recommended_handler: Optional[str] = None  # BOT, HUMAN, MANAGER



