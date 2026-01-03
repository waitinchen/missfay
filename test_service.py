"""测试 Voice Bridge 服务"""
import requests
import sys

print("=" * 60)
print("Testing Voice Bridge Service")
print("=" * 60)
print()

base_url = "http://localhost:8000"

# 测试健康检查
print("1. Testing /health endpoint...")
try:
    response = requests.get(f"{base_url}/health", timeout=3)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
        print("   [OK] Service is running")
    else:
        print(f"   [FAIL] Unexpected status code")
except requests.exceptions.ConnectionError:
    print("   [FAIL] Service is not running!")
    print("   Please start Voice Bridge service first")
    sys.exit(1)
except Exception as e:
    print(f"   [ERROR] {e}")
    sys.exit(1)

print()

# 测试根路径
print("2. Testing / endpoint...")
try:
    response = requests.get(f"{base_url}/", timeout=3)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    if response.status_code == 200:
        content = response.text[:200]
        if content.startswith("<!DOCTYPE") or content.startswith("<html"):
            print("   [OK] HTML content returned")
        else:
            print(f"   [WARN] Not HTML: {content}")
    else:
        print(f"   [FAIL] Status: {response.status_code}")
except Exception as e:
    print(f"   [ERROR] {e}")

print()

# 测试静态文件
print("3. Testing /static/index.html endpoint...")
try:
    response = requests.get(f"{base_url}/static/index.html", timeout=3)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    if response.status_code == 200:
        content = response.text[:200]
        if content.startswith("<!DOCTYPE") or content.startswith("<html"):
            print("   [OK] HTML file served successfully")
            print(f"   Content length: {len(response.text)} bytes")
        else:
            print(f"   [WARN] Not HTML: {content[:100]}")
    else:
        print(f"   [FAIL] Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   [ERROR] {e}")

print()
print("=" * 60)



