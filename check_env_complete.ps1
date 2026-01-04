# 菲菲 401 错误紧急恢复检查脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  菲菲 401 错误紧急恢复检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$envPath = "C:\Users\waiti\missfay\.env"
$baseDir = "C:\Users\waiti\missfay"

# 1. 检查 .env 文件
Write-Host "1. 检查 .env 文件..." -ForegroundColor Yellow
if (Test-Path $envPath) {
    Write-Host "  [OK] .env 文件存在: $envPath" -ForegroundColor Green
    
    $content = Get-Content $envPath -Raw
    $hasOpenRouter = $content -match "OPENROUTER_API_KEY\s*=\s*[^\s]"
    $hasCartesia = $content -match "CARTESIA_API_KEY\s*=\s*[^\s]"
    
    if ($hasOpenRouter) {
        Write-Host "  [OK] OPENROUTER_API_KEY 已配置" -ForegroundColor Green
    } else {
        Write-Host "  [X] OPENROUTER_API_KEY 未配置或为空" -ForegroundColor Red
    }
    
    if ($hasCartesia) {
        Write-Host "  [OK] CARTESIA_API_KEY 已配置" -ForegroundColor Green
    } else {
        Write-Host "  [!] CARTESIA_API_KEY 未配置（可选）" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [X] .env 文件不存在: $envPath" -ForegroundColor Red
    Write-Host "  请创建 .env 文件并配置 API Key" -ForegroundColor Yellow
}
Write-Host ""

# 2. 检查 voice_bridge.py 的 load_dotenv
Write-Host "2. 检查 voice_bridge.py 的 load_dotenv..." -ForegroundColor Yellow
$voiceBridgePath = Join-Path $baseDir "voice_bridge.py"
if (Test-Path $voiceBridgePath) {
    $bridgeContent = Get-Content $voiceBridgePath -Raw
    if ($bridgeContent -match "load_dotenv") {
        Write-Host "  [OK] voice_bridge.py 包含 load_dotenv" -ForegroundColor Green
    } else {
        Write-Host "  [X] voice_bridge.py 未找到 load_dotenv" -ForegroundColor Red
    }
} else {
    Write-Host "  [X] voice_bridge.py 文件不存在" -ForegroundColor Red
}
Write-Host ""

# 3. 检查端口配置
Write-Host "3. 检查端口配置..." -ForegroundColor Yellow
Write-Host "  Voice Bridge (voice_bridge.py): 端口 8000" -ForegroundColor White
Write-Host "  Proxy Layer (phi_proxy_layer.py): 端口 8001" -ForegroundColor White
Write-Host "  GPT-SoVITS: 端口 9880" -ForegroundColor White
Write-Host ""

# 4. 检查运行中的进程
Write-Host "4. 检查运行中的服务..." -ForegroundColor Yellow
$pythonProcesses = Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Select-Object ProcessName, Id
if ($pythonProcesses) {
    Write-Host "  找到 $($pythonProcesses.Count) 个 Python 进程" -ForegroundColor Cyan
    $pythonProcesses | ForEach-Object { Write-Host "    - PID: $($_.Id)" -ForegroundColor White }
    Write-Host "  建议：关闭所有进程后重新启动" -ForegroundColor Yellow
} else {
    Write-Host "  [OK] 没有运行中的 Python 进程" -ForegroundColor Green
}
Write-Host ""

# 5. 生成重启指令
Write-Host "5. 重启服务顺序建议：" -ForegroundColor Yellow
Write-Host "  步骤 1: 关闭所有运行中的终端窗口" -ForegroundColor White
Write-Host "  步骤 2: 启动 GPT-SoVITS (端口 9880)" -ForegroundColor White
Write-Host "  步骤 3: 启动 Voice Bridge (端口 8000)" -ForegroundColor White
Write-Host "  步骤 4: （可选）启动 Proxy Layer (端口 8001)" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  检查完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan


