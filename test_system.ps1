# Quick test script for the support system
Write-Host "`n=== Testing Multi-Agent Support System ===" -ForegroundColor Cyan
Write-Host ""

# Test health endpoints
$services = @(
    @{Name="Router Agent"; Port=8001},
    @{Name="Knowledge Agent"; Port=8002},
    @{Name="Sentiment Agent"; Port=8003},
    @{Name="Decision Agent"; Port=8004},
    @{Name="Orchestrator"; Port=8000}
)

Write-Host "1. Checking service health..." -ForegroundColor Yellow
foreach ($service in $services) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$($service.Port)/api/health" -TimeoutSec 2 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  [OK] $($service.Name) (port $($service.Port))" -ForegroundColor Green
        }
    } catch {
        Write-Host "  [ERROR] $($service.Name) (port $($service.Port)) - Not running" -ForegroundColor Red
    }
}

Write-Host "`n2. Testing Router Agent..." -ForegroundColor Yellow
try {
    $body = @{
        ticket_id = "TEST_001"
        text = "I was charged twice for my order"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8001/api/process" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 30
    Write-Host "  [OK] Router Agent responded" -ForegroundColor Green
    Write-Host "  Category: $($response.category)" -ForegroundColor Cyan
    Write-Host "  Confidence: $($response.confidence)" -ForegroundColor Cyan
} catch {
    Write-Host "  [ERROR] Router Agent test failed: $_" -ForegroundColor Red
}

Write-Host "`n3. Testing Orchestrator (full ticket processing)..." -ForegroundColor Yellow
try {
    $body = @{
        customer_id = "CUST_TEST_001"
        subject = "Duplicate charge"
        body = "I noticed two identical charges on my credit card for my recent order."
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/tickets" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 60
    Write-Host "  [OK] Ticket processed successfully" -ForegroundColor Green
    Write-Host "  Ticket ID: $($response.ticket_id)" -ForegroundColor Cyan
    Write-Host "  Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "  Decision: $($response.decision)" -ForegroundColor Cyan
} catch {
    Write-Host "  [ERROR] Orchestrator test failed: $_" -ForegroundColor Red
    Write-Host "  Make sure all agents are running!" -ForegroundColor Yellow
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Cyan
Write-Host "`nTo view API docs, visit:" -ForegroundColor Yellow
Write-Host "  - Orchestrator: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  - Router Agent: http://localhost:8001/docs" -ForegroundColor Cyan



