# Fix Issues and Retest

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Fixing Issues and Retesting" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure .env exists
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

Write-Host ""
Write-Host "Checking services..." -ForegroundColor Yellow
Write-Host ""

# Check services with longer timeout
$gptOk = $false
$bridgeOk = $false

Write-Host "Checking GPT-SoVITS API..." -ForegroundColor Yellow
for ($i = 1; $i -le 5; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  [OK] GPT-SoVITS API is running" -ForegroundColor Green
            $gptOk = $true
            break
        }
    } catch {
        Write-Host "  Attempt $i/5: Not ready yet, waiting..." -ForegroundColor Gray
        Start-Sleep -Seconds 3
    }
}

if (-not $gptOk) {
    Write-Host "  [WARN] GPT-SoVITS API not responding" -ForegroundColor Yellow
    Write-Host "  Please start it manually in Window A" -ForegroundColor Yellow
}

Write-Host ""

Write-Host "Checking Voice Bridge..." -ForegroundColor Yellow
for ($i = 1; $i -le 5; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  [OK] Voice Bridge is running" -ForegroundColor Green
            $bridgeOk = $true
            break
        }
    } catch {
        Write-Host "  Attempt $i/5: Not ready yet, waiting..." -ForegroundColor Gray
        Start-Sleep -Seconds 3
    }
}

if (-not $bridgeOk) {
    Write-Host "  [WARN] Voice Bridge not responding" -ForegroundColor Yellow
    Write-Host "  Please start it manually in Window B" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Service Status" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GPT-SoVITS API: $(if ($gptOk) { '[OK]' } else { '[NOT READY]' })" -ForegroundColor $(if ($gptOk) { "Green" } else { "Yellow" })
Write-Host "Voice Bridge: $(if ($bridgeOk) { '[OK]' } else { '[NOT READY]' })" -ForegroundColor $(if ($bridgeOk) { "Green" } else { "Yellow" })
Write-Host ""

if ($gptOk -and $bridgeOk) {
    Write-Host "All services ready. Running tests..." -ForegroundColor Green
    Write-Host ""
    & ".\qa_pressure_test.ps1"
} else {
    Write-Host "Please start services first:" -ForegroundColor Yellow
    Write-Host "  Window A: cd `"$packageDir`" ; .\runtime\python.exe api_v2.py" -ForegroundColor White
    Write-Host "  Window B: .\启动Phi系统.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run: .\qa_pressure_test.ps1" -ForegroundColor Yellow
}



