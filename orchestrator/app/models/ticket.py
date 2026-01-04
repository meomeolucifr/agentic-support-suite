"""Ticket models for Orchestrator."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TicketCreateRequest(BaseModel):
    """Request model for creating ticket."""
    customer_id: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class TicketResponse(BaseModel):
    """Response model for ticket."""
    ticket_id: str
    customer_id: str
    subject: str
    body: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime


class TicketProcessingResponse(BaseModel):
    """Response model for ticket processing."""
    ticket_id: str
    status: str
    decision: Optional[str] = None
    solution: Optional[str] = None
    escalated: bool = False
    message: str
    workflow: Optional[Dict[str, Any]] = None


