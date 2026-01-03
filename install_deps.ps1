# 安装 Phi 系统依赖脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  安装 Phi 系统依赖" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 环境
$pythonPath = $null

# 尝试使用整合包的 Python
$packagePython = ".\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\runtime\python.exe"
if (Test-Path $packagePython) {
    $pythonPath = $packagePython
    Write-Host "✓ 找到整合包 Python: $packagePython" -ForegroundColor Green
} else {
    # 尝试系统 Python
    try {
        $pythonVersion = python --version 2>&1
        $pythonPath = "python"
        Write-Host "✓ 找到系统 Python: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ 未找到 Python 环境" -ForegroundColor Red
        Write-Host "   请确保已安装 Python 或解压整合包" -ForegroundColor Yellow
        exit 1
    }
}

# 检查 pip
Write-Host ""
Write-Host "检查 pip..." -ForegroundColor Yellow
try {
    & $pythonPath -m pip --version | Out-Null
    Write-Host "✓ pip 可用" -ForegroundColor Green
} catch {
    Write-Host "❌ pip 不可用" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host ""
Write-Host "安装依赖包..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟，请耐心等待..." -ForegroundColor Gray
Write-Host ""

& $pythonPath -m pip install -r requirements_phi.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ 依赖安装完成！" -ForegroundColor Green
    Write-Host ""
    Write-Host "下一步：" -ForegroundColor Yellow
    Write-Host "1. 复制 .env.example 为 .env 并填入 API 密钥" -ForegroundColor White
    Write-Host "2. 启动 GPT-SoVITS 服务" -ForegroundColor White
    Write-Host "3. 运行 .\启动Phi系统.ps1" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ 依赖安装失败，请检查错误信息" -ForegroundColor Red
    exit 1
}

