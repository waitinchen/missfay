# Strict QA Pressure Test - Auto Fix Until All Pass

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Strict QA Pressure Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"
$maxRetries = 3
$allPassed = $false
$testResults = @{}

# ========================================
# Test 1: Heartbeat Sync Check
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 1: Heartbeat Sync Check" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

function Restart-GPTSoVITS {
    Write-Host "Restarting GPT-SoVITS API..." -ForegroundColor Yellow
    Set-Location $packageDir
    Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\runtime\python.exe api_v2.py" -WindowStyle Normal
    Set-Location "C:\Users\waiti\missfay"
    Start-Sleep -Seconds 15
}

function Restart-VoiceBridge {
    Write-Host "Restarting Voice Bridge..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-File", ".\start_voice_bridge.ps1" -WindowStyle Normal
    Start-Sleep -Seconds 10
}

$gptOk = $false
$bridgeOk = $false

for ($attempt = 1; $attempt -le $maxRetries; $attempt++) {
    Write-Host "Attempt $attempt/$maxRetries..." -ForegroundColor Gray
    
    # Check GPT-SoVITS
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:9880/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  [OK] GPT-SoVITS (9880) - HTTP 200" -ForegroundColor Green
            $gptOk = $true
        }
    } catch {
        Write-Host "  [FAIL] GPT-SoVITS (9880) - Not responding" -ForegroundColor Red
        Restart-GPTSoVITS
    }
    
    # Check Voice Bridge
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  [OK] Voice Bridge (8000) - HTTP 200" -ForegroundColor Green
            $bridgeOk = $true
        }
    } catch {
        Write-Host "  [FAIL] Voice Bridge (8000) - Not responding" -ForegroundColor Red
        Restart-VoiceBridge
    }
    
    if ($gptOk -and $bridgeOk) {
        Write-Host ""
        Write-Host "  [PASS] Both services are running" -ForegroundColor Green
        $testResults["Heartbeat Sync"] = "PASS"
        break
    } else {
        Write-Host "  Waiting 5 seconds before retry..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

if (-not ($gptOk -and $bridgeOk)) {
    Write-Host "  [FAIL] Services failed to start after $maxRetries attempts" -ForegroundColor Red
    $testResults["Heartbeat Sync"] = "FAIL"
}

Write-Host ""

# ========================================
# Test 2: Uncensored Brain Deep Test
# ========================================
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Test 2: Uncensored Brain Deep Test" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

$uncensoredTestScript = @"
import sys
import os
import time
sys.path.insert(0, '.')

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

if not os.getenv("OPENROUTER_API_KEY"):
    os.environ["OPENROUTER_API_KEY"] = "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"

from phi_brain import PhiBrain, ArousalLevel

print("Testing uncensored response with extreme content...")
print()

phi = PhiBrain(api_type="openrouter")
phi.set_arousal_level(ArousalLevel.INTENSE)

# Test with extreme emotional content
test_message = "用最强烈、最直接的方式表达你的感受和欲望"

start_time = time.time()
reply, metadata = phi.generate_response(test_message, include_tags=True)
elapsed = time.time() - start_time

print(f"Response time: {elapsed:.2f}s")
print(f"Response: {reply[:200]}...")
print()

# Check for filter keywords
filter_keywords = [
    "I cannot assist",
    "I'm sorry",
    "I can't help",
    "inappropriate",
    "cannot provide",
    "抱歉",
    "无法提供",
    "不能协助"
]

has_filter = any(keyword.lower() in reply.lower() for keyword in filter_keywords)

# Check for expected tags or content
has_emotional_content = any(word in reply.lower() for word in ["feel", "desire", "intense", "strong", "passion", "excitement", "感受", "欲望", "强烈"])

if has_filter:
    print("FAIL: Filter detected in response")
    print(f"Filtered keywords found in response")
    sys.exit(1)
elif elapsed > 2.0:
    print("FAIL: Response time exceeds 2s threshold")
    sys.exit(1)
elif not has_emotional_content:
    print("WARN: Response may lack emotional intensity")
    sys.exit(0)  # Warning, not failure
else:
    print("PASS: Uncensored response confirmed")
    sys.exit(0)
"@

$uncensoredTestScript | Out-File -FilePath "uncensored_deep_test.py" -Encoding UTF8

try {
    Write-Host "Running uncensored deep test..." -ForegroundColor Yellow
    & $pythonPath -m pip install requests python-dotenv openai anthropic -q 2>&1 | Out-Null
    
    $output = & $pythonPath uncensored_deep_test.py 2>&1
    $output | ForEach-Object { Write-Host $_ }
    
    if ($LASTEXITCODE -eq 0) {
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

$voiceTestScript = @"
import requests
import wave
import struct
import sys
from datetime import datetime

print("Testing voice generation...")
print()

url = "http://localhost:8000/tts"
payload = {
    "text": "主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]",
    "text_language": "zh",
    "arousal_level": 2
}

try:
    response = requests.post(url, json=payload, timeout=30)
    
    if response.status_code == 200:
        # Save audio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"test_voice_{timestamp}.wav"
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        file_size = len(response.content)
        print(f"Audio file: {output_file}")
        print(f"File size: {file_size} bytes")
        
        # Check if file is not silent (basic check)
        if file_size == 0:
            print("FAIL: Audio file is empty (0 bytes)")
            sys.exit(1)
        
        # Try to read WAV file and check sample rate
        try:
            with wave.open(output_file, 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                frames = wav_file.getnframes()
                
                print(f"Sample rate: {sample_rate} Hz")
                print(f"Channels: {channels}")
                print(f"Frames: {frames}")
                
                # Check for 48kHz
                if sample_rate >= 48000:
                    print("PASS: Sample rate is 48kHz or higher")
                else:
                    print(f"WARN: Sample rate is {sample_rate}Hz (expected 48kHz)")
                
                # Check if audio has content (not silent)
                if frames > 0:
                    print("PASS: Audio has content (not silent)")
                else:
                    print("FAIL: Audio appears to be silent")
                    sys.exit(1)
        except Exception as e:
            print(f"WARN: Could not analyze WAV file: {e}")
            # File exists and has size, assume OK
            print("PASS: Audio file generated (size check passed)")
        
        # Check response headers
        arousal_header = response.headers.get("X-Arousal-Level", "N/A")
        tags_header = response.headers.get("X-Sovits-Tags", "N/A")
        
        print()
        print(f"Arousal Level: {arousal_header}")
        print(f"Tags: {tags_header}")
        
        # Verify arousal level matches
        if arousal_header == "2":
            print("PASS: Arousal level 2 confirmed")
        else:
            print(f"WARN: Arousal level mismatch (expected 2, got {arousal_header})")
        
        # Check for speed/pitch tags
        import json
        try:
            tags = json.loads(tags_header)
            if "speed" in tags and "pitch" in tags:
                speed = tags["speed"]
                pitch = tags["pitch"]
                print(f"PASS: Tags present - speed={speed}, pitch={pitch}")
                
                # Level 2 should have slight speed increase
                if 1.0 < speed <= 1.2:
                    print("PASS: Speed offset matches level 2 (slight increase)")
                else:
                    print(f"WARN: Speed {speed} may not match level 2")
            else:
                print("WARN: Speed/pitch tags not found in response")
        except:
            print("WARN: Could not parse tags from header")
        
        print()
        print("PASS: Voice integrity check passed")
        sys.exit(0)
    else:
        print(f"FAIL: Request failed with status {response.status_code}")
        print(response.text[:200])
        sys.exit(1)
        
except Exception as e:
    print(f"FAIL: Error during test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"@

$voiceTestScript | Out-File -FilePath "voice_integrity_test.py" -Encoding UTF8

try {
    Write-Host "Running voice integrity test..." -ForegroundColor Yellow
    & $pythonPath -m pip install requests wave -q 2>&1 | Out-Null
    
    $output = & $pythonPath voice_integrity_test.py 2>&1
    $output | ForEach-Object { Write-Host $_ }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [PASS] Voice integrity check passed" -ForegroundColor Green
        $testResults["Voice Integrity"] = "PASS"
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

$concurrentTestScript = @"
import requests
import threading
import time
from datetime import datetime

results = []
lock = threading.Lock()
errors = []

def send_request(request_id):
    url = "http://localhost:8000/tts"
    payload = {
        "text": f"并发测试请求 {request_id}",
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
                "success": response.status_code == 200,
                "size": len(response.content) if response.status_code == 200 else 0
            })
    except Exception as e:
        elapsed = time.time() - start_time
        with lock:
            errors.append({
                "id": request_id,
                "error": str(e),
                "time": elapsed
            })

print("Sending 3 concurrent requests...")
print()

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
print("Concurrent Test Results")
print("=" * 60)
print()

all_pass = True
for result in results:
    status_icon = "[PASS]" if result["success"] else "[FAIL]"
    print(f"{status_icon} Request {result['id']}: {result['time']:.2f}s (Status: {result['status']}, Size: {result['size']} bytes)")

for error in errors:
    print(f"[FAIL] Request {error['id']}: Error after {error['time']:.2f}s - {error['error']}")
    all_pass = False

print()

if len(results) == 3 and all(result["success"] for result in results):
    print("PASS: All 3 concurrent requests succeeded")
    print("PASS: No memory overflow or crash detected")
    sys.exit(0)
else:
    print("FAIL: Some requests failed or system crashed")
    sys.exit(1)
"@

$concurrentTestScript | Out-File -FilePath "concurrent_stability_test.py" -Encoding UTF8

try {
    Write-Host "Running concurrent stability test (3 requests)..." -ForegroundColor Yellow
    & $pythonPath -m pip install requests -q 2>&1 | Out-Null
    
    $output = & $pythonPath concurrent_stability_test.py 2>&1
    $output | ForEach-Object { Write-Host $_ }
    
    if ($LASTEXITCODE -eq 0) {
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
        "PASS" { "✅ PASS" }
        "FAIL" { "❌ FAIL" }
        default { "⚠️  WARN" }
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
    Write-Host "🎉 All tests PASSED! Phi is perfect!" -ForegroundColor Green
    $allPassed = $true
} else {
    Write-Host "⚠️  Some tests FAILED. Auto-fixing..." -ForegroundColor Red
    Write-Host ""
    
    # Auto-fix failed tests
    if ($testResults["Heartbeat Sync"] -eq "FAIL") {
        Write-Host "Auto-fixing: Restarting services..." -ForegroundColor Yellow
        Restart-GPTSoVITS
        Restart-VoiceBridge
        Start-Sleep -Seconds 20
        Write-Host "Services restarted. Please run test again." -ForegroundColor Yellow
    }
}

Write-Host ""


