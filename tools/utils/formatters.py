"""Response formatting utilities."""
from typing import Dict, Any, List
from datetime import datetime


def format_ticket_response(ticket_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format ticket data for API response."""
    return {
        "ticket_id": str(ticket_data.get("ticket_id")),
        "customer_id": ticket_data.get("customer_id"),
        "subject": ticket_data.get("subject"),
        "body": ticket_data.get("body"),
        "status": ticket_data.get("status"),
        "priority": ticket_data.get("priority"),
        "created_at": ticket_data.get("created_at").isoformat() if ticket_data.get("created_at") else None,
        "updated_at": ticket_data.get("updated_at").isoformat() if ticket_data.get("updated_at") else None,
    }


def format_agent_response(agent_name: str, result: Dict[str, Any], duration: float) -> Dict[str, Any]:
    """Format agent response."""
    return {
        "agent": agent_name,
        "result": result,
        "duration_seconds": duration,
        "timestamp": datetime.utcnow().isoformat()
    }



