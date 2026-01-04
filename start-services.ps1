# PowerShell script to start all services locally
# Make sure .env file is configured with your API keys

Write-Host "Starting all services..." -ForegroundColor Green

# Start Router Agent
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd agents/router-agent; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Knowledge Agent  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd agents/knowledge-agent; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Sentiment Agent
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd agents/sentiment-agent; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Decision Agent
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd agents/decision-agent; python main.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Orchestrator
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd orchestrator; python main.py" -WindowStyle Minimized

Write-Host "All services started! Check the minimized PowerShell windows." -ForegroundColor Green
Write-Host "Orchestrator: http://localhost:8000" -ForegroundColor Cyan



