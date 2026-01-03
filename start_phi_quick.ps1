# Phi 系统一键启动脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动 Phi 系统" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"

# 检查解压目录
if (-not (Test-Path $packageDir)) {
    Write-Host "错误: 解压目录不存在" -ForegroundColor Red
    Write-Host "请确保整合包已解压完成" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✓ 解压目录已就绪" -ForegroundColor Green
Write-Host ""

# 检查 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "警告: .env 文件不存在" -ForegroundColor Yellow
    Write-Host "正在创建 .env 文件..." -ForegroundColor Yellow
    
    $envContent = @"
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct
GPT_SOVITS_URL=http://127.0.0.1:9880
GPT_SOVITS_API_VERSION=v2
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✓ .env 文件已创建" -ForegroundColor Green
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动选项" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 启动 GPT-SoVITS WebUI" -ForegroundColor White
Write-Host "2. 启动 GPT-SoVITS API (api_v2.py)" -ForegroundColor White
Write-Host "3. 启动 Voice Bridge" -ForegroundColor White
Write-Host "4. 运行无过滤测试" -ForegroundColor White
Write-Host "5. 运行完整测试套件" -ForegroundColor White
Write-Host "0. 退出" -ForegroundColor White
Write-Host ""

$choice = Read-Host "请选择 (0-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "启动 GPT-SoVITS WebUI..." -ForegroundColor Yellow
        Write-Host "浏览器将自动打开 http://127.0.0.1:9874" -ForegroundColor Cyan
        Write-Host ""
        Set-Location $packageDir
        Start-Process -FilePath ".\go-webui.bat"
        Set-Location "C:\Users\waiti\missfay"
    }
    "2" {
        Write-Host ""
        Write-Host "启动 GPT-SoVITS API..." -ForegroundColor Yellow
        Write-Host "API 将在 http://127.0.0.1:9880 启动" -ForegroundColor Cyan
        Write-Host ""
        Set-Location $packageDir
        $pythonPath = "$packageDir\runtime\python.exe"
        Start-Process -FilePath $pythonPath -ArgumentList "api_v2.py" -WindowStyle Normal
        Set-Location "C:\Users\waiti\missfay"
        Write-Host "✓ API 服务已启动（新窗口）" -ForegroundColor Green
    }
    "3" {
        Write-Host ""
        Write-Host "启动 Voice Bridge..." -ForegroundColor Yellow
        Write-Host "服务将在 http://0.0.0.0:8000 启动" -ForegroundColor Cyan
        Write-Host ""
        $pythonPath = "$packageDir\runtime\python.exe"
        
        # 检查依赖
        Write-Host "检查依赖..." -ForegroundColor Yellow
        & $pythonPath -m pip install fastapi uvicorn httpx pydantic python-dotenv requests -q
        
        # 设置环境变量
        $env:GPT_SOVITS_URL = "http://127.0.0.1:9880"
        $env:GPT_SOVITS_API_VERSION = "v2"
        
        Write-Host "启动服务..." -ForegroundColor Yellow
        & $pythonPath voice_bridge.py
    }
    "4" {
        Write-Host ""
        Write-Host "运行无过滤测试..." -ForegroundColor Yellow
        Write-Host ""
        $pythonPath = "$packageDir\runtime\python.exe"
        
        # 检查依赖
        & $pythonPath -m pip install requests python-dotenv openai anthropic -q
        
        & $pythonPath phi_test_uncensored.py
    }
    "5" {
        Write-Host ""
        Write-Host "运行完整测试套件..." -ForegroundColor Yellow
        Write-Host ""
        $pythonPath = "$packageDir\runtime\python.exe"
        
        # 检查依赖
        & $pythonPath -m pip install requests python-dotenv -q
        
        Write-Host "1. 验证 API Key..." -ForegroundColor Cyan
        & $pythonPath verify_api.py
        Write-Host ""
        
        Write-Host "2. 运行无过滤测试..." -ForegroundColor Cyan
        & $pythonPath phi_test_uncensored.py
        Write-Host ""
        
        Write-Host "3. 运行 MissAV 对接测试..." -ForegroundColor Cyan
        & $pythonPath test_client.py --test all
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

