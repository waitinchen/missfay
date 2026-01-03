# MissFay Startup (CPU Mode)
$ErrorActionPreference = "SilentlyContinue"

Write-Host "============================" -ForegroundColor Cyan
Write-Host "   MissFay System Startup   " -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

$root = "C:\Users\waiti\missfay"
$packageDir = "$root\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

Write-Host "[1/2] Starting GPT-SoVITS API..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$packageDir'; .\runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880"

Write-Host "[2/2] Starting Voice Bridge..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; & '$pythonPath' voice_bridge.py"

Write-Host ""
Write-Host "Done! Please wait for both windows to initialize." -ForegroundColor Green
Write-Host "UI URL: http://localhost:8000/static/index.html" -ForegroundColor Cyan
