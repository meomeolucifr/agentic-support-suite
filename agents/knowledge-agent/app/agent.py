"""Knowledge Agent implementation."""
import time
from typing import Dict, Any
from app.models.knowledge import (
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    SimilarCase
)
from app.search.semantic_search import find_solution
from tools.database.postgres import get_db_session
from tools.database.models.knowledge_search import KnowledgeSearch as KnowledgeSearchModel
from tools.database.models.ticket import Ticket
from tools.monitoring.metrics import get_metrics_collector


class KnowledgeAgent:
    """Knowledge Agent - searches knowledge base for solutions."""
    
    def __init__(self):
        """Initialize Knowledge Agent."""
        self.metrics = get_metrics_collector()
    
    async def search(self, request: KnowledgeSearchRequest) -> KnowledgeSearchResponse:
        """
        Search knowledge base for solution.
        
        Args:
            request: Knowledge search request
            
        Returns:
            Knowledge search result
        """
        start_time = time.time()
        
        try:
            # Find solution
            result = await find_solution(
                ticket_text=request.text,
                category=request.category,
                top_k=5
            )
            
            # Format similar cases
            similar_cases = None
            if result.get("similar_cases"):
                similar_cases = [
                    SimilarCase(
                        id=case.get("id", ""),
                        text=case.get("text", ""),
                        metadata=case.get("metadata", {}),
                        similarity=case.get("similarity", 0.0)
                    )
                    for case in result["similar_cases"]
                ]
            
            # Create response
            response = KnowledgeSearchResponse(
                ticket_id=request.ticket_id,
                similar_cases_found=result.get("similar_cases_found", 0),
                top_match_case_id=result.get("top_match_case_id"),
                similarity_score=result.get("similarity_score"),
                solution=result.get("solution"),
                confidence=result.get("confidence"),
                solvable_without_escalation=result.get("solvable_without_escalation", False),
                similar_cases=similar_cases
            )
            
            # Save to database (non-blocking - continue even if DB is unavailable)
            try:
                await self._save_search(request.ticket_id, response, result)
            except Exception as db_error:
                # Log but don't fail the request if DB is unavailable
                import logging
                logging.warning(f"Failed to save knowledge search to database: {db_error}")
            
            # Record metrics
            duration = time.time() - start_time
            self.metrics.record_agent_call("knowledge", True, duration)
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_agent_call("knowledge", False, duration)
            raise
    
    async def _save_search(
        self,
        ticket_id: str,
        response: KnowledgeSearchResponse,
        raw_result: Dict[str, Any]
    ):
        """Save knowledge search to database."""
        async for session in get_db_session():
            # Get ticket UUID
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                return
            
            # Create knowledge search record
            db_search = KnowledgeSearchModel(
                ticket_id=ticket.ticket_id,
                query=response.ticket_id,  # Using ticket_id as query identifier
                similar_cases_found=response.similar_cases_found,
                top_match_case_id=response.top_match_case_id,
                similarity_score=response.similarity_score,
                solution=response.solution,
                solution_confidence=response.confidence,
                solvable_without_escalation=response.solvable_without_escalation,
                similar_cases_data=raw_result.get("similar_cases")
            )
            
            session.add(db_search)
            await session.commit()
            break

