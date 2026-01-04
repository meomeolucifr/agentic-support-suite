# Script to switch from Gemini to DeepSeek
Write-Host "Switching to DeepSeek provider..." -ForegroundColor Green

$envFile = ".env"
if (-not (Test-Path $envFile)) {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    exit 1
}

# Read current .env
$content = Get-Content $envFile -Raw

# Update LLM_PROVIDER
if ($content -match "LLM_PROVIDER=") {
    $content = $content -replace "LLM_PROVIDER=.*", "LLM_PROVIDER=deepseek"
} else {
    $content += "`nLLM_PROVIDER=deepseek"
}

# Check if DEEPSEEK_API_KEY exists
if (-not ($content -match "DEEPSEEK_API_KEY=")) {
    Write-Host "`n[WARNING] DEEPSEEK_API_KEY not found in .env" -ForegroundColor Yellow
    Write-Host "Please add your DeepSeek API key:" -ForegroundColor Cyan
    Write-Host "  DEEPSEEK_API_KEY=your_deepseek_api_key_here" -ForegroundColor White
    $addKey = Read-Host "Do you want to add it now? (y/n)"
    if ($addKey -eq "y" -or $addKey -eq "Y") {
        $apiKey = Read-Host "Enter your DeepSeek API key"
        $content += "`nDEEPSEEK_API_KEY=$apiKey"
    }
}

# Write back to .env
Set-Content -Path $envFile -Value $content -NoNewline

Write-Host "`n[OK] Switched to DeepSeek provider!" -ForegroundColor Green
Write-Host "`nPlease restart services:" -ForegroundColor Yellow
Write-Host "  .\restart-services.ps1" -ForegroundColor White


