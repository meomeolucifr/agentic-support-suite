# Script to restart all services cleanly
Write-Host "Stopping all existing services..." -ForegroundColor Yellow

# Find and kill all Python processes running on our ports
$ports = @(8000, 8001, 8002, 8003, 8004)
foreach ($port in $ports) {
    $connections = netstat -ano | findstr ":$port" | findstr "LISTENING"
    if ($connections) {
        $pid = ($connections -split '\s+')[-1]
        if ($pid -match '^\d+$') {
            Write-Host "  Killing process $pid on port $port" -ForegroundColor Yellow
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
}

Start-Sleep -Seconds 2

Write-Host "`nStarting all services..." -ForegroundColor Green

# Start Router Agent
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents\router-agent'; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Knowledge Agent  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents\knowledge-agent'; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Sentiment Agent
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents\sentiment-agent'; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Decision Agent
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents\decision-agent'; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Orchestrator
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\orchestrator'; python main.py" -WindowStyle Minimized

Write-Host "`nAll services started! Check the minimized PowerShell windows." -ForegroundColor Green
Write-Host "Waiting 5 seconds for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "`nTesting services..." -ForegroundColor Cyan
python scripts/test_agents.py



