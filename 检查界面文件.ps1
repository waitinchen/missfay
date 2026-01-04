# 检查界面文件

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  检查心菲对话界面文件" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$staticDir = "static"
$chatFile = "static\phi_chat.html"
$indexFile = "static\index.html"

Write-Host "检查目录和文件..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path $staticDir) {
    Write-Host "  [OK] static 目录存在" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] static 目录不存在" -ForegroundColor Red
    New-Item -ItemType Directory -Path $staticDir | Out-Null
    Write-Host "  [OK] 已创建 static 目录" -ForegroundColor Green
}

Write-Host ""

if (Test-Path $chatFile) {
    $fileInfo = Get-Item $chatFile
    Write-Host "  [OK] phi_chat.html 存在" -ForegroundColor Green
    Write-Host "    大小: $($fileInfo.Length) 字节" -ForegroundColor Gray
    Write-Host "    路径: $($fileInfo.FullName)" -ForegroundColor Gray
} else {
    Write-Host "  [FAIL] phi_chat.html 不存在" -ForegroundColor Red
}

Write-Host ""

if (Test-Path $indexFile) {
    $fileInfo = Get-Item $indexFile
    Write-Host "  [OK] index.html 存在" -ForegroundColor Green
    Write-Host "    大小: $($fileInfo.Length) 字节" -ForegroundColor Gray
} else {
    Write-Host "  [WARN] index.html 不存在" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  重要提示" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "如果文件存在但仍显示 JSON，请:" -ForegroundColor Yellow
Write-Host "  1. 停止 Voice Bridge 服务 (Ctrl+C)" -ForegroundColor White
Write-Host "  2. 重新启动: .\start_voice_bridge.ps1" -ForegroundColor White
Write-Host "  3. 访问: http://localhost:8000/" -ForegroundColor White
Write-Host ""




