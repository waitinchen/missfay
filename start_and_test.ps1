# 启动服务并测试

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Start Service and Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查服务是否运行
Write-Host "Checking if service is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "  [OK] Service is already running" -ForegroundColor Green
    Write-Host ""
    Write-Host "Testing interface..." -ForegroundColor Yellow
    & ".\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\runtime\python.exe" test_service_direct.py
} catch {
    Write-Host "  [WARN] Service is not running" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please start the service:" -ForegroundColor Yellow
    Write-Host "  .\start_voice_bridge.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run this script again to test" -ForegroundColor Gray
}

Write-Host ""

