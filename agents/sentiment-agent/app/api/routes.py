"""API routes for Sentiment Agent."""
from fastapi import APIRouter, HTTPException
from app.models.sentiment import (
    SentimentAnalysisRequest,
    SentimentAnalysisResponse
)
from app.agent import SentimentAnalyzerAgent

router = APIRouter()
agent = SentimentAnalyzerAgent()


@router.post("/process", response_model=SentimentAnalysisResponse)
async def process_sentiment(request: SentimentAnalysisRequest) -> SentimentAnalysisResponse:
    """
    Process sentiment analysis.
    
    Args:
        request: Sentiment analysis request
        
    Returns:
        Sentiment analysis result
    """
    try:
        result = await agent.analyze(request)
        return result
    except Exception as e:
        import traceback
        error_detail = f"{type(e).__name__}: {str(e)}"
        import logging
        logging.error(f"Sentiment Agent error: {error_detail}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "sentiment"}

