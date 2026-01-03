"""直接测试服务响应"""
import requests
import sys

base_url = "http://localhost:8000"

print("=" * 60)
print("Testing Voice Bridge Service")
print("=" * 60)
print()

# 测试健康检查
print("1. Testing /health...")
try:
    response = requests.get(f"{base_url}/health", timeout=3)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
        print("   [OK] Service is running")
    else:
        print(f"   [FAIL] Status: {response.status_code}")
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print("   [FAIL] Service is NOT running!")
    print("   Please start Voice Bridge service first")
    sys.exit(1)
except Exception as e:
    print(f"   [ERROR] {e}")
    sys.exit(1)

print()

# 测试根路径
print("2. Testing / endpoint...")
try:
    response = requests.get(f"{base_url}/", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"   Content-Length: {len(response.content)} bytes")
    
    content = response.text
    if content.startswith("<!DOCTYPE") or content.startswith("<html"):
        print("   [OK] HTML content returned")
        print(f"   First 100 chars: {content[:100]}")
    elif response.headers.get('Content-Type', '').startswith('application/json'):
        print("   [FAIL] JSON returned instead of HTML")
        print(f"   Response: {content[:200]}")
    else:
        print(f"   [WARN] Unknown content type")
        print(f"   Content: {content[:200]}")
except Exception as e:
    print(f"   [ERROR] {e}")

print()

# 测试静态文件
print("3. Testing /static/phi_chat.html...")
try:
    response = requests.get(f"{base_url}/static/phi_chat.html", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    
    if response.status_code == 200:
        content = response.text
        if content.startswith("<!DOCTYPE") or content.startswith("<html"):
            print("   [OK] HTML file served successfully")
            print(f"   Content length: {len(content)} characters")
        else:
            print(f"   [WARN] Not HTML: {content[:100]}")
    else:
        print(f"   [FAIL] Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   [ERROR] {e}")

print()
print("=" * 60)


