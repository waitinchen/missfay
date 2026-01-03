# Phi 系统启动脚本 - 启动 Voice Bridge 和大脑

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动 Phi 系统 (Voice Bridge)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

# 检查 Python
if (-not (Test-Path $pythonPath)) {
    Write-Host "错误: 未找到 Python" -ForegroundColor Red
    Write-Host "请确保整合包已解压" -ForegroundColor Yellow
    pause
    exit 1
}

# 检查 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "警告: .env 文件不存在，正在创建..." -ForegroundColor Yellow
    @"
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct
GPT_SOVITS_URL=http://127.0.0.1:9880
GPT_SOVITS_API_VERSION=v2
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✓ .env 文件已创建" -ForegroundColor Green
    Write-Host ""
}

# 检查 GPT-SoVITS 服务
Write-Host "检查 GPT-SoVITS 服务状态..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "✓ GPT-SoVITS 服务运行中" -ForegroundColor Green
} catch {
    Write-Host "⚠ GPT-SoVITS 服务未启动" -ForegroundColor Yellow
    Write-Host "  请先启动 GPT-SoVITS (运行 go-webui.bat 或 api_v2.py)" -ForegroundColor Gray
    Write-Host ""
    $continue = Read-Host "是否继续启动 Voice Bridge? (Y/N)"
    if ($continue -ne "Y" -and $continue -ne "y") {
        exit 0
    }
}

Write-Host ""

# 安装依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
& $pythonPath -m pip install fastapi uvicorn httpx pydantic python-dotenv requests -q 2>&1 | Out-Null
Write-Host "✓ 依赖检查完成" -ForegroundColor Green
Write-Host ""

# 设置环境变量
$env:GPT_SOVITS_URL = "http://127.0.0.1:9880"
$env:GPT_SOVITS_API_VERSION = "v2"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动 Voice Bridge 服务" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "服务地址: http://0.0.0.0:8000" -ForegroundColor White
Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动服务
& $pythonPath voice_bridge.py
