# Start GPT-SoVITS API Service

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting GPT-SoVITS API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

Set-Location $packageDir

Write-Host "Starting API service..." -ForegroundColor Yellow
Write-Host "API will be available at: http://127.0.0.1:9880" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start API
& $pythonPath api_v2.py


