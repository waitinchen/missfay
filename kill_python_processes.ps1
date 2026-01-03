# 强制关闭所有 Python 进程（修复残留进程问题）
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  强制关闭所有 Python 进程" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 查找所有 Python 进程
$pythonProcesses = Get-Process -Name python -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "找到 $($pythonProcesses.Count) 个 Python 进程:" -ForegroundColor Yellow
    foreach ($proc in $pythonProcesses) {
        Write-Host "  - PID: $($proc.Id), 名称: $($proc.ProcessName), 路径: $($proc.Path)" -ForegroundColor Gray
    }
    Write-Host ""
    
    # 强制关闭
    Write-Host "正在强制关闭..." -ForegroundColor Yellow
    Stop-Process -Name python -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] 所有 Python 进程已关闭" -ForegroundColor Green
} else {
    Write-Host "[OK] 没有找到运行中的 Python 进程" -ForegroundColor Green
}

Write-Host ""
Write-Host "检查端口占用..." -ForegroundColor Yellow
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
$port9880 = Get-NetTCPConnection -LocalPort 9880 -ErrorAction SilentlyContinue

if ($port8000) {
    Write-Host "[!] 端口 8000 仍被占用" -ForegroundColor Red
} else {
    Write-Host "[OK] 端口 8000 已释放" -ForegroundColor Green
}

if ($port9880) {
    Write-Host "[!] 端口 9880 仍被占用" -ForegroundColor Red
} else {
    Write-Host "[OK] 端口 9880 已释放" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  完成" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "现在可以重新启动服务:" -ForegroundColor Yellow
Write-Host "  .\start_voice_bridge.ps1" -ForegroundColor White
Write-Host ""

