# Quick test script for a single agent
param(
    [Parameter(Mandatory=$true)]
    [string]$Agent,
    
    [Parameter(Mandatory=$false)]
    [string]$Port
)

$agents = @{
    "router" = @{ Port = 8001; Endpoint = "/api/process"; Body = '{"ticket_id":"TEST_001","text":"I was charged twice for my order"}' }
    "knowledge" = @{ Port = 8002; Endpoint = "/api/process"; Body = '{"ticket_id":"TEST_001","text":"I was charged twice","category":"BILLING"}' }
    "sentiment" = @{ Port = 8003; Endpoint = "/api/process"; Body = '{"ticket_id":"TEST_001","text":"I was charged twice! This is ridiculous!"}' }
    "decision" = @{ Port = 8004; Endpoint = "/api/process"; Body = '{"ticket_id":"TEST_001","category":"BILLING","sentiment_score":0.8,"similar_cases_found":2}' }
}

if (-not $agents.ContainsKey($Agent)) {
    Write-Host "Unknown agent: $Agent" -ForegroundColor Red
    Write-Host "Available agents: $($agents.Keys -join ', ')" -ForegroundColor Yellow
    exit 1
}

$config = $agents[$Agent]
$port = if ($Port) { $Port } else { $config.Port }
$url = "http://localhost:$port"

Write-Host "Testing $Agent agent at $url" -ForegroundColor Cyan

# Test health check
Write-Host "`n1. Health Check:" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$url/api/health" -ErrorAction Stop
    Write-Host "[OK] Health check passed: $($health | ConvertTo-Json -Compress)" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Health check failed: $_" -ForegroundColor Red
    exit 1
}

# Test functional endpoint
Write-Host "`n2. Functional Test:" -ForegroundColor Yellow
try {
    $result = Invoke-RestMethod -Uri "$url$($config.Endpoint)" -Method Post -ContentType "application/json" -Body $config.Body -ErrorAction Stop
    Write-Host "[OK] Test passed!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Cyan
    $result | ConvertTo-Json -Depth 10
} catch {
    Write-Host "[ERROR] Test failed: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response body: $responseBody" -ForegroundColor Yellow
    }
    exit 1
}


