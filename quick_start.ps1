# Quick Start Voice Bridge Service

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Phi Voice Bridge Service" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

# Check Python
if (-not (Test-Path $pythonPath)) {
    Write-Host "Python not found at: $pythonPath" -ForegroundColor Yellow
    Write-Host "Trying system Python..." -ForegroundColor Yellow
    $pythonPath = "python"
}

# Check .env
if (-not (Test-Path ".env")) {
    Write-Host "WARNING: .env file not found" -ForegroundColor Yellow
    Write-Host "Make sure GEMINI_API_KEY and CARTESIA_API_KEY are set" -ForegroundColor Yellow
    Write-Host ""
}

# Install dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
& $pythonPath -m pip install fastapi uvicorn httpx pydantic python-dotenv requests google-generativeai cartesia -q 2>&1 | Out-Null
Write-Host "Dependencies ready" -ForegroundColor Green
Write-Host ""

# Start service
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Service..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Service URL: http://localhost:8000" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Chat UI: http://localhost:8000/" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Change to project directory
Set-Location "C:\Users\waiti\missfay"

# Start service
& $pythonPath voice_bridge.py

