# Testing Guide

## Quick Start

### 1. Start All Services

**Option A: Using PowerShell Script (Recommended)**
```powershell
.\start-services.ps1
```

**Option B: Manual Start**
Mở 5 cửa sổ PowerShell riêng và chạy:

```powershell
# Terminal 1 - Router Agent
cd agents/router-agent
python main.py

# Terminal 2 - Knowledge Agent
cd agents/knowledge-agent
python main.py

# Terminal 3 - Sentiment Agent
cd agents/sentiment-agent
python main.py

# Terminal 4 - Decision Agent
cd agents/decision-agent
python main.py

# Terminal 5 - Orchestrator
cd orchestrator
python main.py
```

### 2. Verify Services Are Running

Check health endpoints:
- Router Agent: http://localhost:8001/api/health
- Knowledge Agent: http://localhost:8002/api/health
- Sentiment Agent: http://localhost:8003/api/health
- Decision Agent: http://localhost:8004/api/health
- Orchestrator: http://localhost:8000/api/health

### 3. Run Tests

**Option A: PowerShell Script**
```powershell
.\test_system.ps1
```

**Option B: Python Script**
```powershell
python scripts/test_agents.py
```

## Manual Testing

### Test Router Agent

```powershell
$body = @{
    ticket_id = "TEST_001"
    text = "I was charged twice for my order"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/process" -Method Post -Body $body -ContentType "application/json"
```

### Test Knowledge Agent

```powershell
$body = @{
    ticket_id = "TEST_001"
    text = "I was charged twice"
    category = "BILLING"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8002/api/process" -Method Post -Body $body -ContentType "application/json"
```

### Test Sentiment Agent

```powershell
$body = @{
    ticket_id = "TEST_001"
    text = "I was charged twice! This is ridiculous!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8003/api/process" -Method Post -Body $body -ContentType "application/json"
```

### Test Full Ticket Processing (Orchestrator)

```powershell
$body = @{
    customer_id = "CUST_TEST_001"
    subject = "Duplicate charge"
    body = "I noticed two identical charges on my credit card for my recent order."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/tickets" -Method Post -Body $body -ContentType "application/json"
```

## API Documentation

Visit these URLs in your browser:
- Orchestrator: http://localhost:8000/docs
- Router Agent: http://localhost:8001/docs
- Knowledge Agent: http://localhost:8002/docs
- Sentiment Agent: http://localhost:8003/docs
- Decision Agent: http://localhost:8004/docs

## Troubleshooting

### Services Not Starting

1. **Check .env file**: Make sure you have API keys configured:
   ```
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   ```

2. **Check Dependencies**: Make sure PostgreSQL, Redis, and Chroma are running:
   ```powershell
   # If using Docker:
   docker compose up -d postgres redis chroma
   ```

3. **Check Ports**: Make sure ports 8000-8004 are not in use:
   ```powershell
   netstat -ano | findstr "8000 8001 8002 8003 8004"
   ```

### Common Errors

- **Connection refused**: Service not running, check the PowerShell windows
- **API key error**: Check your .env file has valid API keys
- **Database error**: Make sure PostgreSQL is running and accessible
- **Chroma error**: Make sure Chroma is running on port 8000 (or update CHROMA_PORT in .env)



