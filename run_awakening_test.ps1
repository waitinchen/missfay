# Awakening Test Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Phi Awakening Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

Write-Host "Checking services..." -ForegroundColor Yellow
Write-Host ""

# Check GPT-SoVITS API
Write-Host "Checking GPT-SoVITS API (http://127.0.0.1:9880)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  [OK] GPT-SoVITS API is running" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] GPT-SoVITS API not responding" -ForegroundColor Yellow
    Write-Host "  Waiting 5 seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}

Write-Host ""

# Check Voice Bridge
Write-Host "Checking Voice Bridge (http://localhost:8000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  [OK] Voice Bridge is running" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] Voice Bridge not responding" -ForegroundColor Yellow
    Write-Host "  Waiting 5 seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Executing First Voice Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test Text: 主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]" -ForegroundColor White
Write-Host "Arousal Level: 2 (Calm with a hint of awakening excitement)" -ForegroundColor White
Write-Host ""

# Install dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
& $pythonPath -m pip install requests -q 2>&1 | Out-Null

Write-Host "Running test script..." -ForegroundColor Yellow
Write-Host ""

# Execute test
& $pythonPath first_voice_test.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Test Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""


