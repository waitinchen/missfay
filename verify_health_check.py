"""Verify health check endpoint returns all required fields"""
import requests
import json
import sys
import time

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("  Verify Health Check Endpoint")
print("=" * 80)
print()

# Wait for service to start
print("Waiting for service to start...")
for i in range(15):
    try:
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.ok:
            break
    except:
        pass
    time.sleep(1)
    print(f"  Attempt {i+1}/15...")

print()
print("Checking health check endpoint...")
print("-" * 80)

try:
    response = requests.get('http://localhost:8000/health', timeout=5)
    if response.ok:
        data = response.json()
        print(f"Status code: {response.status_code}")
        print(f"Response fields: {list(data.keys())}")
        print()
        
        # Check required fields
        required_fields = ['brain_status', 'cartesia_status']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            print(f"[X] Missing fields: {', '.join(missing)}")
            print()
            print("Fix suggestions:")
            print("1. Ensure service has been restarted")
            print("2. Check health check endpoint code in voice_bridge.py")
            print("3. Restart service: .\\start_voice_bridge.ps1")
        else:
            print("[OK] All required fields present")
            print()
            print("Detailed status:")
            print(f"  brain_ready: {data.get('brain_ready')}")
            print(f"  brain_status: {data.get('brain_status')}")
            print(f"  cartesia_status: {data.get('cartesia_status')}")
            print(f"  engine: {data.get('engine')}")
            print()
            
            # Check status values
            if data.get('brain_status') == 'ready' and data.get('cartesia_status') == 'ready':
                print("[OK] Both LLM and TTS are ready")
                print("Frontend should show: LLM: OK  TTS: OK (green)")
            elif data.get('cartesia_status') == 'unauthorized':
                print("[X] TTS authentication failed (401)")
                print("Please check CARTESIA_API_KEY")
            else:
                print(f"[!] Status abnormal:")
                print(f"  LLM: {data.get('brain_status')}")
                print(f"  TTS: {data.get('cartesia_status')}")
    else:
        print(f"[X] Health check failed: {response.status_code}")
        print(f"Response: {response.text[:200]}")
except requests.exceptions.ConnectionError:
    print("[X] Cannot connect to service")
    print("Please ensure service is running:")
    print("  .\\start_voice_bridge.ps1")
except Exception as e:
    print(f"[X] Error: {str(e)}")

print()
print("=" * 80)
print("  Verification Complete")
print("=" * 80)

