# Check UI Files

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Check Phi Chat Interface Files" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$staticDir = "static"
$chatFile = "static\phi_chat.html"
$indexFile = "static\index.html"

Write-Host "Checking files..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path $staticDir) {
    Write-Host "  [OK] static directory exists" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] static directory not found" -ForegroundColor Red
    exit 1
}

Write-Host ""

if (Test-Path $chatFile) {
    $fileInfo = Get-Item $chatFile
    Write-Host "  [OK] phi_chat.html exists" -ForegroundColor Green
    Write-Host "    Size: $($fileInfo.Length) bytes" -ForegroundColor Gray
    Write-Host "    Path: $($fileInfo.FullName)" -ForegroundColor Gray
} else {
    Write-Host "  [FAIL] phi_chat.html not found" -ForegroundColor Red
    exit 1
}

Write-Host ""

if (Test-Path $indexFile) {
    $fileInfo = Get-Item $indexFile
    Write-Host "  [OK] index.html exists" -ForegroundColor Green
    Write-Host "    Size: $($fileInfo.Length) bytes" -ForegroundColor Gray
} else {
    Write-Host "  [WARN] index.html not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  IMPORTANT: Restart Service!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files exist, but service needs restart:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Stop Voice Bridge service:" -ForegroundColor White
Write-Host "   Press Ctrl+C in the service window" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Restart service:" -ForegroundColor White
Write-Host "   .\start_voice_bridge.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Access interface:" -ForegroundColor White
Write-Host "   http://localhost:8000/" -ForegroundColor Cyan
Write-Host ""
Write-Host "The interface should now load correctly!" -ForegroundColor Green
Write-Host ""




