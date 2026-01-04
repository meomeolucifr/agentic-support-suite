# Sentiment Agent

## Purpose

The Sentiment Agent analyzes customer sentiment from ticket text, detects emotional state, urgency, and churn risk. This information influences whether a ticket should be auto-resolved or escalated to a human.

## Structure

```
sentiment-agent/
├── main.py                    # FastAPI entry point
├── app/
│   ├── agent.py              # SentimentAnalyzerAgent class
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── analyzers/
│   │   ├── llm_sentiment.py  # LLM-based analysis
│   │   └── huggingface_sentiment.py # HF model option
│   └── models/
│       └── sentiment.py      # Sentiment models
└── requirements.txt
```

## Tech Stack

- **Framework**: FastAPI
- **LLM**: Multi-provider (Gemini/DeepSeek) for sentiment analysis
- **Alternative**: HuggingFace Transformers (local models)
- **ML**: PyTorch, Transformers

## Key Components

### SentimentAnalyzerAgent Class
- Receives ticket text
- Analyzes sentiment (score 0-1)
- Detects emotional level (CALM, NEUTRAL, UPSET, ANGRY)
- Calculates churn risk
- Determines if human touch is needed

### Sentiment Levels
- **CALM** (0.0-0.3): Customer is polite, can be auto-resolved
- **NEUTRAL** (0.3-0.5): Standard handling
- **UPSET** (0.5-0.7): Frustrated but manageable
- **ANGRY** (0.7-1.0): Requires human empathy, high escalation priority

## Usage Examples

### Starting the Service

```bash
cd agents/sentiment-agent
uvicorn main:app --host 0.0.0.0 --port 8003
```

### Analyzing Sentiment

```python
POST /process
{
    "ticket_id": "TKT_123",
    "text": "I was charged twice! This is ridiculous!"
}

Response:
{
    "ticket_id": "TKT_123",
    "score": 0.92,
    "level": "ANGRY",
    "urgency": "HIGH",
    "churn_risk": true,
    "requires_human": true,
    "recommended_handler": "HUMAN"
}
```

## Dependencies

- `tools/llm` - LLM provider for sentiment analysis
- `tools/database` - Database models
- HuggingFace Transformers (optional, for local models)
- PostgreSQL for storing sentiment analysis

## Configuration

- `LLM_PROVIDER` - LLM provider (gemini/deepseek)
- `USE_HUGGINGFACE` - Use local HF models instead of LLM (optional)
- Database connection settings



