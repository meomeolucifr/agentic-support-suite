"""JSON response parser utilities."""
import json
import re
from typing import Dict, Any, Optional


def parse_json_response(text: str) -> Dict[str, Any]:
    """
    Parse JSON from LLM response text.
    
    Handles common issues like markdown code blocks, extra text, etc.
    
    Args:
        text: Raw response text from LLM
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If JSON cannot be parsed
    """
    text = text.strip()
    
    # Remove markdown code blocks
    if "```json" in text:
        text = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if text:
            text = text.group(1).strip()
    elif "```" in text:
        text = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
        if text:
            text = text.group(1).strip()
    
    # Try to find JSON object
    if text.startswith("{"):
        # Find the last closing brace
        brace_count = 0
        last_brace = -1
        for i, char in enumerate(text):
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == 0:
                    last_brace = i
                    break
        
        if last_brace > 0:
            text = text[:last_brace + 1]
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}. Text: {text[:200]}")


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate JSON data against schema (basic validation).
    
    Args:
        data: Data to validate
        schema: JSON schema
        
    Returns:
        True if valid
    """
    # Basic validation - check required fields
    if "required" in schema:
        for field in schema["required"]:
            if field not in data:
                return False
    
    # Check types
    if "properties" in schema:
        for field, field_schema in schema["properties"].items():
            if field in data:
                expected_type = field_schema.get("type")
                if expected_type:
                    actual_type = type(data[field]).__name__
                    type_map = {
                        "string": "str",
                        "number": ("int", "float"),
                        "integer": "int",
                        "boolean": "bool",
                        "array": "list",
                        "object": "dict",
                    }
                    
                    if expected_type in type_map:
                        if isinstance(type_map[expected_type], tuple):
                            if actual_type not in type_map[expected_type]:
                                return False
                        elif actual_type != type_map[expected_type]:
                            return False
    
    return True



