# 快速启动 Voice Bridge 服务

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动 Phi Voice Bridge 服务" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

# 检查 Python
if (-not (Test-Path $pythonPath)) {
    Write-Host "❌ Python 未找到: $pythonPath" -ForegroundColor Red
    Write-Host "尝试使用系统 Python..." -ForegroundColor Yellow
    
    # 尝试使用系统 Python
    $pythonPath = "python"
    try {
        $version = & python --version 2>&1
        Write-Host "✅ 找到系统 Python: $version" -ForegroundColor Green
    } catch {
        Write-Host "❌ 系统 Python 也未找到，请安装 Python 3.11+" -ForegroundColor Red
        pause
        exit 1
    }
} else {
    Write-Host "✅ Python 路径: $pythonPath" -ForegroundColor Green
}

# 检查 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env 文件不存在" -ForegroundColor Yellow
    Write-Host "   请确保已设置 GEMINI_API_KEY 和 CARTESIA_API_KEY" -ForegroundColor Yellow
    Write-Host ""
}

# 检查依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
& $pythonPath -m pip install fastapi uvicorn httpx pydantic python-dotenv requests google-generativeai cartesia -q 2>&1 | Out-Null
Write-Host "✅ 依赖检查完成" -ForegroundColor Green
Write-Host ""

# 启动服务
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动服务中..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 服务地址: http://localhost:8000" -ForegroundColor White
Write-Host "📚 API 文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host "💬 聊天界面: http://localhost:8000/" -ForegroundColor White
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 切换到项目目录
Set-Location "C:\Users\waiti\missfay"

# 启动服务
& $pythonPath voice_bridge.py

