# Phi Full System Startup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Phi Full System Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"

Write-Host "Startup Options:" -ForegroundColor Yellow
Write-Host "1. Start GPT-SoVITS API (Window A)" -ForegroundColor White
Write-Host "2. Start Voice Bridge (Window B)" -ForegroundColor White
Write-Host "3. Start GPT-SoVITS WebUI" -ForegroundColor White
Write-Host "4. Run First Voice Test" -ForegroundColor White
Write-Host "5. Start All (1 + 2 + 4)" -ForegroundColor Yellow
Write-Host "0. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Select (0-5)"

switch ($choice) {
    "1" {
        Write-Host "Starting GPT-SoVITS API..." -ForegroundColor Yellow
        $pythonPath = "$packageDir\runtime\python.exe"
        Set-Location $packageDir
        Start-Process -FilePath $pythonPath -ArgumentList "api_v2.py" -WindowStyle Normal
        Set-Location "C:\Users\waiti\missfay"
        Write-Host "API started at http://127.0.0.1:9880" -ForegroundColor Green
    }
    "2" {
        Write-Host "Starting Voice Bridge..." -ForegroundColor Yellow
        & ".\启动Phi系统.ps1"
    }
    "3" {
        Write-Host "Starting GPT-SoVITS WebUI..." -ForegroundColor Yellow
        Set-Location $packageDir
        Start-Process -FilePath ".\go-webui.bat"
        Set-Location "C:\Users\waiti\missfay"
        Write-Host "WebUI started at http://127.0.0.1:9874" -ForegroundColor Green
    }
    "4" {
        Write-Host "Running first voice test..." -ForegroundColor Yellow
        & ".\首次语音生成测试.ps1"
    }
    "5" {
        Write-Host "Starting all services..." -ForegroundColor Yellow
        
        # Start API
        Write-Host "[1/3] Starting GPT-SoVITS API..." -ForegroundColor Cyan
        $pythonPath = "$packageDir\runtime\python.exe"
        Set-Location $packageDir
        Start-Process -FilePath $pythonPath -ArgumentList "api_v2.py" -WindowStyle Normal
        Set-Location "C:\Users\waiti\missfay"
        Write-Host "  Waiting 10 seconds for API to initialize..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        # Start Voice Bridge
        Write-Host "[2/3] Starting Voice Bridge..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-File", ".\启动Phi系统.ps1" -WindowStyle Normal
        Write-Host "  Waiting 5 seconds for Voice Bridge to initialize..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # Run test
        Write-Host "[3/3] Running first voice test..." -ForegroundColor Cyan
        Start-Sleep -Seconds 3
        & ".\首次语音生成测试.ps1"
    }
    "0" {
        exit 0
    }
}

Write-Host ""


