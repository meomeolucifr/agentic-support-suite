"""LLM-based sentiment analysis."""
from typing import Dict, Any
from tools.llm.providers.factory import get_llm_provider
from tools.llm.prompts.sentiment_prompts import get_sentiment_analysis_prompt, get_sentiment_schema


async def analyze_sentiment_llm(ticket_text: str) -> Dict[str, Any]:
    """
    Analyze sentiment using LLM.
    
    Args:
        ticket_text: Ticket text
        
    Returns:
        Sentiment analysis result
    """
    llm = get_llm_provider()
    prompt = get_sentiment_analysis_prompt(ticket_text)
    schema = get_sentiment_schema()
    
    result = await llm.generate_json(
        prompt=prompt,
        schema=schema,
        temperature=0.3
    )
    
    return result



