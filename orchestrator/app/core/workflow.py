"""Workflow state machine."""
from enum import Enum
from typing import Optional
from tools.database.models.ticket import TicketStatus


class WorkflowState(str, Enum):
    """Workflow states."""
    NEW = "NEW"
    ROUTING = "ROUTING"
    KNOWLEDGE_SEARCH = "KNOWLEDGE_SEARCH"
    SENTIMENT_ANALYSIS = "SENTIMENT_ANALYSIS"
    DECISION = "DECISION"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"
    ERROR = "ERROR"


def get_next_state(current_state: WorkflowState) -> Optional[WorkflowState]:
    """Get next state in workflow."""
    state_flow = {
        WorkflowState.NEW: WorkflowState.ROUTING,
        WorkflowState.ROUTING: WorkflowState.KNOWLEDGE_SEARCH,
        WorkflowState.KNOWLEDGE_SEARCH: WorkflowState.SENTIMENT_ANALYSIS,
        WorkflowState.SENTIMENT_ANALYSIS: WorkflowState.DECISION,
        WorkflowState.DECISION: None,  # Terminal states
        WorkflowState.RESOLVED: None,
        WorkflowState.ESCALATED: None,
        WorkflowState.ERROR: None
    }
    return state_flow.get(current_state)


def map_to_ticket_status(workflow_state: WorkflowState) -> TicketStatus:
    """Map workflow state to ticket status."""
    mapping = {
        WorkflowState.NEW: TicketStatus.NEW,
        WorkflowState.ROUTING: TicketStatus.ROUTING,
        WorkflowState.KNOWLEDGE_SEARCH: TicketStatus.KNOWLEDGE_SEARCH,
        WorkflowState.SENTIMENT_ANALYSIS: TicketStatus.SENTIMENT_ANALYSIS,
        WorkflowState.DECISION: TicketStatus.DECISION,
        WorkflowState.RESOLVED: TicketStatus.RESOLVED,
        WorkflowState.ESCALATED: TicketStatus.ESCALATED,
        WorkflowState.ERROR: TicketStatus.NEW  # Default fallback
    }
    return mapping.get(workflow_state, TicketStatus.NEW)



