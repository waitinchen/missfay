# 更新 .env 文件中的 GEMINI_API_KEY

$envFile = ".env"
$newKey = "AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo"

Write-Host "更新 GEMINI_API_KEY..." -ForegroundColor Cyan

if (Test-Path $envFile) {
    # 读取现有内容
    $content = Get-Content $envFile -Raw
    
    # 检查是否已有 GEMINI_API_KEY
    if ($content -match "GEMINI_API_KEY\s*=") {
        # 替换现有的 Key
        $content = $content -replace "GEMINI_API_KEY\s*=.*", "GEMINI_API_KEY=$newKey"
        Write-Host "[OK] 已更新现有的 GEMINI_API_KEY" -ForegroundColor Green
    } else {
        # 添加新的 Key
        $content += "`nGEMINI_API_KEY=$newKey`n"
        Write-Host "[OK] 已添加 GEMINI_API_KEY" -ForegroundColor Green
    }
    
    # 确保有 GEMINI_MODEL
    if ($content -notmatch "GEMINI_MODEL\s*=") {
        $content += "GEMINI_MODEL=gemini-2.0-flash-exp`n"
        Write-Host "[OK] 已添加 GEMINI_MODEL" -ForegroundColor Green
    }
    
    # 写入文件
    $content | Set-Content $envFile -Encoding UTF8
    Write-Host "[OK] .env 文件已更新" -ForegroundColor Green
} else {
    # 创建新文件
    @"
GEMINI_API_KEY=$newKey
GEMINI_MODEL=gemini-2.0-flash-exp
"@ | Set-Content $envFile -Encoding UTF8
    Write-Host "[OK] 已创建 .env 文件" -ForegroundColor Green
}

Write-Host ""
Write-Host "GEMINI_API_KEY 已设置为: $($newKey.Substring(0,10))...$($newKey.Substring($newKey.Length-5))" -ForegroundColor Cyan
Write-Host ""
Write-Host "现在可以启动服务了:" -ForegroundColor Yellow
Write-Host "  .\start_voice_bridge.ps1" -ForegroundColor White

