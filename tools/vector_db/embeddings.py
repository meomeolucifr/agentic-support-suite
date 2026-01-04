"""Embedding generation utilities."""
from typing import List
import chromadb
from chromadb.utils import embedding_functions


def get_embedding_function(model_name: str = "all-MiniLM-L6-v2"):
    """
    Get embedding function for Chroma.
    
    Args:
        model_name: Embedding model name
        
    Returns:
        Embedding function
    """
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name
    )


async def generate_embeddings(texts: List[str], model_name: str = "all-MiniLM-L6-v2") -> List[List[float]]:
    """
    Generate embeddings for texts.
    
    Args:
        texts: List of texts to embed
        model_name: Embedding model name
        
    Returns:
        List of embedding vectors
    """
    embedding_fn = get_embedding_function(model_name)
    return embedding_fn(texts)



