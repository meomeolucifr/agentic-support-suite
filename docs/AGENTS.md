# Agent Specifications

## Overview

The system consists of 4 specialized AI agents, each performing a specific task in the ticket processing pipeline.

## Agent 1: Router Agent

### Purpose

Classifies incoming support tickets into categories and subcategories.

### Input

- Ticket text (subject + body)

### Output

- Category (BILLING, TECHNICAL, BUG, etc.)
- Subcategory (e.g., DUPLICATE_CHARGE for BILLING)
- Confidence score (0.0 - 1.0)
- Reasoning

### Implementation

- Uses LLM (Gemini/DeepSeek) for classification
- Prompt engineering for consistent results
- JSON schema validation for structured output

### Performance

- **Speed**: ~2 seconds per ticket
- **Accuracy**: 95%+ correct classification
- **Confidence Threshold**: 0.7+ for reliable classification

### Example

**Input**: "I was charged twice for my order"

**Output**:
```json
{
  "category": "BILLING",
  "subcategory": "DUPLICATE_CHARGE",
  "confidence": 0.98,
  "reason": "Customer states charged twice, requests refund"
}
```

## Agent 2: Knowledge Agent

### Purpose

Searches the knowledge base for similar cases and adapts solutions.

### Input

- Ticket text
- Category (from Router Agent)

### Output

- Number of similar cases found
- Top match case ID and similarity score
- Adapted solution
- Solution confidence
- Whether solvable without escalation

### Implementation

- Vector search using Chroma
- Semantic similarity matching
- LLM-based solution adaptation
- Confidence scoring

### Performance

- **Speed**: ~3 seconds per ticket
- **Accuracy**: 85%+ confidence on solutions
- **Similarity Threshold**: 0.7+ for good matches

### Example

**Input**: "I was charged twice", category: "BILLING"

**Output**:
```json
{
  "similar_cases_found": 3,
  "top_match_case_id": "CASE_5432",
  "similarity_score": 0.94,
  "solution": "Refund duplicate charge immediately, add $5 goodwill credit",
  "confidence": 0.87,
  "solvable_without_escalation": true
}
```

## Agent 3: Sentiment Agent

### Purpose

Analyzes customer sentiment, detects emotional state, and identifies churn risk.

### Input

- Ticket text

### Output

- Sentiment score (0.0 = calm, 1.0 = extremely angry)
- Emotional level (CALM, NEUTRAL, UPSET, ANGRY)
- Urgency level (LOW, MEDIUM, HIGH)
- Churn risk flag
- Human intervention requirement
- Recommended handler (BOT, HUMAN, MANAGER)

### Implementation

- LLM-based sentiment analysis (primary)
- HuggingFace Transformers (optional)
- Rule-based urgency detection
- Churn risk heuristics

### Performance

- **Speed**: ~1 second per ticket
- **Accuracy**: 92%+ sentiment detection
- **Sentiment Levels**:
  - CALM (0.0-0.3): Can be auto-resolved
  - NEUTRAL (0.3-0.5): Standard handling
  - UPSET (0.5-0.7): Frustrated but manageable
  - ANGRY (0.7-1.0): Requires human empathy

### Example

**Input**: "I was charged twice! This is ridiculous!"

**Output**:
```json
{
  "score": 0.92,
  "level": "ANGRY",
  "urgency": "HIGH",
  "churn_risk": true,
  "requires_human": true,
  "recommended_handler": "HUMAN"
}
```

## Agent 4: Decision Engine Agent

### Purpose

Synthesizes all agent outputs and makes the final decision on ticket handling.

### Input

- Router Agent results
- Knowledge Agent results
- Sentiment Agent results

### Output

- Final decision (AUTO_RESOLVE, ESCALATE_TO_HUMAN, ESCALATE_TO_MANAGER)
- Confidence score
- Reasoning
- Priority level
- SLA in minutes
- Comprehensive context for human agents

### Decision Logic

#### Hard Rules (Override Everything)

1. **High Sentiment**: If sentiment >= 0.85 → ESCALATE_TO_HUMAN
2. **Churn Risk**: If churn_risk = true → ESCALATE_TO_MANAGER
3. **Bug Reports**: If category = BUG → ESCALATE_TO_HUMAN

#### Normal Logic

1. **High Confidence + Low Sentiment**: 
   - If solution_confidence >= 0.85 AND sentiment < 0.7 → AUTO_RESOLVE
2. **Medium Confidence + Calm Customer**:
   - If solution_confidence >= 0.7 AND sentiment < 0.5 → AUTO_RESOLVE
3. **Default**: ESCALATE_TO_HUMAN with context

### Implementation

- Rule-based engine for hard rules
- LLM-assisted reasoning for nuanced cases
- Context aggregation for escalations
- Priority and SLA calculation

### Performance

- **Speed**: ~2 seconds per ticket
- **Accuracy**: 90%+ correct decisions
- **Decision Distribution** (target):
  - AUTO_RESOLVE: 70%
  - ESCALATE_TO_HUMAN: 20%
  - ESCALATE_TO_MANAGER: 10%

### Example

**Input**: All three agent results

**Output**:
```json
{
  "decision": "ESCALATE_TO_HUMAN",
  "confidence": 0.92,
  "reasoning": "Sentiment too high (0.92) despite having solution. Customer needs human empathy.",
  "priority": "HIGH",
  "sla_minutes": 5,
  "context": {
    "issue": "Duplicate charge",
    "solution": "Refund + $5 credit",
    "customer_sentiment": "ANGRY",
    "recommended_action": "Call customer, apologize, process refund"
  }
}
```

## Agent Communication

All agents expose REST APIs:
- `POST /api/process` - Process request
- `GET /api/health` - Health check

Agents are called sequentially by the Orchestrator:
1. Router → 2. Knowledge → 3. Sentiment → 4. Decision

## Error Handling

- Retry logic: 3 attempts with exponential backoff
- Timeout: 30 seconds per agent call
- Fallback: Default to escalation if agent fails
- Logging: All errors logged with context

## Monitoring

Each agent tracks:
- Processing time
- Success/failure rate
- Error types
- Performance metrics

## Configuration

Agents are configured via environment variables:
- Service URLs
- LLM provider selection
- Database connections
- Feature flags (e.g., USE_HUGGINGFACE)



