"""Context builder for escalation."""
from typing import Dict, Any


def build_escalation_context(
    ticket_id: str,
    router_result: Dict[str, Any],
    knowledge_result: Dict[str, Any],
    sentiment_result: Dict[str, Any],
    decision: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build comprehensive context for human agents.
    
    Args:
        ticket_id: Ticket ID
        router_result: Router agent results
        knowledge_result: Knowledge agent results
        sentiment_result: Sentiment agent results
        decision: Decision result
        
    Returns:
        Escalation context
    """
    context = {
        "ticket_id": ticket_id,
        "category": router_result.get("category"),
        "subcategory": router_result.get("subcategory"),
        "issue_summary": f"{router_result.get('category')} - {router_result.get('subcategory', 'N/A')}",
        "customer_sentiment": {
            "score": sentiment_result.get("score"),
            "level": sentiment_result.get("level"),
            "urgency": sentiment_result.get("urgency"),
            "churn_risk": sentiment_result.get("churn_risk")
        },
        "solution": {
            "found": knowledge_result.get("solution") is not None,
            "solution_text": knowledge_result.get("solution"),
            "confidence": knowledge_result.get("confidence"),
            "similar_cases_found": knowledge_result.get("similar_cases_found", 0),
            "top_match_case_id": knowledge_result.get("top_match_case_id")
        },
        "recommended_action": _get_recommended_action(
            decision.get("decision"),
            knowledge_result,
            sentiment_result
        ),
        "priority": decision.get("priority", "MEDIUM"),
        "sla_minutes": decision.get("sla_minutes", 60),
        "ai_confidence": decision.get("reasoning")
    }
    
    return context


def _get_recommended_action(
    decision: str,
    knowledge_result: Dict[str, Any],
    sentiment_result: Dict[str, Any]
) -> str:
    """Get recommended action for human agent."""
    if decision == "AUTO_RESOLVE":
        return knowledge_result.get("solution", "Auto-resolve with provided solution")
    
    if decision == "ESCALATE_TO_MANAGER":
        return "Call customer immediately. High churn risk. Offer retention incentives."
    
    # ESCALATE_TO_HUMAN
    solution = knowledge_result.get("solution")
    if solution:
        return f"Customer needs empathy. Suggested solution: {solution}. Call or chat within SLA."
    else:
        return "Customer needs human assistance. No automated solution found. Investigate and respond."



