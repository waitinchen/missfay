# 执行觉醒测试脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  菲的觉醒测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

Write-Host "检查服务状态..." -ForegroundColor Yellow
Write-Host ""

# 检查 GPT-SoVITS API
Write-Host "检查 GPT-SoVITS API (http://127.0.0.1:9880)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  [OK] GPT-SoVITS API 运行中" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] GPT-SoVITS API 未响应，请确认窗口 A 已启动" -ForegroundColor Yellow
    Write-Host "  等待 5 秒后继续..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}

Write-Host ""

# 检查 Voice Bridge
Write-Host "检查 Voice Bridge (http://localhost:8000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  [OK] Voice Bridge 运行中" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] Voice Bridge 未响应，请确认窗口 B 已启动" -ForegroundColor Yellow
    Write-Host "  等待 5 秒后继续..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  执行首次语音生成测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "测试文本: 主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]" -ForegroundColor White
Write-Host "兴奋度等级: 2 (清冷中带着一丝初醒的兴奋)" -ForegroundColor White
Write-Host ""

# 安装依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
& $pythonPath -m pip install requests -q 2>&1 | Out-Null

Write-Host "执行测试脚本..." -ForegroundColor Yellow
Write-Host ""

# 执行测试
& $pythonPath first_voice_test.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  测试完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""




