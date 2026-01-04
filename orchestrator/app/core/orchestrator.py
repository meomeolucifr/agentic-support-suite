"""Main orchestrator logic."""
import os
import time
from typing import Dict, Any, Optional
import httpx
from tools.database.postgres import get_db_session
from tools.database.models.ticket import Ticket, TicketStatus, TicketPriority
from tools.database.models.decision import DecisionType
from orchestrator.app.core.workflow import WorkflowState, map_to_ticket_status
from orchestrator.app.core.error_handler import retry_with_backoff
from tools.integrations.slack.client import SlackClient
from tools.integrations.email.client import EmailClient
from tools.monitoring.metrics import get_metrics_collector
from tools.monitoring.logger import get_logger

logger = get_logger(__name__)


class Orchestrator:
    """Main orchestrator for ticket processing."""
    
    def __init__(self):
        """Initialize orchestrator."""
        self.router_url = os.getenv("ROUTER_AGENT_URL", "http://localhost:8001")
        self.knowledge_url = os.getenv("KNOWLEDGE_AGENT_URL", "http://localhost:8002")
        self.sentiment_url = os.getenv("SENTIMENT_AGENT_URL", "http://localhost:8003")
        self.decision_url = os.getenv("DECISION_AGENT_URL", "http://localhost:8004")
        self.metrics = get_metrics_collector()
        
        # Initialize integrations (optional, won't fail if not configured)
        try:
            self.slack_client = SlackClient()
        except Exception:
            self.slack_client = None
            logger.warning("Slack client not configured")
        
        try:
            self.email_client = EmailClient()
        except Exception:
            self.email_client = None
            logger.warning("Email client not configured")
    
    async def process_ticket(
        self,
        customer_id: str,
        subject: str,
        body: str
    ) -> Dict[str, Any]:
        """
        Process a ticket through the full workflow.
        
        Args:
            customer_id: Customer ID
            subject: Ticket subject
            body: Ticket body
            
        Returns:
            Processing result
        """
        start_time = time.time()
        ticket_id = None
        
        try:
            # Create ticket in database (non-blocking - continue even if DB is unavailable)
            try:
                ticket_id = await self._create_ticket(customer_id, subject, body)
            except Exception as db_error:
                # Generate a temporary ticket ID if database is unavailable
                import uuid
                ticket_id = f"TEMP_{uuid.uuid4().hex[:8].upper()}"
                logger.warning(f"Database unavailable, using temporary ticket ID: {ticket_id}", error=str(db_error))
            
            # Step 1: Router Agent
            logger.info("Starting router agent", ticket_id=ticket_id)
            router_result = await retry_with_backoff(
                self._call_router_agent,
                ticket_id=ticket_id,
                ticket_text=f"{subject}\n\n{body}"
            )
            # Update ticket status (non-blocking)
            try:
                await self._update_ticket_status(ticket_id, TicketStatus.ROUTING)
            except Exception:
                pass  # Ignore DB errors for status updates
            
            # Step 2: Knowledge Agent
            logger.info("Starting knowledge agent", ticket_id=ticket_id)
            knowledge_result = await retry_with_backoff(
                self._call_knowledge_agent,
                ticket_id=ticket_id,
                ticket_text=f"{subject}\n\n{body}",
                category=router_result.get("category")
            )
            try:
                await self._update_ticket_status(ticket_id, TicketStatus.KNOWLEDGE_SEARCH)
            except Exception:
                pass
            
            # Step 3: Sentiment Agent
            logger.info("Starting sentiment agent", ticket_id=ticket_id)
            sentiment_result = await retry_with_backoff(
                self._call_sentiment_agent,
                ticket_id=ticket_id,
                ticket_text=f"{subject}\n\n{body}"
            )
            try:
                await self._update_ticket_status(ticket_id, TicketStatus.SENTIMENT_ANALYSIS)
            except Exception:
                pass
            
            # Step 4: Decision Agent
            logger.info("Starting decision agent", ticket_id=ticket_id)
            decision_result = await retry_with_backoff(
                self._call_decision_agent,
                ticket_id=ticket_id,
                router_result=router_result,
                knowledge_result=knowledge_result,
                sentiment_result=sentiment_result
            )
            try:
                await self._update_ticket_status(ticket_id, TicketStatus.DECISION)
            except Exception:
                pass
            
            # Step 5: Execute decision
            decision = decision_result.get("decision", "ESCALATE_TO_HUMAN")
            if decision == "AUTO_RESOLVE":
                await self._handle_auto_resolve(ticket_id, decision_result, knowledge_result)
            else:
                await self._handle_escalation(ticket_id, decision_result, decision)
            
            # Record metrics
            duration = time.time() - start_time
            self.metrics.record_ticket_processing_time(str(ticket_id), duration)
            
            return {
                "ticket_id": str(ticket_id),
                "status": "completed",
                "decision": decision,
                "solution": knowledge_result.get("solution") if decision == "AUTO_RESOLVE" else None,
                "escalated": decision != "AUTO_RESOLVE",
                "message": "Ticket processed successfully",
                # Include full agent results for workflow visualization
                "workflow": {
                    "router": {
                        "category": router_result.get("category", "OTHER"),
                        "subcategory": router_result.get("subcategory") or "",
                        "confidence": float(router_result.get("confidence", 0.0)),
                        "reason": router_result.get("reason") or ""
                    },
                    "knowledge": {
                        "similar_cases_found": int(knowledge_result.get("similar_cases_found", 0)),
                        "top_match_case_id": knowledge_result.get("top_match_case_id") or "",
                        "similarity_score": float(knowledge_result.get("similarity_score", 0.0)) if knowledge_result.get("similarity_score") is not None else None,
                        "solution": knowledge_result.get("solution") or "",
                        "confidence": float(knowledge_result.get("confidence", 0.0)) if knowledge_result.get("confidence") is not None else None,
                        "solvable_without_escalation": bool(knowledge_result.get("solvable_without_escalation", False))
                    },
                    "sentiment": {
                        "score": float(sentiment_result.get("score", 0.5)),
                        "level": sentiment_result.get("level", "NEUTRAL"),
                        "urgency": sentiment_result.get("urgency") or "MEDIUM",
                        "churn_risk": bool(sentiment_result.get("churn_risk", False)),
                        "requires_human": bool(sentiment_result.get("requires_human", False)),
                        "recommended_handler": sentiment_result.get("recommended_handler") or ""
                    },
                    "decision": {
                        "decision": decision_result.get("decision", "ESCALATE_TO_HUMAN"),
                        "confidence": float(decision_result.get("confidence", 0.0)),
                        "reasoning": decision_result.get("reasoning") or "",
                        "priority": decision_result.get("priority") or "MEDIUM",
                        "sla_minutes": int(decision_result.get("sla_minutes", 0)) if decision_result.get("sla_minutes") else None
                    }
                }
            }
            
        except Exception as e:
            logger.error("Ticket processing failed", ticket_id=ticket_id, error=str(e))
            if ticket_id:
                try:
                    await self._update_ticket_status(ticket_id, TicketStatus.NEW)  # Reset on error
                except Exception:
                    pass  # Ignore DB errors
            raise
    
    async def _create_ticket(self, customer_id: str, subject: str, body: str) -> str:
        """Create ticket in database."""
        async for session in get_db_session():
            ticket = Ticket(
                customer_id=customer_id,
                subject=subject,
                body=body,
                status=TicketStatus.NEW,
                priority=TicketPriority.MEDIUM
            )
            session.add(ticket)
            await session.commit()
            await session.refresh(ticket)
            return str(ticket.ticket_id)
    
    async def _update_ticket_status(self, ticket_id: str, status: TicketStatus):
        """Update ticket status."""
        async for session in get_db_session():
            ticket = await session.get(Ticket, ticket_id)
            if ticket:
                ticket.status = status
                await session.commit()
            break
    
    async def _call_router_agent(self, ticket_id: str, ticket_text: str) -> Dict[str, Any]:
        """Call router agent."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.router_url}/api/process",
                json={"ticket_id": ticket_id, "text": ticket_text}
            )
            response.raise_for_status()
            data = response.json()
            # Ensure all fields are present
            return {
                "category": data.get("category", "OTHER"),
                "subcategory": data.get("subcategory"),
                "confidence": data.get("confidence", 0.0),
                "reason": data.get("reason")
            }
    
    async def _call_knowledge_agent(
        self,
        ticket_id: str,
        ticket_text: str,
        category: str = None
    ) -> Dict[str, Any]:
        """Call knowledge agent."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {"ticket_id": ticket_id, "text": ticket_text}
            if category:
                payload["category"] = category
            
            response = await client.post(
                f"{self.knowledge_url}/api/process",
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            # Ensure all fields are present
            return {
                "similar_cases_found": data.get("similar_cases_found", 0),
                "top_match_case_id": data.get("top_match_case_id"),
                "similarity_score": data.get("similarity_score"),
                "solution": data.get("solution"),
                "confidence": data.get("confidence"),
                "solvable_without_escalation": data.get("solvable_without_escalation", False)
            }
    
    async def _call_sentiment_agent(self, ticket_id: str, ticket_text: str) -> Dict[str, Any]:
        """Call sentiment agent."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.sentiment_url}/api/process",
                json={"ticket_id": ticket_id, "text": ticket_text}
            )
            response.raise_for_status()
            data = response.json()
            # Ensure all fields are present
            return {
                "score": data.get("score", 0.5),
                "level": data.get("level", "NEUTRAL"),
                "urgency": data.get("urgency"),
                "churn_risk": data.get("churn_risk", False),
                "requires_human": data.get("requires_human", False),
                "recommended_handler": data.get("recommended_handler")
            }
    
    async def _call_decision_agent(
        self,
        ticket_id: str,
        router_result: Dict[str, Any],
        knowledge_result: Dict[str, Any],
        sentiment_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call decision agent."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.decision_url}/api/process",
                json={
                    "ticket_id": ticket_id,
                    "router_result": router_result,
                    "knowledge_result": knowledge_result,
                    "sentiment_result": sentiment_result
                }
            )
            response.raise_for_status()
            data = response.json()
            # Ensure all fields are present
            return {
                "decision": data.get("decision", "ESCALATE_TO_HUMAN"),
                "confidence": data.get("confidence", 0.0),
                "reasoning": data.get("reasoning"),
                "priority": data.get("priority"),
                "sla_minutes": data.get("sla_minutes")
            }
    
    async def _handle_auto_resolve(
        self,
        ticket_id: str,
        decision_result: Dict[str, Any],
        knowledge_result: Dict[str, Any]
    ):
        """Handle auto-resolve decision."""
        await self._update_ticket_status(ticket_id, TicketStatus.RESOLVED)
        
        # Send solution to customer (via email if configured)
        solution = knowledge_result.get("solution", "Your issue has been resolved.")
        if self.email_client:
            # Note: Would need customer email from ticket
            # await self.email_client.send_ticket_response(...)
            pass
        
        logger.info("Ticket auto-resolved", ticket_id=ticket_id, solution=solution)
    
    async def _handle_escalation(
        self,
        ticket_id: str,
        decision_result: Dict[str, Any],
        decision: str
    ):
        """Handle escalation."""
        await self._update_ticket_status(ticket_id, TicketStatus.ESCALATED)
        
        # Send notification to support team
        context = decision_result.get("context", {})
        priority = decision_result.get("priority", "MEDIUM")
        
        if self.slack_client:
            await self.slack_client.send_ticket_escalation(
                ticket_id=ticket_id,
                priority=priority,
                context=context
            )
        
        logger.info("Ticket escalated", ticket_id=ticket_id, decision=decision, priority=priority)


