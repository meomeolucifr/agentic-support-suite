"""Chroma vector database client."""
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings


_chroma_client = None
_chroma_collection = None


def get_chroma_client() -> chromadb.ClientAPI:
    """Get Chroma client instance."""
    global _chroma_client
    
    if _chroma_client is not None:
        return _chroma_client
    
    chroma_host = os.getenv("CHROMA_HOST", "localhost")
    chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
    
    # For persistent client (local)
    persist_directory = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
    
    # Try HTTP client first (if Chroma server is running)
    try:
        _chroma_client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(anonymized_telemetry=False)
        )
        # Test connection
        _chroma_client.heartbeat()
    except Exception:
        # Fallback to persistent client (local)
        _chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
    
    return _chroma_client


def get_collection(name: Optional[str] = None) -> chromadb.Collection:
    """Get or create Chroma collection."""
    global _chroma_collection
    
    collection_name = name or os.getenv("CHROMA_COLLECTION_NAME", "support_cases")
    client = get_chroma_client()
    
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        # Collection doesn't exist, create it
        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "Support ticket cases"}
        )
    
    return collection


async def search_similar_cases(
    query_text: str,
    collection_name: Optional[str] = None,
    top_k: int = 5,
    filter_dict: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Search for similar cases in Chroma.
    
    Args:
        query_text: Query text to search for
        collection_name: Collection name (optional)
        top_k: Number of results to return
        filter_dict: Metadata filters
        
    Returns:
        List of similar cases with metadata
    """
    collection = get_collection(collection_name)
    
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
        where=filter_dict if filter_dict else None
    )
    
    # Format results
    similar_cases = []
    if results["ids"] and len(results["ids"][0]) > 0:
        for i in range(len(results["ids"][0])):
            similar_cases.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i] if results["documents"] else "",
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else 0.0,
                "similarity": 1.0 - results["distances"][0][i] if results["distances"] else 0.0
            })
    
    return similar_cases


async def add_case(
    case_id: str,
    text: str,
    metadata: Dict[str, Any],
    collection_name: Optional[str] = None
):
    """
    Add a case to Chroma collection.
    
    Args:
        case_id: Unique case ID
        text: Case text (will be embedded)
        metadata: Case metadata
        collection_name: Collection name (optional)
    """
    collection = get_collection(collection_name)
    
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[case_id]
    )


async def update_case(
    case_id: str,
    text: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    collection_name: Optional[str] = None
):
    """
    Update a case in Chroma collection.
    
    Args:
        case_id: Case ID to update
        text: Updated text (optional)
        metadata: Updated metadata (optional)
        collection_name: Collection name (optional)
    """
    collection = get_collection(collection_name)
    
    update_data = {}
    if text is not None:
        update_data["documents"] = [text]
    if metadata is not None:
        update_data["metadatas"] = [metadata]
    
    if update_data:
        collection.update(
            ids=[case_id],
            **update_data
        )


async def delete_case(
    case_id: str,
    collection_name: Optional[str] = None
):
    """
    Delete a case from Chroma collection.
    
    Args:
        case_id: Case ID to delete
        collection_name: Collection name (optional)
    """
    collection = get_collection(collection_name)
    collection.delete(ids=[case_id])



