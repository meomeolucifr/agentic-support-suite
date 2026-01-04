"""API routes for Orchestrator."""
from fastapi import APIRouter, HTTPException
from typing import List
from orchestrator.app.models.ticket import (
    TicketCreateRequest,
    TicketProcessingResponse
)
from orchestrator.app.core.orchestrator import Orchestrator
from tools.database.postgres import get_db_session
from tools.database.models.ticket import Ticket
from tools.database.models.classification import Classification
from tools.database.models.knowledge_search import KnowledgeSearch
from tools.database.models.sentiment import Sentiment
from tools.database.models.decision import Decision

router = APIRouter()
orchestrator = Orchestrator()


@router.get("/tickets", response_model=List[dict])
async def list_tickets():
    """
    List all tickets.
    
    Returns:
        List of tickets
    """
    try:
        tickets = []
        async for session in get_db_session():
            from sqlalchemy import select
            result = await session.execute(select(Ticket).order_by(Ticket.created_at.desc()).limit(100))
            db_tickets = result.scalars().all()
            
            for ticket in db_tickets:
                tickets.append({
                    "ticket_id": str(ticket.ticket_id),
                    "customer_id": ticket.customer_id,
                    "subject": ticket.subject,
                    "body": ticket.body,
                    "status": ticket.status.value if hasattr(ticket.status, 'value') else str(ticket.status),
                    "priority": ticket.priority.value if hasattr(ticket.priority, 'value') else str(ticket.priority),
                    "created_at": ticket.created_at.isoformat() if hasattr(ticket.created_at, 'isoformat') else str(ticket.created_at),
                    "updated_at": ticket.updated_at.isoformat() if hasattr(ticket.updated_at, 'isoformat') else str(ticket.updated_at) if ticket.updated_at else None,
                })
            break
        return tickets
    except Exception as e:
        # If database is unavailable, return empty list
        import logging
        logging.warning(f"Database unavailable for listing tickets: {e}")
        return []


@router.get("/tickets/{ticket_id}", response_model=dict)
async def get_ticket(ticket_id: str):
    """
    Get ticket by ID with full workflow data.
    
    Args:
        ticket_id: Ticket ID
        
    Returns:
        Ticket details with workflow
    """
    try:
        async for session in get_db_session():
            from sqlalchemy import select
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")
            
            # Get classification (router result)
            classification_result = await session.execute(
                select(Classification).where(Classification.ticket_id == ticket.ticket_id).order_by(Classification.created_at.desc()).limit(1)
            )
            classification = classification_result.scalar_one_or_none()
            
            # Get knowledge search result
            knowledge_result = await session.execute(
                select(KnowledgeSearch).where(KnowledgeSearch.ticket_id == ticket.ticket_id).order_by(KnowledgeSearch.created_at.desc()).limit(1)
            )
            knowledge = knowledge_result.scalar_one_or_none()
            
            # Get sentiment result
            sentiment_result = await session.execute(
                select(Sentiment).where(Sentiment.ticket_id == ticket.ticket_id).order_by(Sentiment.created_at.desc()).limit(1)
            )
            sentiment = sentiment_result.scalar_one_or_none()
            
            # Get decision result
            decision_result = await session.execute(
                select(Decision).where(Decision.ticket_id == ticket.ticket_id).order_by(Decision.created_at.desc()).limit(1)
            )
            decision = decision_result.scalar_one_or_none()
            
            # Build workflow data
            workflow = {}
            if classification:
                workflow["router"] = {
                    "category": classification.category,
                    "subcategory": classification.subcategory,
                    "confidence": classification.confidence,
                    "reason": classification.reason,
                    "created_at": classification.created_at.isoformat() if hasattr(classification.created_at, 'isoformat') else str(classification.created_at)
                }
            
            if knowledge:
                workflow["knowledge"] = {
                    "similar_cases_found": knowledge.similar_cases_found,
                    "top_match_case_id": knowledge.top_match_case_id,
                    "similarity_score": knowledge.similarity_score,
                    "solution": knowledge.solution,
                    "confidence": knowledge.solution_confidence,
                    "solvable_without_escalation": knowledge.solvable_without_escalation,
                    "created_at": knowledge.created_at.isoformat() if hasattr(knowledge.created_at, 'isoformat') else str(knowledge.created_at)
                }
            
            if sentiment:
                workflow["sentiment"] = {
                    "score": sentiment.score,
                    "level": sentiment.level.value if hasattr(sentiment.level, 'value') else str(sentiment.level),
                    "urgency": sentiment.urgency,
                    "churn_risk": sentiment.churn_risk,
                    "requires_human": sentiment.requires_human,
                    "recommended_handler": sentiment.recommended_handler,
                    "created_at": sentiment.created_at.isoformat() if hasattr(sentiment.created_at, 'isoformat') else str(sentiment.created_at)
                }
            
            if decision:
                workflow["decision"] = {
                    "decision": decision.final_decision.value if hasattr(decision.final_decision, 'value') else str(decision.final_decision),
                    "confidence": decision.confidence,
                    "reasoning": decision.reasoning,
                    "priority": decision.priority,
                    "sla_minutes": decision.sla_minutes,
                    "created_at": decision.created_at.isoformat() if hasattr(decision.created_at, 'isoformat') else str(decision.created_at)
                }
            
            return {
                "ticket_id": str(ticket.ticket_id),
                "customer_id": ticket.customer_id,
                "subject": ticket.subject,
                "body": ticket.body,
                "status": ticket.status.value if hasattr(ticket.status, 'value') else str(ticket.status),
                "priority": ticket.priority.value if hasattr(ticket.priority, 'value') else str(ticket.priority),
                "created_at": ticket.created_at.isoformat() if hasattr(ticket.created_at, 'isoformat') else str(ticket.created_at),
                "updated_at": ticket.updated_at.isoformat() if hasattr(ticket.updated_at, 'isoformat') else str(ticket.updated_at) if ticket.updated_at else None,
                "workflow": workflow,
                "decision": workflow.get("decision", {}).get("decision") if workflow.get("decision") else None,
                "solution": workflow.get("knowledge", {}).get("solution") if workflow.get("knowledge") else None,
            }
            break
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.warning(f"Database unavailable for getting ticket: {e}")
        raise HTTPException(status_code=404, detail="Ticket not found")


@router.post("/tickets", response_model=TicketProcessingResponse)
async def create_ticket(request: TicketCreateRequest) -> TicketProcessingResponse:
    """
    Create and process a ticket.
    
    Args:
        request: Ticket creation request
        
    Returns:
        Ticket processing result
    """
    try:
        result = await orchestrator.process_ticket(
            customer_id=request.customer_id,
            subject=request.subject,
            body=request.body
        )
        
        # Ensure workflow is serializable
        workflow_data = result.get("workflow", {})
        if workflow_data:
            # Convert any non-serializable values
            import json
            try:
                json.dumps(workflow_data)  # Test if serializable
            except (TypeError, ValueError):
                # Convert to serializable format
                workflow_data = json.loads(json.dumps(workflow_data, default=str))
        
        return TicketProcessingResponse(
            ticket_id=result["ticket_id"],
            status=result["status"],
            decision=result.get("decision"),
            solution=result.get("solution"),
            escalated=result.get("escalated", False),
            message=result.get("message", "Ticket processed"),
            workflow=workflow_data
        )
    except Exception as e:
        import traceback
        import logging
        error_detail = f"{type(e).__name__}: {str(e)}"
        logging.error(f"Error creating ticket: {error_detail}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "orchestrator"}

