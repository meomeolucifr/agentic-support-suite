# Start PostgreSQL using Docker
Write-Host "Starting PostgreSQL database..." -ForegroundColor Green

# Check if Docker is running
try {
    docker ps | Out-Null
} catch {
    Write-Host "[ERROR] Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if PostgreSQL container already exists
$existing = docker ps -a --filter "name=support_postgres" --format "{{.Names}}"
if ($existing -eq "support_postgres") {
    Write-Host "PostgreSQL container exists. Starting it..." -ForegroundColor Yellow
    docker start support_postgres
} else {
    Write-Host "Creating and starting PostgreSQL container..." -ForegroundColor Yellow
    docker run -d `
        --name support_postgres `
        -e POSTGRES_DB=support_system `
        -e POSTGRES_USER=postgres `
        -e POSTGRES_PASSWORD=postgres `
        -p 5432:5432 `
        postgres:15-alpine
}

Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Check if PostgreSQL is ready
$maxRetries = 10
$retry = 0
while ($retry -lt $maxRetries) {
    try {
        $result = docker exec support_postgres pg_isready -U postgres 2>&1
        if ($result -match "accepting connections") {
            Write-Host "[OK] PostgreSQL is ready!" -ForegroundColor Green
            Write-Host "Connection: postgresql://postgres:postgres@localhost:5432/support_system" -ForegroundColor Cyan
            break
        }
    } catch {
        # Continue retrying
    }
    $retry++
    Write-Host "  Retrying... ($retry/$maxRetries)" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
}

if ($retry -eq $maxRetries) {
    Write-Host "[WARNING] PostgreSQL might not be ready yet. Check with: docker logs support_postgres" -ForegroundColor Yellow
}

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Initialize database: python scripts/setup_db.py" -ForegroundColor White
Write-Host "2. Seed knowledge base: python scripts/seed_knowledge_base.py" -ForegroundColor White


