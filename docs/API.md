# API Documentation

## Overview

The Support System exposes REST APIs for ticket submission and management. All agents also expose their own APIs for direct access.

## Base URLs

- **Orchestrator**: `http://localhost:8000`
- **Router Agent**: `http://localhost:8001`
- **Knowledge Agent**: `http://localhost:8002`
- **Sentiment Agent**: `http://localhost:8003`
- **Decision Agent**: `http://localhost:8004`

## Orchestrator API

### Create Ticket

Submit a new support ticket for processing.

**Endpoint**: `POST /api/tickets`

**Request Body**:
```json
{
  "customer_id": "CUST_123",
  "subject": "I was charged twice",
  "body": "I noticed two identical charges on my credit card for my recent order."
}
```

**Response**:
```json
{
  "ticket_id": "TKT_2026_01_04_001",
  "status": "completed",
  "decision": "ESCALATE_TO_HUMAN",
  "solution": null,
  "escalated": true,
  "message": "Ticket processed successfully"
}
```

### Health Check

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "orchestrator"
}
```

### Detailed Health Check

**Endpoint**: `GET /api/health/detailed`

**Response**:
```json
{
  "orchestrator": "healthy",
  "agents": {
    "router": {
      "status": "healthy",
      "url": "http://localhost:8001"
    },
    "knowledge": {
      "status": "healthy",
      "url": "http://localhost:8002"
    },
    "sentiment": {
      "status": "healthy",
      "url": "http://localhost:8003"
    },
    "decision": {
      "status": "healthy",
      "url": "http://localhost:8004"
    }
  }
}
```

## Router Agent API

### Classify Ticket

**Endpoint**: `POST /api/process`

**Request Body**:
```json
{
  "ticket_id": "TKT_123",
  "text": "I was charged twice for my order"
}
```

**Response**:
```json
{
  "ticket_id": "TKT_123",
  "category": "BILLING",
  "subcategory": "DUPLICATE_CHARGE",
  "confidence": 0.98,
  "reason": "Customer states charged twice, requests refund"
}
```

## Knowledge Agent API

### Search Knowledge Base

**Endpoint**: `POST /api/process`

**Request Body**:
```json
{
  "ticket_id": "TKT_123",
  "text": "I was charged twice",
  "category": "BILLING"
}
```

**Response**:
```json
{
  "ticket_id": "TKT_123",
  "similar_cases_found": 3,
  "top_match_case_id": "CASE_5432",
  "similarity_score": 0.94,
  "solution": "Refund duplicate charge immediately, add $5 credit",
  "confidence": 0.87,
  "solvable_without_escalation": true
}
```

## Sentiment Agent API

### Analyze Sentiment

**Endpoint**: `POST /api/process`

**Request Body**:
```json
{
  "ticket_id": "TKT_123",
  "text": "I was charged twice! This is ridiculous!"
}
```

**Response**:
```json
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

## Decision Agent API

### Make Decision

**Endpoint**: `POST /api/process`

**Request Body**:
```json
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
```

**Response**:
```json
{
  "ticket_id": "TKT_123",
  "decision": "ESCALATE_TO_HUMAN",
  "confidence": 0.92,
  "reasoning": "Sentiment too high despite having solution",
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

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid request
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```



