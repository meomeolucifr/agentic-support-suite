"""Prompt templates for Knowledge Agent."""


def get_solution_adaptation_prompt(
    ticket_text: str,
    similar_cases: list,
    category: str
) -> str:
    """
    Get prompt for adapting solution from similar cases.
    
    Args:
        ticket_text: Current ticket text
        similar_cases: List of similar cases with solutions
        category: Ticket category
        
    Returns:
        Formatted prompt
    """
    cases_text = "\n\n".join([
        f"Case {i+1}:\n"
        f"  Issue: {case.get('issue', 'N/A')}\n"
        f"  Solution: {case.get('solution', 'N/A')}\n"
        f"  Similarity: {case.get('similarity', 0):.2f}"
        for i, case in enumerate(similar_cases)
    ])
    
    return f"""You found similar cases for this ticket. Adapt the solution to the current customer's issue.

Current Ticket:
{ticket_text}

Category: {category}

Similar Cases Found:
{cases_text}

Analyze these similar cases and determine:
1. Can this ticket be solved using the solutions from similar cases?
2. What is the best solution for this specific ticket?
3. What is your confidence level (0.0 to 1.0)?

Return a JSON object with:
- solution: The recommended solution for this ticket
- confidence: Confidence score (0.0 to 1.0)
- solvable_without_escalation: true if bot can handle, false if human needed
- reasoning: Brief explanation

Example response:
{{
    "solution": "Refund the duplicate charge immediately and add $5 goodwill credit",
    "confidence": 0.87,
    "solvable_without_escalation": true,
    "reasoning": "Similar case shows this is a common issue with a standard resolution"
}}"""


def get_solution_schema() -> dict:
    """Get JSON schema for solution adaptation response."""
    return {
        "type": "object",
        "properties": {
            "solution": {
                "type": "string"
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0
            },
            "solvable_without_escalation": {
                "type": "boolean"
            },
            "reasoning": {
                "type": "string"
            }
        },
        "required": ["solution", "confidence", "solvable_without_escalation"]
    }



