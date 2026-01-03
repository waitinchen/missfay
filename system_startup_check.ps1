# Phi 系统启动检查脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Phi 系统启动检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$allReady = $true

# 1. 检查解压目录
Write-Host "1. 检查解压目录..." -ForegroundColor Yellow
if (Test-Path $packageDir) {
    Write-Host "   ✓ 解压目录存在" -ForegroundColor Green
} else {
    Write-Host "   ❌ 解压目录不存在" -ForegroundColor Red
    $allReady = $false
}

# 2. 检查关键文件
Write-Host ""
Write-Host "2. 检查关键文件..." -ForegroundColor Yellow
$keyFiles = @(
    "$packageDir\go-webui.bat",
    "$packageDir\webui.py",
    "$packageDir\runtime\python.exe"
)

foreach ($file in $keyFiles) {
    if (Test-Path $file) {
        Write-Host "   ✓ $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $(Split-Path $file -Leaf) (缺失)" -ForegroundColor Red
        $allReady = $false
    }
}

# 3. 检查预训练模型
Write-Host ""
Write-Host "3. 检查预训练模型..." -ForegroundColor Yellow
$modelDir = "$packageDir\GPT_SoVITS\pretrained_models"
if (Test-Path $modelDir) {
    $modelFiles = Get-ChildItem $modelDir -Recurse -File | Measure-Object
    Write-Host "   ✓ 预训练模型目录存在" -ForegroundColor Green
    Write-Host "   ✓ 模型文件数量: $($modelFiles.Count)" -ForegroundColor Green
} else {
    Write-Host "   ⚠ 预训练模型目录不存在" -ForegroundColor Yellow
}

# 4. 检查 Phi 系统文件
Write-Host ""
Write-Host "4. 检查 Phi 系统文件..." -ForegroundColor Yellow
$phiFiles = @(
    "phi_brain.py",
    "voice_bridge.py",
    "test_client.py",
    "verify_api.py"
)

foreach ($file in $phiFiles) {
    if (Test-Path $file) {
        Write-Host "   ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file (缺失)" -ForegroundColor Red
        $allReady = $false
    }
}

# 5. 检查 .env 配置
Write-Host ""
Write-Host "5. 检查配置文件..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✓ .env 文件存在" -ForegroundColor Green
    
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENROUTER_API_KEY=sk-or-") {
        Write-Host "   ✓ OpenRouter API Key 已配置" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ OpenRouter API Key 未配置" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠ .env 文件不存在（可运行配置脚本创建）" -ForegroundColor Yellow
}

# 6. 检查 Python 环境
Write-Host ""
Write-Host "6. 检查 Python 环境..." -ForegroundColor Yellow
$pythonPath = "$packageDir\runtime\python.exe"
if (Test-Path $pythonPath) {
    Write-Host "   ✓ Python 已就绪" -ForegroundColor Green
    try {
        $version = & $pythonPath --version 2>&1
        Write-Host "   ✓ $version" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠ 无法获取 Python 版本" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ Python 不存在" -ForegroundColor Red
    $allReady = $false
}

# 总结
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  检查总结" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($allReady) {
    Write-Host "✅ 系统已就绪，可以启动！" -ForegroundColor Green
    Write-Host ""
    Write-Host "下一步操作：" -ForegroundColor Yellow
    Write-Host "1. 启动 GPT-SoVITS: cd `"$packageDir`" ; .\go-webui.bat" -ForegroundColor White
    Write-Host "2. 启动 Voice Bridge: python voice_bridge.py" -ForegroundColor White
    Write-Host "3. 运行测试: python phi_test_uncensored.py" -ForegroundColor White
} else {
    Write-Host "⚠️  部分组件缺失，请检查上述错误" -ForegroundColor Yellow
}

Write-Host ""

