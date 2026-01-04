"""Sentiment Agent implementation."""
import time
import os
from typing import Dict, Any
from app.models.sentiment import (
    SentimentAnalysisRequest,
    SentimentAnalysisResponse
)
from app.analyzers.llm_sentiment import analyze_sentiment_llm
from app.analyzers.huggingface_sentiment import analyze_sentiment_hf
from tools.database.postgres import get_db_session
from tools.database.models.sentiment import Sentiment as SentimentModel, SentimentLevel
from tools.database.models.ticket import Ticket
from tools.monitoring.metrics import get_metrics_collector


class SentimentAnalyzerAgent:
    """Sentiment Analyzer Agent - analyzes customer sentiment."""
    
    def __init__(self):
        """Initialize Sentiment Agent."""
        self.use_hf = os.getenv("USE_HUGGINGFACE", "false").lower() == "true"
        self.metrics = get_metrics_collector()
    
    async def analyze(self, request: SentimentAnalysisRequest) -> SentimentAnalysisResponse:
        """
        Analyze sentiment of ticket.
        
        Args:
            request: Sentiment analysis request
            
        Returns:
            Sentiment analysis result
        """
        start_time = time.time()
        
        try:
            # Analyze sentiment
            if self.use_hf:
                result = await analyze_sentiment_hf(request.text)
            else:
                result = await analyze_sentiment_llm(request.text)
            
            # Map level string to enum
            level_map = {
                "CALM": SentimentLevel.CALM,
                "NEUTRAL": SentimentLevel.NEUTRAL,
                "UPSET": SentimentLevel.UPSET,
                "ANGRY": SentimentLevel.ANGRY
            }
            level = level_map.get(result.get("level", "NEUTRAL"), SentimentLevel.NEUTRAL)
            
            # Create response
            response = SentimentAnalysisResponse(
                ticket_id=request.ticket_id,
                score=result.get("score", 0.5),
                level=result.get("level", "NEUTRAL"),
                urgency=result.get("urgency"),
                churn_risk=result.get("churn_risk", False),
                requires_human=result.get("requires_human", False),
                recommended_handler=result.get("recommended_handler")
            )
            
            # Save to database (non-blocking - continue even if DB is unavailable)
            try:
                await self._save_sentiment(request.ticket_id, response, level)
            except Exception as db_error:
                # Log but don't fail the request if DB is unavailable
                import logging
                logging.warning(f"Failed to save sentiment to database: {db_error}")
            
            # Record metrics
            duration = time.time() - start_time
            self.metrics.record_agent_call("sentiment", True, duration)
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_agent_call("sentiment", False, duration)
            raise
    
    async def _save_sentiment(
        self,
        ticket_id: str,
        response: SentimentAnalysisResponse,
        level: SentimentLevel
    ):
        """Save sentiment analysis to database."""
        async for session in get_db_session():
            # Get ticket UUID
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                return
            
            # Create sentiment record
            db_sentiment = SentimentModel(
                ticket_id=ticket.ticket_id,
                score=response.score,
                level=level,
                urgency=response.urgency,
                churn_risk=response.churn_risk,
                requires_human=response.requires_human,
                recommended_handler=response.recommended_handler
            )
            
            session.add(db_sentiment)
            await session.commit()
            break

