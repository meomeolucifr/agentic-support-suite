"""Google Gemini LLM provider."""
import os
import json
import asyncio
import google.generativeai as genai
from typing import Dict, Any, Optional, List
from tools.llm.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider."""
    
    def __init__(self):
        """Initialize Gemini provider."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash as default (latest, faster) or gemini-1.5-pro for better quality
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.model = genai.GenerativeModel(self.model_name)
    
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text completion."""
        generation_config = {
            "temperature": temperature,
        }
        if max_tokens:
            generation_config["max_output_tokens"] = max_tokens
        
        # Run synchronous generate_content in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.model.generate_content(
                prompt,
                generation_config=generation_config,
                **kwargs
            )
        )
        
        return response.text
    
    async def generate_json(
        self,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
        temperature: float = 0.3,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured JSON response."""
        # Add JSON format instruction to prompt
        json_prompt = f"""{prompt}

Please respond with valid JSON only. Do not include any text before or after the JSON."""
        
        if schema:
            json_prompt += f"\n\nExpected JSON schema: {json.dumps(schema, indent=2)}"
        
        generation_config = {
            "temperature": temperature,
        }
        
        # Run synchronous generate_content in thread pool to avoid blocking
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    json_prompt,
                    generation_config=generation_config,
                    **kwargs
                )
            )
        except Exception as e:
            error_msg = str(e)
            # Check for quota/rate limit errors
            if "quota" in error_msg.lower() or "429" in error_msg or "ResourceExhausted" in str(type(e)):
                raise ValueError(
                    f"Gemini API quota exceeded. Free tier limit: 20 requests/day/model. "
                    f"Please wait or switch to DeepSeek provider. Error: {error_msg[:200]}"
                )
            raise ValueError(f"Gemini API call failed: {type(e).__name__}: {error_msg}")
        
        # Extract JSON from response
        try:
            # Check if response has text attribute
            if not hasattr(response, 'text') or not response.text:
                # Try to get text from parts
                if hasattr(response, 'parts') and response.parts:
                    text = response.parts[0].text.strip() if hasattr(response.parts[0], 'text') else str(response.parts[0])
                else:
                    raise ValueError(f"Invalid response from Gemini API: No text attribute. Response type: {type(response)}, Response: {response}")
            else:
                text = response.text.strip()
        except AttributeError as e:
            # Response might not have text attribute
            raise ValueError(f"Invalid response from Gemini API: {type(response)}. Error: {str(e)}. Response: {response}")
        
        # Try to find JSON in response (might have markdown code blocks)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Try to fix common issues
            text = text.strip()
            if text.startswith("{"):
                # Find the last }
                last_brace = text.rfind("}")
                if last_brace > 0:
                    text = text[:last_brace + 1]
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        pass
            raise ValueError(f"Failed to parse JSON from Gemini response. Error: {str(e)}. Response preview: {text[:500]}")
    
    async def get_embeddings(self, text: str) -> List[float]:
        """Generate embeddings (Gemini doesn't have direct embedding API, use Chroma's default)."""
        raise NotImplementedError(
            "Gemini doesn't provide direct embeddings API. "
            "Use Chroma's default embedding model or a separate embedding service."
        )


