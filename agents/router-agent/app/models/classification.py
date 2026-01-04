"""Classification models for Router Agent."""
from pydantic import BaseModel, Field
from typing import Optional


class ClassificationRequest(BaseModel):
    """Request model for classification."""
    ticket_id: str
    text: str = Field(..., min_length=1, description="Ticket text to classify")


class ClassificationResponse(BaseModel):
    """Response model for classification."""
    ticket_id: str
    category: str
    subcategory: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: Optional[str] = None



