"""Local Testing Script - Test Phi System Functionality"""
import os
import sys
import requests
import time
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("  " + "=" * 76)
print("   Phi System Local Testing (本地测试)")
print("  " + "=" * 76)
print("=" * 80)
print()

BASE_URL = "http://localhost:8000"
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0
}

def test(name, func):
    """Execute test"""
    test_results["total"] += 1
    print(f"[{test_results['total']}] {name}")
    print("-" * 80)
    try:
        result = func()
        if result:
            print(f"   [OK] {name} - Passed")
            test_results["passed"] += 1
        else:
            print(f"   [X] {name} - Failed")
            test_results["failed"] += 1
    except Exception as e:
        print(f"   [X] {name} - Error: {str(e)[:100]}")
        test_results["failed"] += 1
    print()

# Test 1: Health check endpoint
def test_health():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status code: {response.status_code}")
            print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"   Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   Error: Cannot connect to service, please ensure Voice Bridge is running")
        return False
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

# Test 2: Frontend interface
def test_frontend():
    """Test frontend interface"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            content = response.text
            if "心菲" in content or "Phi" in content or "<html" in content.lower():
                print(f"   Status code: {response.status_code}")
                print(f"   Content type: {response.headers.get('content-type', 'unknown')}")
                print(f"   Content length: {len(content)} characters")
                return True
            else:
                print(f"   Status code: {response.status_code}, but content doesn't match expected")
                return False
        else:
            print(f"   Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   Error: Cannot connect to service")
        return False
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

# Test 3: Static files
def test_static():
    """Test static files"""
    try:
        response = requests.get(f"{BASE_URL}/static/phi_chat.html", timeout=5)
        if response.status_code == 200:
            print(f"   Status code: {response.status_code}")
            print(f"   File size: {len(response.content)} bytes")
            return True
        else:
            print(f"   Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

# Test 4: Chat endpoint (simple test)
def test_chat_endpoint():
    """Test chat endpoint"""
    try:
        payload = {
            "text": "你好",
            "arousal_level": 0  # Integer 0-4, not string
        }
        print(f"   Sending request to /chat...")
        print(f"   Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   Status code: {response.status_code}")
            print(f"   Response contains: {list(data.keys())}")
            if "reply" in data:
                reply_preview = data['reply'][:100] if len(data['reply']) > 100 else data['reply']
                print(f"   Reply preview: {reply_preview}...")
            if "audio" in data:
                audio_status = "exists" if data['audio'] else "missing"
                print(f"   Audio data: {audio_status}")
            return True
        else:
            print(f"   Status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error info: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   Error info: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print("   Error: Request timeout (LLM may be slow to respond)")
        return False
    except requests.exceptions.ConnectionError:
        print("   Error: Cannot connect to service")
        return False
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

# Test 5: Phi Voice endpoint (proxy layer)
def test_phi_voice_endpoint():
    """Test Phi Voice endpoint"""
    try:
        payload = {
            "user_input": "主人，菲菲测试中",
            "session_id": "test_session_001"
        }
        print(f"   Sending request to /api/v1/phi_voice...")
        response = requests.post(
            f"{BASE_URL}/api/v1/phi_voice",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            print(f"   Status code: {response.status_code}")
            print(f"   Content type: {content_type}")
            if 'audio' in content_type:
                print(f"   Audio data size: {len(response.content)} bytes")
                return True
            else:
                # May be JSON format
                try:
                    data = response.json()
                    if "audio" in data:
                        print(f"   Audio in JSON format: {len(data.get('audio', ''))} characters")
                        return True
                except:
                    pass
                print(f"   Response type: {response.text[:100]}")
                return True
        else:
            print(f"   Status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error info: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   Error info: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print("   Error: Request timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("   Error: Cannot connect to service")
        return False
    except Exception as e:
        print(f"   Error: {str(e)}")
        return False

# Execute tests
print("Starting tests...")
print()

test("Health Check Endpoint (/health)", test_health)
time.sleep(1)

test("Frontend Interface (/)", test_frontend)
time.sleep(1)

test("Static Files (/static/phi_chat.html)", test_static)
time.sleep(1)

print("=" * 80)
print("  Functional Tests (may take longer)")
print("=" * 80)
print()

test("Chat Endpoint (/chat)", test_chat_endpoint)
time.sleep(2)

test("Phi Voice Endpoint (/api/v1/phi_voice)", test_phi_voice_endpoint)
time.sleep(1)

# Summary report
print("=" * 80)
print("  Test Results Summary")
print("=" * 80)
print()
print(f"   Total tests: {test_results['total']}")
print(f"   ✅ Passed: {test_results['passed']}")
print(f"   ❌ Failed: {test_results['failed']}")
print()

success_rate = (test_results['passed'] / test_results['total'] * 100) if test_results['total'] > 0 else 0
print(f"   Success rate: {success_rate:.1f}%")
print()

if success_rate == 100:
    status = "Perfect"
    status_cn = "完美"
elif success_rate >= 80:
    status = "Good"
    status_cn = "良好"
elif success_rate >= 60:
    status = "Needs Attention"
    status_cn = "需要关注"
else:
    status = "Needs Fix"
    status_cn = "需要修复"

print(f"   Overall status: {status} ({status_cn})")
print()

if test_results['failed'] > 0:
    print("   [⚠] Some tests failed, please check:")
    print("      - Is the service running?")
    print("      - Are API Keys valid?")
    print("      - Is network connection normal?")
    print()
else:
    print("   [✅] All tests passed, system is running normally!")
    print("      - You can access http://localhost:8000/ to use the interface")
    print("      - Health monitor should show: LLM: OK  TTS: OK")
    print()

print("=" * 80)
print("  Testing Complete")
print("=" * 80)
print()

