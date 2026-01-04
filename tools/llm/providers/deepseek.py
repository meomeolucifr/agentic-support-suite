"""DeepSeek LLM provider (OpenAI-compatible)."""
import os
import json
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from tools.llm.base import BaseLLMProvider


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek LLM provider (OpenAI-compatible API)."""
    
    def __init__(self):
        """Initialize DeepSeek provider."""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is required")
        
        api_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=api_base
        )
        self.model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text completion."""
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    async def generate_json(
        self,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.3,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured JSON response."""
        # Add JSON format instruction
        json_prompt = f"""{prompt}

Please respond with valid JSON only. Do not include any text before or after the JSON."""
        
        if schema:
            json_prompt += f"\n\nExpected JSON schema: {json.dumps(schema, indent=2)}"
        
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": json_prompt}
            ],
            temperature=temperature,
            response_format={"type": "json_object"} if schema else None,
            **kwargs
        )
        
        text = response.choices[0].message.content.strip()
        
        # Try to extract JSON
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to fix common issues
            text = text.strip()
            if text.startswith("{"):
                last_brace = text.rfind("}")
                if last_brace > 0:
                    text = text[:last_brace + 1]
                    return json.loads(text)
            raise ValueError(f"Failed to parse JSON from response: {text[:200]}")
    
    async def get_embeddings(self, text: str) -> List[float]:
        """Generate embeddings (DeepSeek may not support embeddings directly)."""
        raise NotImplementedError(
            "DeepSeek API may not provide embeddings. "
            "Use Chroma's default embedding model or a separate embedding service."
        )



