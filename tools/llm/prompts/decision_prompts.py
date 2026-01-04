"""Prompt templates for Decision Engine."""


def get_decision_prompt(
    router_result: dict,
    knowledge_result: dict,
    sentiment_result: dict
) -> str:
    """
    Get decision-making prompt.
    
    Args:
        router_result: Router agent results
        knowledge_result: Knowledge agent results
        sentiment_result: Sentiment agent results
        
    Returns:
        Formatted prompt
    """
    return f"""You are a decision engine for a customer support system. Analyze all the signals and make a final decision.

Router Agent Results:
- Category: {router_result.get('category', 'N/A')}
- Confidence: {router_result.get('confidence', 0)}

Knowledge Agent Results:
- Solution Found: {knowledge_result.get('solution', 'N/A')}
- Solution Confidence: {knowledge_result.get('confidence', 0)}
- Solvable Without Escalation: {knowledge_result.get('solvable_without_escalation', False)}

Sentiment Agent Results:
- Sentiment Score: {sentiment_result.get('score', 0)}
- Level: {sentiment_result.get('level', 'N/A')}
- Churn Risk: {sentiment_result.get('churn_risk', False)}
- Requires Human: {sentiment_result.get('requires_human', False)}

Decision Rules:
1. If sentiment >= 0.85 → ESCALATE_TO_HUMAN (override everything)
2. If churn_risk = true → ESCALATE_TO_HUMAN or ESCALATE_TO_MANAGER
3. If category = BUG → ESCALATE_TO_HUMAN (needs engineering)
4. If solution_confidence >= 0.85 AND sentiment < 0.7 → AUTO_RESOLVE
5. If solution_confidence >= 0.7 AND sentiment < 0.5 → AUTO_RESOLVE
6. Otherwise → ESCALATE_TO_HUMAN with context

Make a decision and provide reasoning.

Return a JSON object with:
- decision: AUTO_RESOLVE, ESCALATE_TO_HUMAN, or ESCALATE_TO_MANAGER
- confidence: Confidence in decision (0.0 to 1.0)
- reasoning: Explanation of decision
- priority: LOW, MEDIUM, HIGH, or URGENT
- sla_minutes: SLA in minutes (5 for high priority, 15 for medium, 60 for low)

Example response:
{{
    "decision": "ESCALATE_TO_HUMAN",
    "confidence": 0.92,
    "reasoning": "Sentiment too high (0.92) despite having solution. Customer needs human empathy.",
    "priority": "HIGH",
    "sla_minutes": 5
}}"""


def get_decision_schema() -> dict:
    """Get JSON schema for decision response."""
    return {
        "type": "object",
        "properties": {
            "decision": {
                "type": "string",
                "enum": ["AUTO_RESOLVE", "ESCALATE_TO_HUMAN", "ESCALATE_TO_MANAGER"]
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0
            },
            "reasoning": {
                "type": "string"
            },
            "priority": {
                "type": "string",
                "enum": ["LOW", "MEDIUM", "HIGH", "URGENT"]
            },
            "sla_minutes": {
                "type": "integer"
            }
        },
        "required": ["decision", "confidence", "reasoning"]
    }



