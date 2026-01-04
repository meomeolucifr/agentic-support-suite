# Master Setup Script - Full System Setup
# This script sets up and starts the entire multi-agent customer support system

param(
    [switch]$SkipServices,
    [switch]$SkipSeed,
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"

Write-Host "`n" -NoNewline
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  Multi-Agent Customer Support System - Full Setup" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Prerequisites
Write-Host "[1/7] Checking Prerequisites..." -ForegroundColor Yellow
Write-Host ""

$prereqsOk = $true

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  [OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Python not found! Please install Python 3.9+" -ForegroundColor Red
    $prereqsOk = $false
}

# Check Docker
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "  [OK] Docker: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Docker not found! Please install Docker Desktop" -ForegroundColor Red
    $prereqsOk = $false
}

# Check .env file
if (Test-Path ".env") {
    Write-Host "  [OK] .env file found" -ForegroundColor Green
    # Check if API keys are set
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "GEMINI_API_KEY=your_|DEEPSEEK_API_KEY=your_") {
        Write-Host "  [WARN] Please update API keys in .env file!" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [WARN] .env file not found!" -ForegroundColor Yellow
    Write-Host "  Please create .env file with required variables:" -ForegroundColor Cyan
    Write-Host "    LLM_PROVIDER=gemini (or deepseek)" -ForegroundColor White
    Write-Host "    GEMINI_API_KEY=your_key (or DEEPSEEK_API_KEY=your_key)" -ForegroundColor White
    Write-Host "    POSTGRES_HOST=localhost" -ForegroundColor White
    Write-Host "    POSTGRES_PORT=5432" -ForegroundColor White
    Write-Host "    POSTGRES_DB=support_system" -ForegroundColor White
    Write-Host "    POSTGRES_USER=postgres" -ForegroundColor White
    Write-Host "    POSTGRES_PASSWORD=postgres" -ForegroundColor White
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        $prereqsOk = $false
    }
}

if (-not $prereqsOk) {
    Write-Host "`n[ERROR] Prerequisites check failed. Please fix the issues above." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Start Infrastructure Services (PostgreSQL, Redis, Chroma)
Write-Host "[2/7] Starting Infrastructure Services..." -ForegroundColor Yellow
Write-Host ""

# Check if Docker is running
try {
    docker ps | Out-Null
} catch {
    Write-Host "  [ERROR] Docker is not running! Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Start PostgreSQL
Write-Host "  Starting PostgreSQL..." -ForegroundColor Cyan
$postgresRunning = docker ps --filter "name=postgres" --format "{{.Names}}" | Select-String "postgres"
if ($postgresRunning) {
    Write-Host "    [OK] PostgreSQL already running" -ForegroundColor Green
} else {
    docker-compose up -d postgres 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    [OK] PostgreSQL started" -ForegroundColor Green
    } else {
        Write-Host "    [ERROR] Failed to start PostgreSQL" -ForegroundColor Red
        exit 1
    }
}

# Start Redis
Write-Host "  Starting Redis..." -ForegroundColor Cyan
$redisRunning = docker ps --filter "name=redis" --format "{{.Names}}" | Select-String "redis"
if ($redisRunning) {
    Write-Host "    [OK] Redis already running" -ForegroundColor Green
} else {
    docker-compose up -d redis 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    [OK] Redis started" -ForegroundColor Green
    } else {
        Write-Host "    [ERROR] Failed to start Redis" -ForegroundColor Red
        exit 1
    }
}

# Start Chroma
Write-Host "  Starting Chroma..." -ForegroundColor Cyan
$chromaRunning = docker ps --filter "name=chroma" --format "{{.Names}}" | Select-String "chroma"
if ($chromaRunning) {
    Write-Host "    [OK] Chroma already running" -ForegroundColor Green
} else {
    docker-compose up -d chroma 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    [OK] Chroma started" -ForegroundColor Green
    } else {
        Write-Host "    [ERROR] Failed to start Chroma" -ForegroundColor Red
        exit 1
    }
}

Write-Host "  Waiting for services to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

Write-Host ""

# Step 3: Setup Database
Write-Host "[3/7] Setting Up Database..." -ForegroundColor Yellow
Write-Host ""

