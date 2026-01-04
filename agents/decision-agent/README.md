# Decision Agent

## Purpose

The Decision Engine Agent synthesizes all signals from the previous three agents and makes the final decision: AUTO_RESOLVE, ESCALATE_TO_HUMAN, or ESCALATE_TO_MANAGER. It also builds comprehensive context for human agents when escalation is needed.

## Structure

```
decision-agent/
├── main.py                    # FastAPI entry point
├── app/
│   ├── agent.py              # DecisionEngineAgent class
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── engine/
│   │   ├── decision_logic.py # Decision rules engine
│   │   └── context_builder.py # Context aggregation
│   └── models/
│       └── decision.py       # Decision models
└── requirements.txt
```

## Tech Stack

- **Framework**: FastAPI
- **Decision Engine**: Rule-based + LLM-assisted reasoning
- **Validation**: Pydantic v2

## Key Components

### DecisionEngineAgent Class
- Receives results from Router, Knowledge, and Sentiment agents
- Applies decision rules
- Builds escalation context
- Returns final decision with reasoning

### Decision Logic
- **Hard Rules**: Sentiment >= 0.85 → ESCALATE_TO_HUMAN
- **Normal Logic**: Confidence thresholds + sentiment combinations
- **Context Building**: Aggregates all agent outputs for human review

### Decision Types
- `AUTO_RESOLVE` - Bot can handle, send solution to customer
- `ESCALATE_TO_HUMAN` - Needs human agent, include context
- `ESCALATE_TO_MANAGER` - High priority, churn risk, manager needed

## Usage Examples

### Starting the Service

```bash
cd agents/decision-agent
uvicorn main:app --host 0.0.0.0 --port 8004
```

### Making Decision

```python
POST /process
{
    "ticket_id": "TKT_123",
    "router_result": {
        "category": "BILLING",
        "confidence": 0.98
    },
    "knowledge_result": {
        "solution": "Refund duplicate charge",
        "confidence": 0.87
    },
    "sentiment_result": {
        "score": 0.92,
        "churn_risk": true
    }
}

Response:
{
    "ticket_id": "TKT_123",
    "decision": "ESCALATE_TO_HUMAN",
    "confidence": 0.92,
    "reasoning": "Sentiment too high despite solution",
    "context": {
        "issue": "Duplicate charge",
        "solution": "Refund + $5 credit",
        "customer_sentiment": "ANGRY",
        "recommended_action": "Call customer, apologize, process refund"
    },
    "priority": "HIGH",
    "sla_minutes": 5
}
```

## Dependencies

- `tools/database` - Database models
- `tools/integrations` - For notifications (Slack, Email)
- PostgreSQL for storing decisions

## Configuration

- Integration API keys (Slack, Email)
- Database connection settings
- SLA configuration



