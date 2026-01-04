"""Base LLM provider interface."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate text completion.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    async def generate_json(
        self,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.3,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response.
        
        Args:
            prompt: Input prompt with JSON format instructions
            schema: JSON schema to validate against (optional)
            temperature: Sampling temperature (lower for more deterministic)
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Parsed JSON dictionary
        """
        pass
    
    async def get_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for text (if supported).
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
            
        Raises:
            NotImplementedError: If provider doesn't support embeddings
        """
        raise NotImplementedError("This provider does not support embeddings")



