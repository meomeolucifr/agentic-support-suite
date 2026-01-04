# LLM Integration Tools

## Purpose

Provider-agnostic LLM integration that supports multiple LLM APIs (Gemini, DeepSeek) with a unified interface. Easy to add new providers.

## Structure

```
llm/
├── base.py              # Base LLM provider interface
├── providers/           # Provider implementations
│   ├── gemini.py       # Google Gemini API client
│   ├── deepseek.py     # DeepSeek API client
│   └── factory.py      # Provider factory/selector
├── prompts/             # Prompt templates
│   ├── router_prompts.py
│   ├── knowledge_prompts.py
│   ├── sentiment_prompts.py
│   └── decision_prompts.py
└── response_parser.py   # JSON response parsing
```

## Tech Stack

- **Gemini**: google-generativeai
- **DeepSeek**: OpenAI-compatible API (openai library)
- **Parsing**: JSON schema validation

## Key Components

### BaseLLMProvider Interface
Abstract base class that all providers implement:
- `generate(prompt: str) -> str` - Text generation
- `generate_json(prompt: str, schema: dict) -> dict` - Structured JSON
- `get_embeddings(text: str) -> List[float]` - Embeddings (if supported)

### Provider Implementations
- **GeminiProvider**: Google Gemini API
- **DeepSeekProvider**: DeepSeek API (OpenAI-compatible)

### Factory Pattern
- `get_llm_provider()` - Returns configured provider based on env var

## Usage Examples

### Getting Provider

```python
from tools.llm.providers.factory import get_llm_provider

llm = get_llm_provider()  # Returns Gemini or DeepSeek based on config
```

### Generating Text

```python
response = await llm.generate(
    prompt="Classify this ticket: I was charged twice",
    temperature=0.7,
    max_tokens=500
)
```

### Generating JSON

```python
response = await llm.generate_json(
    prompt="Classify this ticket: I was charged twice",
    schema={
        "type": "object",
        "properties": {
            "category": {"type": "string"},
            "confidence": {"type": "number"}
        }
    }
)
```

## Configuration

- `LLM_PROVIDER` - Provider to use: "gemini" or "deepseek"
- `GEMINI_API_KEY` - Gemini API key (if using Gemini)
- `DEEPSEEK_API_KEY` - DeepSeek API key (if using DeepSeek)

## Adding New Providers

1. Create new provider class inheriting from `BaseLLMProvider`
2. Implement required methods
3. Register in `factory.py`
4. Add configuration option



