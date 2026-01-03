# Test UI Access

Write-Host "Checking UI files..." -ForegroundColor Yellow

$indexPath = "static\index.html"
if (Test-Path $indexPath) {
    $fileSize = (Get-Item $indexPath).Length
    Write-Host "  [OK] index.html exists ($fileSize bytes)" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] index.html not found" -ForegroundColor Red
    Write-Host "  Creating index.html..." -ForegroundColor Yellow
    
    # Create directory if needed
    if (-not (Test-Path "static")) {
        New-Item -ItemType Directory -Path "static" | Out-Null
    }
}

Write-Host ""
Write-Host "Testing URL access..." -ForegroundColor Yellow
Write-Host "  Open: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Or: http://localhost:8000/static/index.html" -ForegroundColor Cyan
Write-Host ""


