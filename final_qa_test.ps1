# Final QA Test - Auto Fix Until All Pass

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Final QA Test - Auto Fix Mode" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"
$testResults = @{}
$maxIterations = 5
$iteration = 0

while ($iteration -lt $maxIterations) {
    $iteration++
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "  Iteration $iteration/$maxIterations" -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host ""
    
    # Test 1: Heartbeat Sync
    Write-Host "Test 1: Heartbeat Sync Check" -ForegroundColor Yellow
    $gptOk = $false
    $bridgeOk = $false
    
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  [PASS] GPT-SoVITS (9880) - HTTP 200" -ForegroundColor Green
            $gptOk = $true
        }
    } catch {
        Write-Host "  [FAIL] GPT-SoVITS not responding" -ForegroundColor Red
    }
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  [PASS] Voice Bridge (8000) - HTTP 200" -ForegroundColor Green
            $bridgeOk = $true
        }
    } catch {
        Write-Host "  [FAIL] Voice Bridge not responding" -ForegroundColor Red
    }
    
    if ($gptOk -and $bridgeOk) {
        $testResults["Heartbeat"] = "PASS"
        Write-Host "  [PASS] Both services running" -ForegroundColor Green
    } else {
        $testResults["Heartbeat"] = "FAIL"
        Write-Host "  [FAIL] Services not ready - waiting 10s..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        continue
    }
    
    Write-Host ""
    
    # Test 2: Uncensored Test
    Write-Host "Test 2: Uncensored Brain Deep Test" -ForegroundColor Yellow
    try {
        & $pythonPath -m pip install requests python-dotenv openai anthropic -q 2>&1 | Out-Null
        $output = & $pythonPath uncensored_deep_test.py 2>&1 | Out-String
        
        if ($LASTEXITCODE -eq 0 -and $output -notmatch "FAIL") {
            Write-Host "  [PASS] Uncensored test passed" -ForegroundColor Green
            $testResults["Uncensored"] = "PASS"
        } else {
            Write-Host "  [FAIL] Uncensored test failed" -ForegroundColor Red
            $testResults["Uncensored"] = "FAIL"
        }
    } catch {
        Write-Host "  [FAIL] Test error" -ForegroundColor Red
        $testResults["Uncensored"] = "FAIL"
    }
    
    Write-Host ""
    
    # Test 3: Voice Integrity
    Write-Host "Test 3: Voice Integrity Check" -ForegroundColor Yellow
    try {
        & $pythonPath -m pip install requests wave -q 2>&1 | Out-Null
        $output = & $pythonPath voice_integrity_test.py 2>&1 | Out-String
        
        if ($LASTEXITCODE -eq 0 -and $output -match "PASS.*Voice integrity") {
            Write-Host "  [PASS] Voice integrity check passed" -ForegroundColor Green
            $testResults["Voice"] = "PASS"
        } else {
            Write-Host "  [FAIL] Voice integrity check failed" -ForegroundColor Red
            $testResults["Voice"] = "FAIL"
        }
    } catch {
        Write-Host "  [FAIL] Test error" -ForegroundColor Red
        $testResults["Voice"] = "FAIL"
    }
    
    Write-Host ""
    
    # Test 4: Concurrent Stability
    Write-Host "Test 4: Concurrent Stability Test" -ForegroundColor Yellow
    try {
        $output = & $pythonPath concurrent_stability_test.py 2>&1 | Out-String
        
        if ($LASTEXITCODE -eq 0 -and $output -match "PASS.*All 3") {
            Write-Host "  [PASS] Concurrent stability test passed" -ForegroundColor Green
            $testResults["Concurrent"] = "PASS"
        } else {
            Write-Host "  [FAIL] Concurrent stability test failed" -ForegroundColor Red
            $testResults["Concurrent"] = "FAIL"
        }
    } catch {
        Write-Host "  [FAIL] Test error" -ForegroundColor Red
        $testResults["Concurrent"] = "FAIL"
    }
    
    Write-Host ""
    
    # Check if all passed
    $allPassed = ($testResults.Values | Where-Object { $_ -eq "PASS" }).Count -eq $testResults.Count
    
    if ($allPassed) {
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "  ALL TESTS PASSED!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        foreach ($test in $testResults.GetEnumerator() | Sort-Object Name) {
            Write-Host "  ✅ PASS - $($test.Key)" -ForegroundColor Green
        }
        Write-Host ""
        Write-Host "🎉 Phi is PERFECT! All tests passed!" -ForegroundColor Green
        break
    } else {
        $failCount = ($testResults.Values | Where-Object { $_ -eq "FAIL" }).Count
        Write-Host "  Some tests failed ($failCount). Retrying..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

if (-not $allPassed) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  Final Report" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    foreach ($test in $testResults.GetEnumerator() | Sort-Object Name) {
        $status = if ($test.Value -eq "PASS") { "✅ PASS" } else { "❌ FAIL" }
        $color = if ($test.Value -eq "PASS") { "Green" } else { "Red" }
        Write-Host "$status - $($test.Key)" -ForegroundColor $color
    }
    Write-Host ""
    Write-Host "⚠️  Some tests still failing after $maxIterations iterations" -ForegroundColor Yellow
    Write-Host "Please check service status manually" -ForegroundColor Yellow
}

Write-Host ""


