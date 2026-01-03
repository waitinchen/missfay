# 快速验证 OpenRouter API Key

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  验证 OpenRouter API Key" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "警告: .env 文件不存在" -ForegroundColor Yellow
    Write-Host "正在运行配置脚本..." -ForegroundColor Yellow
    .\配置OpenRouter.ps1
    Write-Host ""
}

# 检查 API Key
$envContent = Get-Content ".env" -Raw -ErrorAction SilentlyContinue
if ($envContent -match "OPENROUTER_API_KEY=(.+)") {
    $apiKey = $matches[1].Trim()
    Write-Host "找到 API Key: $($apiKey.Substring(0, [Math]::Min(20, $apiKey.Length)))...$($apiKey.Substring([Math]::Max(0, $apiKey.Length - 10)))" -ForegroundColor Green
} else {
    Write-Host "错误: 未找到 OPENROUTER_API_KEY" -ForegroundColor Red
    Write-Host "请运行 .\配置OpenRouter.ps1 配置 API Key" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "查找 Python 环境..." -ForegroundColor Yellow

# 尝试使用整合包的 Python
$packagePython = ".\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\runtime\python.exe"
if (Test-Path $packagePython) {
    Write-Host "使用整合包 Python" -ForegroundColor Green
    Write-Host ""
    Write-Host "运行验证脚本..." -ForegroundColor Yellow
    & $packagePython check_openrouter.py
} else {
    # 尝试系统 Python
    try {
        python --version | Out-Null
        Write-Host "使用系统 Python" -ForegroundColor Green
        Write-Host ""
        Write-Host "运行验证脚本..." -ForegroundColor Yellow
        python check_openrouter.py
    } catch {
        Write-Host "错误: 未找到 Python 环境" -ForegroundColor Red
        Write-Host "请确保已安装 Python 或解压整合包" -ForegroundColor Yellow
        exit 1
    }
}

