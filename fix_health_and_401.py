"""Fix health check and 401 error"""
import requests
import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("  Fix Health Check and 401 Error")
print("=" * 80)
print()

# 1. Check health endpoint
print("[1] Check Health Endpoint")
print("-" * 80)
try:
    response = requests.get('http://localhost:8000/health', timeout=5)
    if response.ok:
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Fields: {list(data.keys())}")
        print()
        
        missing = []
        if 'brain_status' not in data:
            missing.append('brain_status')
        if 'cartesia_status' not in data:
            missing.append('cartesia_status')
        
        if missing:
            print(f"   [X] Missing fields: {', '.join(missing)}")
            print(f"   [Fix] Service may not have restarted")
            print(f"   [Action] Please restart:")
            print(f"      .\\kill_python_processes.ps1")
            print(f"      .\\start_voice_bridge.ps1")
        else:
            print(f"   [OK] All fields present")
            print(f"   brain_status: {data.get('brain_status')}")
            print(f"   cartesia_status: {data.get('cartesia_status')}")
    else:
        print(f"   [X] Health check failed: {response.status_code}")
except Exception as e:
    print(f"   [X] Cannot connect: {str(e)}")

print()

# 2. Test chat endpoint (check 401)
print("[2] Test Chat Endpoint (Check 401)")
print("-" * 80)
try:
    payload = {"text": "test", "arousal_level": 0}
    response = requests.post('http://localhost:8000/chat', json=payload, timeout=30)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 401:
        print(f"   [X] 401 Error: Authentication failed")
        print(f"   [Fix] Check CARTESIA_API_KEY")
        try:
            error_data = response.json()
            print(f"   Error: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"   Error: {response.text[:200]}")
    elif response.status_code == 200:
        print(f"   [OK] Chat endpoint working")
    else:
        print(f"   [X] Other error: {response.status_code}")
except Exception as e:
    print(f"   [X] Request failed: {str(e)}")

print()
print("=" * 80)
print("  Check Complete")
print("=" * 80)

