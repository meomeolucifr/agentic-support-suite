# Script to prepare and push to GitHub
param(
    [string]$RepoName = "agentic-support-suite",
    [string]$Description = "An intelligent, production-ready multi-agent customer support system powered by AI"
)

Write-Host "`n" -NoNewline
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  Preparing Repository for GitHub" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "[OK] Git is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check if already a git repo
if (Test-Path ".git") {
    Write-Host "[OK] Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "Initializing Git repository..." -ForegroundColor Cyan
    git init
    Write-Host "[OK] Git repository initialized" -ForegroundColor Green
}

# Check current branch
$currentBranch = git branch --show-current 2>&1
if ($LASTEXITCODE -eq 0 -and $currentBranch) {
    Write-Host "[OK] Current branch: $currentBranch" -ForegroundColor Green
} else {
    Write-Host "Creating initial commit on main branch..." -ForegroundColor Cyan
    git checkout -b main 2>&1 | Out-Null
}

Write-Host "`nChecking .gitignore..." -ForegroundColor Cyan
if (Test-Path ".gitignore") {
    Write-Host "[OK] .gitignore exists" -ForegroundColor Green
} else {
    Write-Host "[WARN] .gitignore not found" -ForegroundColor Yellow
}

Write-Host "`nChecking for sensitive files..." -ForegroundColor Cyan
$sensitiveFiles = @(".env", ".env.local", "chroma_data", "*.log")
$foundSensitive = $false
foreach ($pattern in $sensitiveFiles) {
    $files = Get-ChildItem -Path . -Filter $pattern -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.FullName.Contains("node_modules") -and -not $_.FullName.Contains(".git") }
    if ($files) {
        Write-Host "  [WARN] Found sensitive files matching $pattern" -ForegroundColor Yellow
        $foundSensitive = $true
    }
}
if (-not $foundSensitive) {
    Write-Host "[OK] No sensitive files found" -ForegroundColor Green
}

Write-Host "`nPreparing to add files..." -ForegroundColor Cyan
Write-Host "  This will stage all files except those in .gitignore" -ForegroundColor White

# Add all files
Write-Host "`nAdding files to staging..." -ForegroundColor Cyan
git add .
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Files staged successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to stage files" -ForegroundColor Red
    exit 1
}

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "`nCommitting changes..." -ForegroundColor Cyan
    $commitMessage = "Initial commit: Agentic Support Suite - Multi-agent customer support system"
    git commit -m $commitMessage
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Changes committed successfully" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to commit changes" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`n[INFO] No changes to commit (repository is up to date)" -ForegroundColor Cyan
}

Write-Host "`n" -NoNewline
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  Repository Ready!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   - Go to: https://github.com/new" -ForegroundColor Cyan
Write-Host "   - Repository name: $RepoName" -ForegroundColor White
Write-Host "   - Description: $Description" -ForegroundColor White
Write-Host "   - Visibility: Public or Private" -ForegroundColor White
Write-Host "   - DO NOT initialize with README, .gitignore, or license" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Add remote and push:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/$RepoName.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Or use SSH:" -ForegroundColor White
Write-Host "   git remote add origin git@github.com:YOUR_USERNAME/$RepoName.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""

