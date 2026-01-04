"""Decision Engine Agent implementation."""
import time
from typing import Dict, Any
from app.models.decision import (
    DecisionRequest,
    DecisionResponse
)
from app.engine.decision_logic import make_decision
from app.engine.context_builder import build_escalation_context
from tools.database.postgres import get_db_session
from tools.database.models.decision import Decision as DecisionModel, DecisionType
from tools.database.models.ticket import Ticket
from tools.monitoring.metrics import get_metrics_collector


class DecisionEngineAgent:
    """Decision Engine Agent - makes final decisions."""
    
    def __init__(self):
        """Initialize Decision Agent."""
        self.metrics = get_metrics_collector()
    
    async def decide(self, request: DecisionRequest) -> DecisionResponse:
        """
        Make decision based on all agent results.
        
        Args:
            request: Decision request with all agent results
            
        Returns:
            Decision result
        """
        start_time = time.time()
        
        try:
            # Make decision
            decision_result = await make_decision(
                router_result=request.router_result,
                knowledge_result=request.knowledge_result,
                sentiment_result=request.sentiment_result
            )
            
            # Build context for escalation
            context = build_escalation_context(
                ticket_id=request.ticket_id,
                router_result=request.router_result,
                knowledge_result=request.knowledge_result,
                sentiment_result=request.sentiment_result,
                decision=decision_result
            )
            
            # Map decision string to enum
            decision_map = {
                "AUTO_RESOLVE": DecisionType.AUTO_RESOLVE,
                "ESCALATE_TO_HUMAN": DecisionType.ESCALATE_TO_HUMAN,
                "ESCALATE_TO_MANAGER": DecisionType.ESCALATE_TO_MANAGER
            }
            decision_type = decision_map.get(
                decision_result.get("decision", "ESCALATE_TO_HUMAN"),
                DecisionType.ESCALATE_TO_HUMAN
            )
            
            # Create response
            response = DecisionResponse(
                ticket_id=request.ticket_id,
                decision=decision_result.get("decision", "ESCALATE_TO_HUMAN"),
                confidence=decision_result.get("confidence", 0.0),
                reasoning=decision_result.get("reasoning"),
                context=context,
                priority=decision_result.get("priority"),
                sla_minutes=decision_result.get("sla_minutes")
            )
            
            # Save to database (non-blocking - continue even if DB is unavailable)
            try:
                await self._save_decision(request.ticket_id, response, decision_type, context)
            except Exception as db_error:
                # Log but don't fail the request if DB is unavailable
                import logging
                logging.warning(f"Failed to save decision to database: {db_error}")
            
            # Record metrics
            duration = time.time() - start_time
            self.metrics.record_agent_call("decision", True, duration)
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_agent_call("decision", False, duration)
            raise
    
    async def _save_decision(
        self,
        ticket_id: str,
        response: DecisionResponse,
        decision_type: DecisionType,
        context: Dict[str, Any]
    ):
        """Save decision to database."""
        async for session in get_db_session():
            # Get ticket UUID
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                return
            
            # Create decision record
            db_decision = DecisionModel(
                ticket_id=ticket.ticket_id,
                final_decision=decision_type,
                confidence=response.confidence,
                reasoning=response.reasoning,
                context=context,
                priority=response.priority,
                sla_minutes=response.sla_minutes,
                ai_confidence=response.reasoning
            )
            
            session.add(db_decision)
            await session.commit()
            break

