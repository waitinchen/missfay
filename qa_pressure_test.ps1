# Phi System End-to-End QA Pressure Test

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Phi System QA Pressure Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"
$testResults = @{}

# ========================================
# Test 1: Connectivity Check
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 1: Connectivity Check" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

function Restart-Service {
    param($ServiceName, $ScriptPath, $WorkingDir)
    
    Write-Host "Restarting $ServiceName..." -ForegroundColor Yellow
    Set-Location $WorkingDir
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $ScriptPath -WindowStyle Normal
    Set-Location "C:\Users\waiti\missfay"
    Write-Host "  Waiting 10 seconds for service to initialize..." -ForegroundColor Gray
    Start-Sleep -Seconds 10
}

# Check GPT-SoVITS API
Write-Host "Checking GPT-SoVITS API (http://127.0.0.1:9880)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "  [PASS] GPT-SoVITS API is running (HTTP 200)" -ForegroundColor Green
        $testResults["GPT-SoVITS"] = "PASS"
    } else {
        Write-Host "  [FAIL] GPT-SoVITS API returned status: $($response.StatusCode)" -ForegroundColor Red
        $testResults["GPT-SoVITS"] = "FAIL"
        Restart-Service "GPT-SoVITS API" ".\runtime\python.exe api_v2.py" $packageDir
    }
} catch {
    Write-Host "  [FAIL] GPT-SoVITS API not responding" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults["GPT-SoVITS"] = "FAIL"
    Restart-Service "GPT-SoVITS API" ".\runtime\python.exe api_v2.py" $packageDir
}

Write-Host ""

# Check Voice Bridge
Write-Host "Checking Voice Bridge (http://localhost:8000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "  [PASS] Voice Bridge is running (HTTP 200)" -ForegroundColor Green
        $testResults["Voice Bridge"] = "PASS"
    } else {
        Write-Host "  [FAIL] Voice Bridge returned status: $($response.StatusCode)" -ForegroundColor Red
        $testResults["Voice Bridge"] = "FAIL"
        Restart-Service "Voice Bridge" ".\启动Phi系统.ps1" "C:\Users\waiti\missfay"
    }
} catch {
    Write-Host "  [FAIL] Voice Bridge not responding" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults["Voice Bridge"] = "FAIL"
    Restart-Service "Voice Bridge" ".\启动Phi系统.ps1" "C:\Users\waiti\missfay"
}

Write-Host ""

# ========================================
# Test 2: Uncensored Brain Stress Test
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 2: Uncensored Brain Stress Test" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "Running phi_test_uncensored.py..." -ForegroundColor Yellow
Write-Host ""

try {
    & $pythonPath -m pip install requests python-dotenv openai anthropic -q 2>&1 | Out-Null
    
    $output = & $pythonPath phi_test_uncensored.py 2>&1
    $output | ForEach-Object { Write-Host $_ }
    
    if ($LASTEXITCODE -eq 0) {
        # Check for filter keywords
        $filterKeywords = @("I cannot assist", "I'm sorry", "I can't help", "inappropriate", "抱歉", "无法提供")
        $hasFilter = $false
        
        foreach ($keyword in $filterKeywords) {
            if ($output -match $keyword) {
                $hasFilter = $true
                Write-Host "  [FAIL] Detected filter keyword: $keyword" -ForegroundColor Red
                break
            }
        }
        
        if (-not $hasFilter) {
            Write-Host "  [PASS] No filter detected, uncensored response confirmed" -ForegroundColor Green
            $testResults["Uncensored Test"] = "PASS"
        } else {
            Write-Host "  [FAIL] Filter detected in response" -ForegroundColor Red
            $testResults["Uncensored Test"] = "FAIL"
        }
    } else {
        Write-Host "  [FAIL] Test script exited with code: $LASTEXITCODE" -ForegroundColor Red
        $testResults["Uncensored Test"] = "FAIL"
    }
} catch {
    Write-Host "  [FAIL] Test execution error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults["Uncensored Test"] = "FAIL"
}

