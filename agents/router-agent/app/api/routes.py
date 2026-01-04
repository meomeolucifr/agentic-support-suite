"""API routes for Router Agent."""
from fastapi import APIRouter, HTTPException
from app.models.classification import (
    ClassificationRequest,
    ClassificationResponse
)
from app.agent import RouterAgent

router = APIRouter()
agent = RouterAgent()


@router.post("/process", response_model=ClassificationResponse)
async def process_ticket(request: ClassificationRequest) -> ClassificationResponse:
    """
    Process ticket classification.
    
    Args:
        request: Classification request
        
    Returns:
        Classification result
    """
    try:
        result = await agent.classify(
            ticket_id=request.ticket_id,
            ticket_text=request.text
        )
        return result
    except Exception as e:
        import traceback
        error_detail = f"{type(e).__name__}: {str(e)}"
        import logging
        logging.error(f"Router Agent error: {error_detail}\n{traceback.format_exc()}")
        # Return more detailed error in response
        raise HTTPException(
            status_code=500, 
            detail=f"Router Agent failed: {error_detail}. Check logs for full traceback."
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "router"}

