"""Prompt templates for Router Agent."""
from typing import List


CATEGORIES = [
    "BILLING",
    "TECHNICAL",
    "BUG",
    "FEATURE_REQUEST",
    "ACCOUNT",
    "SHIPPING",
    "SPAM",
    "OTHER"
]


def get_classification_prompt(ticket_text: str) -> str:
    """
    Get classification prompt for router agent.
    
    Args:
        ticket_text: Customer ticket text
        
    Returns:
        Formatted prompt
    """
    return f"""Classify this support ticket into ONE category.

Ticket text:
{ticket_text}

Categories:
{', '.join(CATEGORIES)}

Return a JSON object with:
- category: The category (one of the categories above)
- subcategory: A more specific subcategory (e.g., "DUPLICATE_CHARGE" for BILLING)
- confidence: A confidence score between 0.0 and 1.0
- reason: A brief explanation of why this category was chosen

Example response:
{{
    "category": "BILLING",
    "subcategory": "DUPLICATE_CHARGE",
    "confidence": 0.98,
    "reason": "Customer states charged twice, requests refund"
}}"""


def get_classification_schema() -> dict:
    """Get JSON schema for classification response."""
    return {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": CATEGORIES
            },
            "subcategory": {
                "type": "string"
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0
            },
            "reason": {
                "type": "string"
            }
        },
        "required": ["category", "confidence"]
    }



