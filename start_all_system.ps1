# Phi 全系统启动脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Phi 全系统启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"

# 检查解压目录
if (-not (Test-Path $packageDir)) {
    Write-Host "错误: 解压目录不存在" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✓ 系统检查完成" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动选项" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 启动 GPT-SoVITS WebUI (窗口 A)" -ForegroundColor White
Write-Host "2. 启动 Voice Bridge (窗口 B)" -ForegroundColor White
Write-Host "3. 启动 GPT-SoVITS API (用于 Voice Bridge)" -ForegroundColor White
Write-Host "4. 执行首次语音生成测试" -ForegroundColor White
Write-Host "5. 全部启动 (1 + 3 + 2 + 4)" -ForegroundColor Yellow
Write-Host "0. 退出" -ForegroundColor White
Write-Host ""

$choice = Read-Host "请选择 (0-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "启动 GPT-SoVITS WebUI (窗口 A)..." -ForegroundColor Yellow
        Set-Location $packageDir
        Start-Process -FilePath ".\go-webui.bat"
        Set-Location "C:\Users\waiti\missfay"
        Write-Host "✓ WebUI 已在新窗口启动" -ForegroundColor Green
        Write-Host "  浏览器将自动打开: http://127.0.0.1:9874" -ForegroundColor Cyan
    }
    "2" {
        Write-Host ""
        Write-Host "启动 Voice Bridge (窗口 B)..." -ForegroundColor Yellow
        & ".\启动Phi系统.ps1"
    }
    "3" {
        Write-Host ""
        Write-Host "启动 GPT-SoVITS API..." -ForegroundColor Yellow
        $pythonPath = "$packageDir\runtime\python.exe"
        Set-Location $packageDir
        Start-Process -FilePath $pythonPath -ArgumentList "api_v2.py" -WindowStyle Normal
        Set-Location "C:\Users\waiti\missfay"
        Write-Host "✓ API 服务已在新窗口启动" -ForegroundColor Green
        Write-Host "  API 地址: http://127.0.0.1:9880" -ForegroundColor Cyan
    }
    "4" {
        Write-Host ""
        Write-Host "执行首次语音生成测试..." -ForegroundColor Yellow
        & ".\首次语音生成测试.ps1"
    }
    "5" {
        Write-Host ""
        Write-Host "启动所有服务..." -ForegroundColor Yellow
        Write-Host ""
        
        # 1. 启动 GPT-SoVITS API
        Write-Host "[1/4] 启动 GPT-SoVITS API..." -ForegroundColor Cyan
        $pythonPath = "$packageDir\runtime\python.exe"
        Set-Location $packageDir
        Start-Process -FilePath $pythonPath -ArgumentList "api_v2.py" -WindowStyle Normal
        Set-Location "C:\Users\waiti\missfay"
        Write-Host "  ✓ API 服务已启动" -ForegroundColor Green
        Write-Host "  等待 10 秒让服务初始化..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        # 2. 启动 Voice Bridge
        Write-Host ""
        Write-Host "[2/4] 启动 Voice Bridge..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-File", ".\启动Phi系统.ps1" -WindowStyle Normal
        Write-Host "  ✓ Voice Bridge 已在新窗口启动" -ForegroundColor Green
        Write-Host "  等待 5 秒让服务初始化..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # 3. 启动 WebUI (可选)
        Write-Host ""
        Write-Host "[3/4] 启动 GPT-SoVITS WebUI (可选)..." -ForegroundColor Cyan
        $startWebUI = Read-Host "是否启动 WebUI? (Y/N)"
        if ($startWebUI -eq "Y" -or $startWebUI -eq "y") {
            Set-Location $packageDir
            Start-Process -FilePath ".\go-webui.bat"
            Set-Location "C:\Users\waiti\missfay"
            Write-Host "  ✓ WebUI 已启动" -ForegroundColor Green
        }
        
        # 4. 执行测试
        Write-Host ""
        Write-Host "[4/4] 执行首次语音生成测试..." -ForegroundColor Cyan
        Write-Host "  等待 3 秒后开始测试..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        & ".\首次语音生成测试.ps1"
    }
    "0" {
        Write-Host "退出" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "无效选择" -ForegroundColor Red
    }
}

Write-Host ""