try {
    python scripts/setup_db.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Database setup complete" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] Database setup failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "  [ERROR] Database setup failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 4: Seed Knowledge Base
if (-not $SkipSeed) {
    Write-Host "[4/7] Seeding Knowledge Base..." -ForegroundColor Yellow
    Write-Host ""

    try {
        $output = python scripts/seed_knowledge_base.py 2>&1
        $output | Write-Host
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Knowledge base seeded" -ForegroundColor Green
        } else {
            Write-Host "  [ERROR] Knowledge base seeding failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
            Write-Host "  This might be OK if Chroma is not ready yet. You can run this later:" -ForegroundColor Yellow
            Write-Host "    python scripts/seed_knowledge_base.py" -ForegroundColor White
        }
    } catch {
        Write-Host "  [WARN] Knowledge base seeding failed: $_" -ForegroundColor Yellow
        Write-Host "  You can run this manually later: python scripts/seed_knowledge_base.py" -ForegroundColor Cyan
    }
} else {
    Write-Host "[4/7] Seeding Knowledge Base... [SKIPPED]" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Install Python Dependencies (if needed)
Write-Host "[5/7] Checking Python Dependencies..." -ForegroundColor Yellow
Write-Host ""

try {
    python -c "import fastapi, sqlalchemy, chromadb, redis, openai" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Python dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] Some dependencies missing. Installing..." -ForegroundColor Yellow
        pip install -r requirements.txt
        Write-Host "  [OK] Dependencies installed" -ForegroundColor Green
    }
} catch {
    Write-Host "  [WARN] Could not verify dependencies. Please run: pip install -r requirements.txt" -ForegroundColor Yellow
}

Write-Host ""

# Step 6: Start Agent Services
if (-not $SkipServices) {
    Write-Host "[6/7] Starting Agent Services..." -ForegroundColor Yellow
    Write-Host ""

    # Stop existing services first
    Write-Host "  Stopping existing services..." -ForegroundColor Cyan
    $ports = @(8000, 8001, 8002, 8003, 8004)
    foreach ($port in $ports) {
        $conn = netstat -ano | findstr ":$port" | findstr "LISTENING"
        if ($conn) {
            $pidLine = $conn -split '\s+'
            $pid = $pidLine[-1]
            if ($pid -match '^\d+$') {
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            }
        }
    }
    Start-Sleep -Seconds 2

    # Start services
    Write-Host "  Starting Router Agent..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents\router-agent'; python main.py" -WindowStyle Minimized
    Start-Sleep -Seconds 2

    Write-Host "  Starting Knowledge Agent..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents\knowledge-agent'; python main.py" -WindowStyle Minimized
    Start-Sleep -Seconds 2

    Write-Host "  Starting Sentiment Agent..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents\sentiment-agent'; python main.py" -WindowStyle Minimized
    Start-Sleep -Seconds 2

    Write-Host "  Starting Decision Agent..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents\decision-agent'; python main.py" -WindowStyle Minimized
    Start-Sleep -Seconds 2

    Write-Host "  Starting Orchestrator..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\orchestrator'; python main.py" -WindowStyle Minimized
    Start-Sleep -Seconds 5

    Write-Host "  [OK] All services started" -ForegroundColor Green
} else {
    Write-Host "[6/7] Starting Agent Services... [SKIPPED]" -ForegroundColor Yellow
}

Write-Host ""

# Step 7: Verify System
Write-Host "[7/7] Verifying System..." -ForegroundColor Yellow
Write-Host ""

if (-not $SkipServices) {
    Write-Host "  Checking service health..." -ForegroundColor Cyan
    Start-Sleep -Seconds 3
    
    $ports = @{
        8000 = "Orchestrator"
        8001 = "Router Agent"
        8002 = "Knowledge Agent"
        8003 = "Sentiment Agent"
        8004 = "Decision Agent"
    }
    
    $allHealthy = $true
    foreach ($port in $ports.Keys) {
        $conn = netstat -ano | findstr ":$port" | findstr "LISTENING"
        if ($conn) {
            Write-Host "    [OK] $($ports[$port]) (port $port)" -ForegroundColor Green
        } else {
            Write-Host "    [ERROR] $($ports[$port]) (port $port) - Not running" -ForegroundColor Red
            $allHealthy = $false
        }
    }
    
    if (-not $allHealthy) {
        Write-Host "  [WARN] Some services are not running. Check the PowerShell windows for errors." -ForegroundColor Yellow
    }
}

if (-not $SkipTests) {
    Write-Host "  Running system tests..." -ForegroundColor Cyan
    python scripts/test_agents.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] System tests passed" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] Some tests failed. Check the output above." -ForegroundColor Yellow
    }
} else {
    Write-Host "  [SKIPPED] System tests" -ForegroundColor Yellow
}

Write-Host ""

# Summary
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host "  2. Access: http://localhost:3000" -ForegroundColor White
Write-Host "  3. API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "To stop services:" -ForegroundColor Yellow
Write-Host "  .\restart-services.ps1 (will restart)" -ForegroundColor White
Write-Host "  Or close the PowerShell windows manually" -ForegroundColor White
Write-Host ""

