"""Decision logic engine."""
from typing import Dict, Any
from tools.llm.providers.factory import get_llm_provider
from tools.llm.prompts.decision_prompts import get_decision_prompt, get_decision_schema


async def make_decision(
    router_result: Dict[str, Any],
    knowledge_result: Dict[str, Any],
    sentiment_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Make decision based on all agent results.
    
    Args:
        router_result: Router agent results
        knowledge_result: Knowledge agent results
        sentiment_result: Sentiment agent results
        
    Returns:
        Decision result
    """
    # Hard rules first
    sentiment_score = sentiment_result.get("score", 0.0)
    churn_risk = sentiment_result.get("churn_risk", False)
    category = router_result.get("category", "")
    
    # Hard rule: High sentiment -> escalate
    if sentiment_score >= 0.85:
        return {
            "decision": "ESCALATE_TO_HUMAN",
            "confidence": 0.95,
            "reasoning": f"Sentiment score {sentiment_score:.2f} exceeds threshold (0.85). Customer needs human empathy.",
            "priority": "HIGH",
            "sla_minutes": 5
        }
    
    # Hard rule: Churn risk -> escalate to manager
    if churn_risk:
        return {
            "decision": "ESCALATE_TO_MANAGER",
            "confidence": 0.90,
            "reasoning": "Customer at risk of churn. Requires manager attention.",
            "priority": "URGENT",
            "sla_minutes": 2
        }
    
    # Hard rule: Bug -> escalate (needs engineering)
    if category == "BUG":
        return {
            "decision": "ESCALATE_TO_HUMAN",
            "confidence": 0.85,
            "reasoning": "Bug reports require engineering team review.",
            "priority": "HIGH",
            "sla_minutes": 15
        }
    
    # Use LLM for nuanced decisions
    llm = get_llm_provider()
    prompt = get_decision_prompt(router_result, knowledge_result, sentiment_result)
    schema = get_decision_schema()
    
    result = await llm.generate_json(
        prompt=prompt,
        schema=schema,
        temperature=0.2  # Very low temperature for consistent decisions
    )
    
    return result



