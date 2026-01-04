"""
检查 Railway 生产环境的环境变量配置
用于诊断 LLM 初始化问题
"""

import httpx
import json
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 生产环境 URL
PRODUCTION_URL = "https://missfay.tonetown.ai"

print("=" * 60)
print("Railway 生产环境诊断")
print("=" * 60)
print()

print(f"生产环境 URL: {PRODUCTION_URL}")
print()

# 1. 检查健康状态
print("1. 检查 /health 端点...")
try:
    response = httpx.get(f"{PRODUCTION_URL}/health", timeout=10.0)
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] 状态码: {response.status_code}")
        print()
        
        print("   健康状态:")
        print(f"   - brain_ready: {data.get('brain_ready', False)}")
        print(f"   - brain_status: {data.get('brain_status', 'unknown')}")
        print(f"   - cartesia_status: {data.get('cartesia_status', 'unknown')}")
        print()
        
        # 显示诊断信息
        diagnostics = data.get('diagnostics')
        if diagnostics:
            print("   诊断信息:")
            print(f"   - gemini_key_exists: {diagnostics.get('gemini_key_exists', False)}")
            print(f"   - gemini_key_length: {diagnostics.get('gemini_key_length', 0)}")
            if diagnostics.get('init_error'):
                print(f"   - init_error: {diagnostics.get('init_error')[:100]}...")
            print()
            
            if not diagnostics.get('gemini_key_exists'):
                print("   [ERROR] GEMINI_API_KEY 未在环境变量中找到！")
                print("   解决方案: 在 Railway Dashboard 中设置 GEMINI_API_KEY")
        else:
            if data.get('brain_ready'):
                print("   [OK] LLM 已就绪，无需诊断")
            else:
                print("   [WARN] 未返回诊断信息，但 brain_ready 为 False")
    else:
        print(f"   [ERROR] 状态码: {response.status_code}")
        print(f"   响应: {response.text[:200]}")
except Exception as e:
    print(f"   [ERROR] 连接失败: {str(e)}")
    print("   请检查生产环境是否正常运行")

print()

# 2. 检查环境变量验证
print("2. 检查 /verify-keys 端点...")
try:
    response = httpx.get(f"{PRODUCTION_URL}/verify-keys", timeout=10.0)
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] 状态码: {response.status_code}")
        print()
        
        keys = data.get('keys', {})
        gemini_key_info = keys.get('GEMINI_API_KEY', {})
        
        print("   GEMINI_API_KEY 状态:")
        print(f"   - exists: {gemini_key_info.get('exists', False)}")
        print(f"   - valid: {gemini_key_info.get('valid', False)}")
        print(f"   - length: {gemini_key_info.get('length', 0)}")
        if gemini_key_info.get('error'):
            print(f"   - error: {gemini_key_info.get('error')}")
        print()
        
        if not gemini_key_info.get('exists'):
            print("   [ERROR] GEMINI_API_KEY 不存在于环境变量中")
            print("   解决方案:")
            print("   1. 访问 Railway Dashboard")
            print("   2. 进入 Service → Variables")
            print("   3. 添加变量: GEMINI_API_KEY = AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo")
            print("   4. 保存并重新部署")
        elif not gemini_key_info.get('valid'):
            print("   [ERROR] GEMINI_API_KEY 存在但无效")
            print("   解决方案: 检查 API Key 是否正确，或验证 Key 是否有效")
        else:
            print("   [OK] GEMINI_API_KEY 存在且有效")
    else:
        print(f"   [ERROR] 状态码: {response.status_code}")
except Exception as e:
    print(f"   [ERROR] 请求失败: {str(e)}")

print()
print("=" * 60)
print("诊断完成")
print("=" * 60)
print()
print("如果 GEMINI_API_KEY 不存在或无效，请:")
print("1. 访问 Railway Dashboard: https://railway.com")
print("2. 进入您的 Service → Variables")
print("3. 确保以下变量已设置:")
print("   - GEMINI_API_KEY = AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo")
print("   - GEMINI_MODEL = gemini-2.0-flash-exp")
print("   - CARTESIA_API_KEY = (您的 Cartesia Key)")
print("   - CARTESIA_VOICE_ID = a5a8b420-9360-4145-9c1e-db4ede8e4b15")
print("4. 保存后重新部署服务")
print()

