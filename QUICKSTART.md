# Quick Start Guide (Without Docker)

## Prerequisites

- Python 3.11+ installed
- LLM API key (Gemini or DeepSeek)

## Step 1: Configure Environment

Edit `.env` file and add your API key:

```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_actual_key_here
```

## Step 2: Install Dependencies

Already done! ✅

## Step 3: Start Services Locally

You'll need **5 terminal windows** - one for each service:

### Terminal 1: Router Agent
```powershell
cd agents/router-agent
python main.py
```

### Terminal 2: Knowledge Agent
```powershell
cd agents/knowledge-agent
python main.py
```

### Terminal 3: Sentiment Agent
```powershell
cd agents/sentiment-agent
python main.py
```

### Terminal 4: Decision Agent
```powershell
cd agents/decision-agent
python main.py
```

### Terminal 5: Orchestrator
```powershell
cd orchestrator
python main.py
```

## Step 4: Test the System

In a new terminal:

```powershell
# Test health checks
curl http://localhost:8000/api/health
curl http://localhost:8001/api/health
curl http://localhost:8002/api/health
curl http://localhost:8003/api/health
curl http://localhost:8004/api/health

# Submit a test ticket
Invoke-RestMethod -Uri http://localhost:8000/api/tickets -Method Post -ContentType "application/json" -Body '{"customer_id":"CUST_001","subject":"I was charged twice","body":"I see two identical charges on my credit card"}'
```

## Note About Databases

**Without Docker**, you'll need to install and run:
- **PostgreSQL** - For relational data (or use SQLite for testing)
- **Chroma** - For vector search (runs as a library, no separate service needed)
- **Redis** - Optional, for caching

For **quick testing**, you can modify the code to use SQLite instead of PostgreSQL temporarily.

---

## Option 2: Install Docker (Recommended for Production)

If you want to use Docker:

1. **Download Docker Desktop**: https://www.docker.com/products/docker-desktop/
2. **Install and start Docker Desktop**
3. **Restart your terminal**
4. **Then run**: `docker-compose up -d`