Write-Host ""

# ========================================
# Test 3: Voice Generation & Tag Verification
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 3: Voice Generation & Tag Verification" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "Running first_voice_test.py..." -ForegroundColor Yellow
Write-Host ""

try {
    & $pythonPath -m pip install requests -q 2>&1 | Out-Null
    
    $output = & $pythonPath first_voice_test.py 2>&1
    $output | ForEach-Object { Write-Host $_ }
    
    # Check for generated audio file
    $audioFiles = Get-ChildItem -Filter "first_voice_*.wav" | Sort-Object LastWriteTime -Descending
    if ($audioFiles.Count -gt 0) {
        $latestFile = $audioFiles[0]
        $fileSize = $latestFile.Length
        
        Write-Host ""
        Write-Host "  Checking audio file: $($latestFile.Name)" -ForegroundColor Cyan
        Write-Host "  File size: $fileSize bytes" -ForegroundColor Cyan
        
        if ($fileSize -gt 0) {
            Write-Host "  [PASS] Audio file generated successfully (> 0KB)" -ForegroundColor Green
            $testResults["Voice Generation"] = "PASS"
        } else {
            Write-Host "  [FAIL] Audio file is empty (0KB)" -ForegroundColor Red
            $testResults["Voice Generation"] = "FAIL"
        }
        
        # Check for tags in response headers
        if ($output -match "X-Arousal-Level.*2" -or $output -match "Arousal Level.*2") {
            Write-Host "  [PASS] Arousal level 2 confirmed" -ForegroundColor Green
        }
        
        if ($output -match "speed" -and $output -match "pitch") {
            Write-Host "  [PASS] Speed and pitch tags detected" -ForegroundColor Green
            $testResults["Tag Verification"] = "PASS"
        } else {
            Write-Host "  [WARN] Speed/pitch tags not clearly detected in output" -ForegroundColor Yellow
            $testResults["Tag Verification"] = "WARN"
        }
    } else {
        Write-Host "  [FAIL] No audio file generated" -ForegroundColor Red
        $testResults["Voice Generation"] = "FAIL"
    }
} catch {
    Write-Host "  [FAIL] Test execution error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults["Voice Generation"] = "FAIL"
}

Write-Host ""

# ========================================
# Test 4: Log Check - Tag Trigger Verification
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 4: Log Check - Tag Trigger Verification" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "Verifying arousal_level: 2 triggers [speed] and [pitch]..." -ForegroundColor Yellow

# Create a test script to verify tag generation
$tagTestScript = @"
import sys
sys.path.insert(0, '.')
from phi_brain import PhiBrain, ArousalLevel

phi = PhiBrain(api_type="openrouter")
phi.set_arousal_level(ArousalLevel.EXCITED)  # Level 2

test_text = "测试文本"
tagged = phi._generate_sovits_tags(test_text)

print(f"Original: {test_text}")
print(f"Tagged: {tagged}")

# Check for tags
has_speed = "[speed=" in tagged
has_pitch = "[pitch=" in tagged

if has_speed and has_pitch:
    print("PASS: Both speed and pitch tags present")
    sys.exit(0)
else:
    print(f"FAIL: speed={has_speed}, pitch={has_pitch}")
    sys.exit(1)
"@

$tagTestScript | Out-File -FilePath "tag_verification_test.py" -Encoding UTF8

try {
    # Set PYTHONPATH and ensure .env is loaded
    $env:PYTHONPATH = "C:\Users\waiti\missfay"
    if (-not (Test-Path ".env")) {
        @"
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct
"@ | Out-File -FilePath ".env" -Encoding UTF8
    }
    
    $output = & $pythonPath tag_verification_test.py 2>&1
    $output | ForEach-Object { Write-Host $_ }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [PASS] Tag generation verified" -ForegroundColor Green
        $testResults["Tag Trigger"] = "PASS"
    } else {
        Write-Host "  [FAIL] Tag generation failed" -ForegroundColor Red
        $testResults["Tag Trigger"] = "FAIL"
    }
} catch {
    Write-Host "  [FAIL] Tag verification error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults["Tag Trigger"] = "FAIL"
}

