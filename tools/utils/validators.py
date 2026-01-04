"""Input validation utilities."""
from typing import Any, Dict
from pydantic import BaseModel, ValidationError


def validate_ticket_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate ticket submission data.
    
    Args:
        data: Ticket data dictionary
        
    Returns:
        Validated data
        
    Raises:
        ValueError: If validation fails
    """
    required_fields = ["customer_id", "subject", "body"]
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if not isinstance(data["customer_id"], str) or not data["customer_id"].strip():
        raise ValueError("customer_id must be a non-empty string")
    
    if not isinstance(data["subject"], str) or not data["subject"].strip():
        raise ValueError("subject must be a non-empty string")
    
    if not isinstance(data["body"], str) or not data["body"].strip():
        raise ValueError("body must be a non-empty string")
    
    return data



