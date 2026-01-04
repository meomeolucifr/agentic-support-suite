"""API routes for Knowledge Agent."""
from fastapi import APIRouter, HTTPException
from app.models.knowledge import (
    KnowledgeSearchRequest,
    KnowledgeSearchResponse
)
from app.agent import KnowledgeAgent

router = APIRouter()
agent = KnowledgeAgent()


@router.post("/process", response_model=KnowledgeSearchResponse)
async def process_search(request: KnowledgeSearchRequest) -> KnowledgeSearchResponse:
    """
    Process knowledge base search.
    
    Args:
        request: Knowledge search request
        
    Returns:
        Knowledge search result
    """
    try:
        result = await agent.search(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "knowledge"}

