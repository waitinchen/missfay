# Service Status Check

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Service Status Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check GPT-SoVITS API
Write-Host "Checking GPT-SoVITS API (http://127.0.0.1:9880)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  [OK] GPT-SoVITS API is running" -ForegroundColor Green
    $gptOk = $true
} catch {
    Write-Host "  [FAIL] GPT-SoVITS API not responding" -ForegroundColor Red
    Write-Host "  Please check Window A" -ForegroundColor Yellow
    $gptOk = $false
}

Write-Host ""

# Check Voice Bridge
Write-Host "Checking Voice Bridge (http://localhost:8000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  [OK] Voice Bridge is running" -ForegroundColor Green
    $bridgeOk = $true
} catch {
    Write-Host "  [FAIL] Voice Bridge not responding" -ForegroundColor Red
    Write-Host "  Please check Window B" -ForegroundColor Yellow
    $bridgeOk = $false
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($gptOk -and $bridgeOk) {
    Write-Host "All services are ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run the test:" -ForegroundColor Yellow
    Write-Host '  $py = ".\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\runtime\python.exe"' -ForegroundColor White
    Write-Host '  & $py first_voice_test.py' -ForegroundColor White
} else {
    Write-Host "Some services are not ready yet" -ForegroundColor Yellow
    Write-Host "Please wait for services to fully initialize" -ForegroundColor Yellow
}

Write-Host ""



