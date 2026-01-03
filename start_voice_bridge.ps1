# Start Voice Bridge Service

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Phi Voice Bridge" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

# Check Python
if (-not (Test-Path $pythonPath)) {
    Write-Host "Error: Python not found" -ForegroundColor Red
    pause
    exit 1
}

# Check .env
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    @"
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct
GPT_SOVITS_URL=http://127.0.0.1:9880
GPT_SOVITS_API_VERSION=v2
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "  [OK] .env created" -ForegroundColor Green
}

# Check GPT-SoVITS
Write-Host "Checking GPT-SoVITS service..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  [OK] GPT-SoVITS is running" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] GPT-SoVITS not responding" -ForegroundColor Yellow
    Write-Host "  Please start GPT-SoVITS API first" -ForegroundColor Gray
    Write-Host ""
    $continue = Read-Host "Continue anyway? (Y/N)"
    if ($continue -ne "Y" -and $continue -ne "y") {
        exit 0
    }
}

Write-Host ""

# Install dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
& $pythonPath -m pip install fastapi uvicorn httpx pydantic python-dotenv requests -q 2>&1 | Out-Null
Write-Host "  [OK] Dependencies ready" -ForegroundColor Green
Write-Host ""

# Set environment variables
$env:GPT_SOVITS_URL = "http://127.0.0.1:9880"
$env:GPT_SOVITS_API_VERSION = "v2"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Voice Bridge Service" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Service URL: http://0.0.0.0:8000" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start service
& $pythonPath voice_bridge.py


