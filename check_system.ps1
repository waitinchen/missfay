# Phi System Check Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Phi System Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$allReady = $true

# 1. Check extraction directory
Write-Host "1. Checking extraction directory..." -ForegroundColor Yellow
if (Test-Path $packageDir) {
    Write-Host "   [OK] Directory exists" -ForegroundColor Green
} else {
    Write-Host "   [FAIL] Directory not found" -ForegroundColor Red
    $allReady = $false
}

# 2. Check key files
Write-Host ""
Write-Host "2. Checking key files..." -ForegroundColor Yellow
$keyFiles = @(
    "$packageDir\go-webui.bat",
    "$packageDir\webui.py",
    "$packageDir\runtime\python.exe",
    "$packageDir\api_v2.py"
)

foreach ($file in $keyFiles) {
    $fileName = Split-Path $file -Leaf
    if (Test-Path $file) {
        Write-Host "   [OK] $fileName" -ForegroundColor Green
    } else {
        Write-Host "   [FAIL] $fileName (missing)" -ForegroundColor Red
        $allReady = $false
    }
}

# 3. Check pretrained models
Write-Host ""
Write-Host "3. Checking pretrained models..." -ForegroundColor Yellow
$modelDir = "$packageDir\GPT_SoVITS\pretrained_models"
if (Test-Path $modelDir) {
    $modelFiles = Get-ChildItem $modelDir -Recurse -File -ErrorAction SilentlyContinue | Measure-Object
    Write-Host "   [OK] Model directory exists" -ForegroundColor Green
    Write-Host "   [OK] Model files: $($modelFiles.Count)" -ForegroundColor Green
} else {
    Write-Host "   [WARN] Model directory not found" -ForegroundColor Yellow
}

# 4. Check Phi system files
Write-Host ""
Write-Host "4. Checking Phi system files..." -ForegroundColor Yellow
$phiFiles = @(
    "phi_brain.py",
    "voice_bridge.py",
    "test_client.py",
    "verify_api.py"
)

foreach ($file in $phiFiles) {
    if (Test-Path $file) {
        Write-Host "   [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "   [FAIL] $file (missing)" -ForegroundColor Red
        $allReady = $false
    }
}

# 5. Check .env configuration
Write-Host ""
Write-Host "5. Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   [OK] .env file exists" -ForegroundColor Green
    
    $envContent = Get-Content ".env" -Raw -ErrorAction SilentlyContinue
    if ($envContent -match "OPENROUTER_API_KEY=sk-or-") {
        Write-Host "   [OK] OpenRouter API Key configured" -ForegroundColor Green
    } else {
        Write-Host "   [WARN] OpenRouter API Key not configured" -ForegroundColor Yellow
    }
} else {
    Write-Host "   [WARN] .env file not found" -ForegroundColor Yellow
}

# 6. Check Python environment
Write-Host ""
Write-Host "6. Checking Python environment..." -ForegroundColor Yellow
$pythonPath = "$packageDir\runtime\python.exe"
if (Test-Path $pythonPath) {
    Write-Host "   [OK] Python ready" -ForegroundColor Green
    try {
        $version = & $pythonPath --version 2>&1
        Write-Host "   [OK] $version" -ForegroundColor Green
    } catch {
        Write-Host "   [WARN] Cannot get Python version" -ForegroundColor Yellow
    }
} else {
    Write-Host "   [FAIL] Python not found" -ForegroundColor Red
    $allReady = $false
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($allReady) {
    Write-Host "[SUCCESS] System is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Start GPT-SoVITS: cd `"$packageDir`" ; .\go-webui.bat" -ForegroundColor White
    Write-Host "2. Start Voice Bridge: python voice_bridge.py" -ForegroundColor White
    Write-Host "3. Run tests: python phi_test_uncensored.py" -ForegroundColor White
} else {
    Write-Host "[WARN] Some components are missing" -ForegroundColor Yellow
}

Write-Host ""



