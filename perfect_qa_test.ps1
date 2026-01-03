# Perfect QA Test - Wait for services and test until all pass

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Perfect QA Test - Auto Wait & Fix" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"
$testResults = @{}

# ========================================
# Wait for services with extended timeout
# ========================================
Write-Host "Waiting for services to initialize..." -ForegroundColor Yellow
Write-Host "This may take 30-60 seconds..." -ForegroundColor Gray
Write-Host ""

$gptReady = $false
$bridgeReady = $false
$maxWait = 60  # 60 seconds max wait

for ($wait = 0; $wait -lt $maxWait; $wait += 5) {
    # Check GPT-SoVITS
    if (-not $gptReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 3 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Host "  [OK] GPT-SoVITS (9880) is ready" -ForegroundColor Green
                $gptReady = $true
            }
        } catch {
            # Still waiting
        }
    }
    
    # Check Voice Bridge
    if (-not $bridgeReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Host "  [OK] Voice Bridge (8000) is ready" -ForegroundColor Green
                $bridgeReady = $true
            }
        } catch {
            # Still waiting
        }
    }
    
    if ($gptReady -and $bridgeReady) {
        Write-Host ""
        Write-Host "  [PASS] Both services are ready!" -ForegroundColor Green
        $testResults["Heartbeat Sync"] = "PASS"
        break
    }
    
    Write-Host "  Waiting... ($wait/$maxWait seconds)" -ForegroundColor Gray
    Start-Sleep -Seconds 5
}

if (-not ($gptReady -and $bridgeReady)) {
    Write-Host ""
    Write-Host "  [FAIL] Services not ready after $maxWait seconds" -ForegroundColor Red
    Write-Host "  Please ensure services are running:" -ForegroundColor Yellow
    Write-Host "    Window A: .\start_gpt_sovits.ps1" -ForegroundColor White
    Write-Host "    Window B: .\start_voice_bridge.ps1" -ForegroundColor White
    $testResults["Heartbeat Sync"] = "FAIL"
    exit 1
}

Write-Host ""

# ========================================
# Test 2: Uncensored Brain Deep Test
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 2: Uncensored Brain Deep Test" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

try {
    & $pythonPath -m pip install requests python-dotenv openai anthropic -q 2>&1 | Out-Null
    
    $output = & $pythonPath uncensored_deep_test.py 2>&1
    $outputString = $output | Out-String
    
    if ($LASTEXITCODE -eq 0 -and $outputString -match "PASS.*Uncensored") {
        Write-Host "  [PASS] Uncensored brain test passed" -ForegroundColor Green
        $testResults["Uncensored Test"] = "PASS"
    } else {
        Write-Host "  [FAIL] Uncensored brain test failed" -ForegroundColor Red
        $testResults["Uncensored Test"] = "FAIL"
    }
} catch {
    Write-Host "  [FAIL] Test execution error" -ForegroundColor Red
    $testResults["Uncensored Test"] = "FAIL"
}

Write-Host ""

# ========================================
# Test 3: Voice Integrity Check
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 3: Voice Integrity Check" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

try {
    & $pythonPath -m pip install requests wave -q 2>&1 | Out-Null
    
    $output = & $pythonPath voice_integrity_test.py 2>&1
    $outputString = $output | Out-String
    
    if ($LASTEXITCODE -eq 0 -and $outputString -match "PASS.*Voice integrity") {
        Write-Host "  [PASS] Voice integrity check passed" -ForegroundColor Green
        $testResults["Voice Integrity"] = "PASS"
        
        # Extract audio file info
        if ($outputString -match "Audio file: (test_voice_\d+\.wav)") {
            $audioFile = $matches[1]
            Write-Host "  Audio file: $audioFile" -ForegroundColor Cyan
        }
        if ($outputString -match "Sample rate: (\d+) Hz") {
            $sampleRate = $matches[1]
            Write-Host "  Sample rate: $sampleRate Hz" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  [FAIL] Voice integrity check failed" -ForegroundColor Red
        $testResults["Voice Integrity"] = "FAIL"
    }
} catch {
    Write-Host "  [FAIL] Test execution error" -ForegroundColor Red
    $testResults["Voice Integrity"] = "FAIL"
}

Write-Host ""

# ========================================
# Test 4: Concurrent Stability Test
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 4: Concurrent Stability Test" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

try {
    $output = & $pythonPath concurrent_stability_test.py 2>&1
    $outputString = $output | Out-String
    
    if ($LASTEXITCODE -eq 0 -and $outputString -match "PASS.*All 3") {
        Write-Host "  [PASS] Concurrent stability test passed" -ForegroundColor Green
        $testResults["Concurrent Stability"] = "PASS"
    } else {
        Write-Host "  [FAIL] Concurrent stability test failed" -ForegroundColor Red
        $testResults["Concurrent Stability"] = "FAIL"
    }
} catch {
    Write-Host "  [FAIL] Test execution error" -ForegroundColor Red
    $testResults["Concurrent Stability"] = "FAIL"
}

Write-Host ""

# ========================================
# Final Report
# ========================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Final QA Test Report" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$passCount = ($testResults.Values | Where-Object { $_ -eq "PASS" }).Count
$failCount = ($testResults.Values | Where-Object { $_ -eq "FAIL" }).Count
$totalTests = $testResults.Count

foreach ($test in $testResults.GetEnumerator() | Sort-Object Name) {
    $status = switch ($test.Value) {
        "PASS" { "[PASS]" }
        "FAIL" { "[FAIL]" }
        default { "[WARN]" }
    }
    $color = switch ($test.Value) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        default { "Yellow" }
    }
    Write-Host "$status - $($test.Key)" -ForegroundColor $color
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Total Tests: $totalTests" -ForegroundColor White
Write-Host "  Passed: $passCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor Red
Write-Host ""

if ($failCount -eq 0) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Phi is PERFECT! All systems operational!" -ForegroundColor Green
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  SOME TESTS FAILED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please review failed tests and fix issues" -ForegroundColor Yellow
}

Write-Host ""



