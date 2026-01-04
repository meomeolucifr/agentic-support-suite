"""API routes for Decision Agent."""
from fastapi import APIRouter, HTTPException
from app.models.decision import (
    DecisionRequest,
    DecisionResponse
)
from app.agent import DecisionEngineAgent

router = APIRouter()
agent = DecisionEngineAgent()


@router.post("/process", response_model=DecisionResponse)
async def process_decision(request: DecisionRequest) -> DecisionResponse:
    """
    Process decision.
    
    Args:
        request: Decision request
        
    Returns:
        Decision result
    """
    try:
        result = await agent.decide(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "decision"}

