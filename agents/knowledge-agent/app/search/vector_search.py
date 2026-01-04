"""Vector search implementation."""
from typing import List, Dict, Any
from tools.vector_db.chroma_client import search_similar_cases


async def search_similar(
    query_text: str,
    category: str = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for similar cases using vector search.
    
    Args:
        query_text: Query text
        category: Filter by category (optional)
        top_k: Number of results
        
    Returns:
        List of similar cases
    """
    filter_dict = None
    if category:
        filter_dict = {"category": category}
    
    results = await search_similar_cases(
        query_text=query_text,
        top_k=top_k,
        filter_dict=filter_dict
    )
    
    return results



