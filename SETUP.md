# Quick Setup Guide

## One-Command Setup

Chạy script này để setup toàn bộ hệ thống một lần:

```powershell
.\setup-full-system.ps1
```

Script này sẽ tự động:

1. ✅ **Kiểm tra prerequisites** (Python, Docker, .env)
2. ✅ **Start infrastructure** (PostgreSQL, Redis, Chroma)
3. ✅ **Setup database** (tạo tất cả tables)
4. ✅ **Seed knowledge base** (20+ cases thực tế)
5. ✅ **Start agent services** (Router, Knowledge, Sentiment, Decision, Orchestrator)
6. ✅ **Verify system** (health checks và tests)

## Trước khi chạy

### 1. Tạo file `.env`

Tạo file `.env` trong thư mục gốc với nội dung:

```env
# LLM Provider (chọn một)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Hoặc dùng DeepSeek
# LLM_PROVIDER=deepseek
# DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=support_system
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Chroma
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

### 2. Đảm bảo Docker đang chạy

Mở Docker Desktop và đợi đến khi Docker sẵn sàng.

### 3. Chạy setup script

```powershell
.\setup-full-system.ps1
```

## Options

Script hỗ trợ các options:

```powershell
# Skip seeding knowledge base
.\setup-full-system.ps1 -SkipSeed

# Skip starting services (chỉ setup database)
.\setup-full-system.ps1 -SkipServices

# Skip tests
.\setup-full-system.ps1 -SkipTests
```

## Sau khi setup

### Start Frontend

```powershell
cd frontend
npm install  # Chỉ cần chạy lần đầu
npm run dev
```

Truy cập: http://localhost:3000

### API Documentation

Truy cập: http://localhost:8000/docs

## Troubleshooting

### PostgreSQL không start được

```powershell
# Kiểm tra Docker
docker ps

# Start PostgreSQL thủ công
docker-compose up -d postgres

# Kiểm tra logs
docker logs support_postgres
```

### Services không start

```powershell
# Restart tất cả services
.\restart-services.ps1

# Hoặc start từng service
cd agents/router-agent
python main.py
```

### Knowledge base seeding failed

Có thể Chroma chưa sẵn sàng. Chạy lại sau:

```powershell
python scripts/seed_knowledge_base.py
```

### Database connection error

Đảm bảo PostgreSQL đang chạy:

```powershell
docker ps | findstr postgres
```

Nếu không có, start lại:

```powershell
docker-compose up -d postgres
```

## Manual Setup (nếu script không hoạt động)

### 1. Start Infrastructure

```powershell
docker-compose up -d postgres redis chroma
```

### 2. Setup Database

```powershell
python scripts/setup_db.py
```

### 3. Seed Knowledge Base

```powershell
python scripts/seed_knowledge_base.py
```

### 4. Start Services

```powershell
.\start-services.ps1
```

Hoặc start từng service trong terminal riêng:

```powershell
# Terminal 1
cd agents/router-agent && python main.py

# Terminal 2
cd agents/knowledge-agent && python main.py

# Terminal 3
cd agents/sentiment-agent && python main.py

# Terminal 4
cd agents/decision-agent && python main.py

# Terminal 5
cd orchestrator && python main.py
```

## Verify Installation

```powershell
# Test all agents
python scripts/test_agents.py

# Check service health
curl http://localhost:8000/api/health
curl http://localhost:8001/api/health
curl http://localhost:8002/api/health
curl http://localhost:8003/api/health
curl http://localhost:8004/api/health
```

## Next Steps

1. ✅ Setup hoàn tất!
2. 🚀 Start frontend: `cd frontend && npm run dev`
3. 📝 Tạo ticket test qua frontend hoặc API
4. 📊 Xem analytics và workflow trong dashboard


