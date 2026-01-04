"""Semantic search logic."""
from typing import List, Dict, Any
from tools.llm.providers.factory import get_llm_provider
from tools.llm.prompts.knowledge_prompts import (
    get_solution_adaptation_prompt,
    get_solution_schema
)
from app.search.vector_search import search_similar


async def find_solution(
    ticket_text: str,
    category: str = None,
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Find solution by searching similar cases and adapting.
    
    Args:
        ticket_text: Ticket text
        category: Ticket category (optional)
        top_k: Number of similar cases to retrieve
        
    Returns:
        Solution with confidence
    """
    # Search for similar cases
    similar_cases = await search_similar(
        query_text=ticket_text,
        category=category,
        top_k=top_k
    )
    
    if not similar_cases:
        return {
            "similar_cases_found": 0,
            "solution": None,
            "confidence": 0.0,
            "solvable_without_escalation": False
        }
    
    # Format similar cases for LLM
    formatted_cases = []
    for case in similar_cases:
        formatted_cases.append({
            "issue": case.get("text", ""),
            "solution": case.get("metadata", {}).get("resolution", ""),
            "similarity": case.get("similarity", 0.0)
        })
    
    # Get top match
    top_match = similar_cases[0] if similar_cases else None
    
    # Use LLM to adapt solution (with graceful fallback if LLM fails)
    solution = None
    confidence = 0.0
    solvable_without_escalation = False
    
    try:
        llm = get_llm_provider()
        prompt = get_solution_adaptation_prompt(
            ticket_text=ticket_text,
            similar_cases=formatted_cases,
            category=category or "UNKNOWN"
        )
        schema = get_solution_schema()
        
        result = await llm.generate_json(
            prompt=prompt,
            schema=schema,
            temperature=0.3
        )
        
        solution = result.get("solution")
        confidence = result.get("confidence", 0.0)
        solvable_without_escalation = result.get("solvable_without_escalation", False)
        
    except Exception as e:
        # If LLM fails, use top match's resolution as fallback
        import logging
        logging.warning(f"LLM solution adaptation failed: {e}. Using top match resolution as fallback.")
        
        if top_match and top_match.get("metadata", {}).get("resolution"):
            solution = top_match["metadata"]["resolution"]
            # Use similarity score as confidence proxy
            confidence = min(top_match.get("similarity", 0.0) * 0.9, 0.85)  # Cap at 0.85 for fallback
            solvable_without_escalation = True
        else:
            # No resolution available, mark as needing escalation
            solution = "Similar cases found but unable to generate solution. Requires human review."
            confidence = 0.5
            solvable_without_escalation = False
    
    return {
        "similar_cases_found": len(similar_cases),
        "top_match_case_id": top_match.get("id") if top_match else None,
        "similarity_score": top_match.get("similarity") if top_match else None,
        "solution": solution,
        "confidence": confidence,
        "solvable_without_escalation": solvable_without_escalation,
        "similar_cases": similar_cases
    }

