"""Knowledge search models."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class KnowledgeSearchRequest(BaseModel):
    """Request model for knowledge search."""
    ticket_id: str
    text: str = Field(..., min_length=1)
    category: Optional[str] = None


class SimilarCase(BaseModel):
    """Similar case model."""
    id: str
    text: str
    metadata: Dict[str, Any]
    similarity: float


class KnowledgeSearchResponse(BaseModel):
    """Response model for knowledge search."""
    ticket_id: str
    similar_cases_found: int
    top_match_case_id: Optional[str] = None
    similarity_score: Optional[float] = None
    solution: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    solvable_without_escalation: bool = True
    similar_cases: Optional[List[SimilarCase]] = None



