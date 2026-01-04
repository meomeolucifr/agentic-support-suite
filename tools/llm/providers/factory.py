"""LLM provider factory."""
import os
from typing import Optional
from tools.llm.base import BaseLLMProvider
from tools.llm.providers.gemini import GeminiProvider
from tools.llm.providers.deepseek import DeepSeekProvider


_provider_instance: Optional[BaseLLMProvider] = None


def get_llm_provider() -> BaseLLMProvider:
    """
    Get configured LLM provider instance.
    
    Returns:
        LLM provider instance
        
    Raises:
        ValueError: If provider is not configured or invalid
    """
    global _provider_instance
    
    if _provider_instance is not None:
        return _provider_instance
    
    provider_name = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_name == "gemini":
        _provider_instance = GeminiProvider()
    elif provider_name == "deepseek":
        _provider_instance = DeepSeekProvider()
    else:
        raise ValueError(
            f"Unknown LLM provider: {provider_name}. "
            f"Supported providers: gemini, deepseek"
        )
    
    return _provider_instance


def reset_provider():
    """Reset provider instance (useful for testing)."""
    global _provider_instance
    _provider_instance = None