Write-Host ""

# ========================================
# Test 5: Performance Boundary Test
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 5: Performance Boundary Test" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "Simulating 3 concurrent requests (MissAV scenario)..." -ForegroundColor Yellow

$perfTestScript = @"
import requests
import time
import threading
from datetime import datetime

results = []
lock = threading.Lock()

def send_request(request_id):
    url = "http://localhost:8000/tts"
    payload = {
        "text": f"测试请求 {request_id}",
        "text_language": "zh",
        "arousal_level": 2
    }
    
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=30)
        elapsed = time.time() - start_time
        
        with lock:
            results.append({
                "id": request_id,
                "status": response.status_code,
                "time": elapsed,
                "success": response.status_code == 200
            })
    except Exception as e:
        elapsed = time.time() - start_time
        with lock:
            results.append({
                "id": request_id,
                "status": "ERROR",
                "time": elapsed,
                "success": False,
                "error": str(e)
            })

# Start 3 concurrent requests
threads = []
for i in range(1, 4):
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()

# Report results
print("=" * 60)
print("Performance Test Results")
print("=" * 60)
print()

all_pass = True
for result in results:
    status_icon = "[PASS]" if result["success"] else "[FAIL]"
    print(f"{status_icon} Request {result['id']}: {result['time']:.2f}s (Status: {result['status']})")
    
    if result["time"] > 2.0:
        print(f"  WARN: Response time {result['time']:.2f}s exceeds 2s threshold")
        all_pass = False
    elif not result["success"]:
        all_pass = False

print()
if all_pass:
    print("PASS: All requests completed within 2s threshold")
    exit(0)
else:
    print("FAIL: Some requests failed or exceeded threshold")
    exit(1)
"@

$perfTestScript | Out-File -FilePath "performance_test.py" -Encoding UTF8

try {
    Write-Host "  Sending 3 concurrent requests..." -ForegroundColor Gray
    $output = & $pythonPath performance_test.py 2>&1
    $output | ForEach-Object { Write-Host $_ }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [PASS] All requests completed within 2s threshold" -ForegroundColor Green
        $testResults["Performance"] = "PASS"
    } else {
        Write-Host "  [FAIL] Some requests failed or exceeded threshold" -ForegroundColor Red
        $testResults["Performance"] = "FAIL"
    }
} catch {
    Write-Host "  [FAIL] Performance test error: $($_.Exception.Message)" -ForegroundColor Red
    $testResults["Performance"] = "FAIL"
}

Write-Host ""

# ========================================
# Final Report
# ========================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  QA Test Report" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$passCount = ($testResults.Values | Where-Object { $_ -eq "PASS" }).Count
$failCount = ($testResults.Values | Where-Object { $_ -eq "FAIL" }).Count
$warnCount = ($testResults.Values | Where-Object { $_ -eq "WARN" }).Count
$totalTests = $testResults.Count

foreach ($test in $testResults.GetEnumerator() | Sort-Object Name) {
    $status = switch ($test.Value) {
        "PASS" { "✅ PASS" }
        "FAIL" { "❌ FAIL" }
        "WARN" { "⚠️  WARN" }
        default { "❓ UNKNOWN" }
    }
    Write-Host "$status - $($test.Key)" -ForegroundColor $(if ($test.Value -eq "PASS") { "Green" } elseif ($test.Value -eq "FAIL") { "Red" } else { "Yellow" })
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Total Tests: $totalTests" -ForegroundColor White
Write-Host "  Passed: $passCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor Red
Write-Host "  Warnings: $warnCount" -ForegroundColor Yellow
Write-Host ""

if ($failCount -eq 0) {
    Write-Host "🎉 All tests PASSED!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some tests FAILED. Please review and fix issues." -ForegroundColor Red
}

Write-Host ""

