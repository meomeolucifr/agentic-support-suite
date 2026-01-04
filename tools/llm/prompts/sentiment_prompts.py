"""Prompt templates for Sentiment Agent."""


def get_sentiment_analysis_prompt(ticket_text: str) -> str:
    """
    Get sentiment analysis prompt.
    
    Args:
        ticket_text: Customer ticket text
        
    Returns:
        Formatted prompt
    """
    return f"""Analyze the sentiment and emotional state of this customer support ticket.

Ticket text:
{ticket_text}

Analyze:
1. Sentiment score (0.0 = very calm, 1.0 = extremely angry)
2. Emotional level (CALM, NEUTRAL, UPSET, ANGRY)
3. Urgency level (LOW, MEDIUM, HIGH)
4. Churn risk (is customer likely to leave?)
5. Does this require human empathy or can it be handled by bot?

Return a JSON object with:
- score: Sentiment score (0.0 to 1.0)
- level: Emotional level (CALM, NEUTRAL, UPSET, ANGRY)
- urgency: Urgency level (LOW, MEDIUM, HIGH)
- churn_risk: true if customer is at risk of leaving
- requires_human: true if human touch is needed
- recommended_handler: BOT, HUMAN, or MANAGER

Example response:
{{
    "score": 0.92,
    "level": "ANGRY",
    "urgency": "HIGH",
    "churn_risk": true,
    "requires_human": true,
    "recommended_handler": "HUMAN"
}}"""


def get_sentiment_schema() -> dict:
    """Get JSON schema for sentiment analysis response."""
    return {
        "type": "object",
        "properties": {
            "score": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0
            },
            "level": {
                "type": "string",
                "enum": ["CALM", "NEUTRAL", "UPSET", "ANGRY"]
            },
            "urgency": {
                "type": "string",
                "enum": ["LOW", "MEDIUM", "HIGH"]
            },
            "churn_risk": {
                "type": "boolean"
            },
            "requires_human": {
                "type": "boolean"
            },
            "recommended_handler": {
                "type": "string",
                "enum": ["BOT", "HUMAN", "MANAGER"]
            }
        },
        "required": ["score", "level", "churn_risk", "requires_human"]
    }



