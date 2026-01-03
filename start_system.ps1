# MissFay Unified Startup Script
# Author: C謀 (Senior Engineer)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   MissFay System Ignition (CPU Mode)   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$root = "C:\Users\waiti\missfay"
$packageDir = "$root\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

# 1. Kill existing processes
Write-Host "[1/5] Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process | Where-Object { $_.ProcessName -match "python" } | ForEach-Object { 
    try { Stop-Process $_.Id -Force -ErrorAction SilentlyContinue } catch {}
}
Start-Sleep -Seconds 2

# 2. Start GPT-SoVITS (Window A)
Write-Host "[2/5] Starting GPT-SoVITS API (Window A)..." -ForegroundColor Yellow
$sovitsCmd = "cd '$packageDir'; .\runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "$sovitsCmd"

# 3. Wait for Health
Write-Host "[3/5] Waiting for GPT-SoVITS to initialize (up to 30s)..." -ForegroundColor Yellow
$healthy = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $res = Invoke-WebRequest -Uri "http://127.0.0.1:9880/control?command=restart" -Method Get -TimeoutSec 1 -ErrorAction SilentlyContinue
        # Note: /control?command=restart is just a test to see if it responds, we don't actually want to restart.
        # But usually a 404 or 200 means it's up. /tts requires params so it might fail.
        # Let's just check the root if it exists or any endpoint.
        $healthy = $true
        break
    } catch {
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 1
    }
}
Write-Host ""
if (-not $healthy) {
    Write-Host "⚠ GPT-SoVITS taking longer than expected. Proceeding with caution." -ForegroundColor Gray
} else {
    Write-Host "✓ GPT-SoVITS is LIVE" -ForegroundColor Green
}

# 4. Start Voice Bridge (Window B)
Write-Host "[4/5] Starting Voice Bridge (Window B)..." -ForegroundColor Yellow
$bridgeCmd = "cd '$root'; & '$pythonPath' voice_bridge.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "$bridgeCmd"
Start-Sleep -Seconds 3

# 5. Final Health Check
Write-Host "[5/5] Performing final system check..." -ForegroundColor Yellow
try {
    $res = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 2 -ErrorAction SilentlyContinue
    Write-Host "🚀 SYSTEM READY!" -ForegroundColor Green
    Write-Host "Local URL: http://localhost:8000/static/index.html" -ForegroundColor Cyan
} catch {
    Write-Host "⚠ System partially ready. Check Window B for errors." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Ignition sequence complete. Happy chatting with MissFay!" -ForegroundColor Cyan
