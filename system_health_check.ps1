# Phi 系统健康检查脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Phi 系统健康检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allHealthy = $true

# 1. 检查 Python 环境
Write-Host "1. 检查 Python 环境..." -ForegroundColor Yellow
$pythonPath = $null

$packagePython = ".\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\runtime\python.exe"
if (Test-Path $packagePython) {
    $pythonPath = $packagePython
    Write-Host "   ✓ 整合包 Python 可用" -ForegroundColor Green
} else {
    try {
        python --version | Out-Null
        $pythonPath = "python"
        Write-Host "   ✓ 系统 Python 可用" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Python 不可用" -ForegroundColor Red
        $allHealthy = $false
    }
}

# 2. 检查依赖包
Write-Host ""
Write-Host "2. 检查依赖包..." -ForegroundColor Yellow
$requiredPackages = @("fastapi", "uvicorn", "httpx", "pydantic", "openai", "anthropic", "requests")

foreach ($package in $requiredPackages) {
    try {
        & $pythonPath -c "import $package" 2>&1 | Out-Null
        Write-Host "   ✓ $package" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ $package (未安装)" -ForegroundColor Red
        $allHealthy = $false
    }
}

# 3. 检查核心文件
Write-Host ""
Write-Host "3. 检查核心文件..." -ForegroundColor Yellow
$coreFiles = @(
    "phi_brain.py",
    "voice_bridge.py",
    "test_client.py",
    "requirements_phi.txt",
    ".env.example"
)

foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        Write-Host "   ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file (缺失)" -ForegroundColor Red
        $allHealthy = $false
    }
}

# 4. 检查 .env 文件
Write-Host ""
Write-Host "4. 检查配置文件..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✓ .env 文件存在" -ForegroundColor Green
    
    # 检查是否包含 API 密钥
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENAI_API_KEY=sk-" -or $envContent -match "ANTHROPIC_API_KEY=sk-ant-") {
        Write-Host "   ✓ API 密钥已配置" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ .env 文件存在但未配置 API 密钥" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠ .env 文件不存在（可复制 .env.example 创建）" -ForegroundColor Yellow
}

# 5. 检查 GPT-SoVITS 服务
Write-Host ""
Write-Host "5. 检查 GPT-SoVITS 服务..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "   ✓ GPT-SoVITS 服务运行中" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ GPT-SoVITS 服务未启动（需要先启动服务）" -ForegroundColor Yellow
}

# 6. 检查 Voice Bridge 服务
Write-Host ""
Write-Host "6. 检查 Voice Bridge 服务..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "   ✓ Voice Bridge 服务运行中" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ Voice Bridge 服务未启动（运行 .\启动Phi系统.ps1 启动）" -ForegroundColor Yellow
}

# 总结
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  健康检查总结" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($allHealthy) {
    Write-Host "✅ 核心组件健康" -ForegroundColor Green
    Write-Host ""
    Write-Host "系统已就绪，可以启动服务！" -ForegroundColor Green
} else {
    Write-Host "⚠️  部分组件异常，请检查上述错误" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "建议操作：" -ForegroundColor Yellow
    Write-Host "1. 运行 .\安装依赖.ps1 安装缺失的依赖" -ForegroundColor White
    Write-Host "2. 检查核心文件是否完整" -ForegroundColor White
}

Write-Host ""

