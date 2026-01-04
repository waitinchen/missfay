"""
使用 Python 测试 API 端点
"""

import sys
import json
import time

# 设置 UTF-8 编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import httpx
except ImportError:
    print("[ERROR] httpx 未安装")
    print("请运行: pip install httpx")
    sys.exit(1)

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("测试 API 端点")
print("=" * 60)
print()

# 测试 1: 健康检查
print("1. 测试 /health 端点...")
try:
    response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] 状态码: {response.status_code}")
        print(f"   [OK] 响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print()
        
        # 检查关键状态
        if data.get("brain_ready"):
            print("   [OK] LLM (大脑) 已就绪")
        else:
            print("   [WARN] LLM (大脑) 未就绪")
        
        if data.get("cartesia_status") == "ready":
            print("   [OK] TTS (Cartesia) 已就绪")
        else:
            print(f"   [WARN] TTS (Cartesia) 状态: {data.get('cartesia_status')}")
    else:
        print(f"   [ERROR] 状态码: {response.status_code}")
        print(f"   响应: {response.text}")
except Exception as e:
    print(f"   [ERROR] 连接失败: {str(e)}")
    print("   请确保服务已启动: python -m uvicorn voice_bridge:app --host 0.0.0.0 --port 8000")
    sys.exit(1)

print()

# 测试 2: 验证环境变量
print("2. 测试 /verify-keys 端点...")
try:
    response = httpx.get(f"{BASE_URL}/verify-keys", timeout=5.0)
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] 状态码: {response.status_code}")
        print(f"   [OK] 响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print()
        
        # 检查每个 Key
        keys_to_check = ["GEMINI_API_KEY", "CARTESIA_API_KEY", "CARTESIA_VOICE_ID", "GEMINI_MODEL"]
        for key in keys_to_check:
            status = data.get(key, {})
            if status.get("exists") and status.get("valid"):
                print(f"   [OK] {key}: 存在且有效")
            elif status.get("exists"):
                print(f"   [WARN] {key}: 存在但可能无效")
            else:
                print(f"   [ERROR] {key}: 不存在")
    else:
        print(f"   [ERROR] 状态码: {response.status_code}")
        print(f"   响应: {response.text}")
except Exception as e:
    print(f"   [ERROR] 请求失败: {str(e)}")

print()

# 测试 3: 聊天端点
print("3. 测试 /chat 端点...")
try:
    payload = {
        "text": "你好",
        "arousal_level": 0
    }
    print(f"   发送: {json.dumps(payload, ensure_ascii=False)}")
    
    response = httpx.post(
        f"{BASE_URL}/chat",
        json=payload,
        timeout=30.0  # 聊天可能需要更长时间
    )
    
    if response.status_code == 200:
        print(f"   [OK] 状态码: {response.status_code}")
        
        # 检查响应类型
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            data = response.json()
            print(f"   [OK] 响应类型: JSON")
            print(f"   [OK] 响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        elif "audio" in content_type:
            print(f"   [OK] 响应类型: 音频")
            print(f"   [OK] 音频大小: {len(response.content)} 字节")
        else:
            print(f"   [OK] 响应类型: {content_type}")
            print(f"   [OK] 响应长度: {len(response.content)} 字节")
    elif response.status_code == 429:
        print(f"   [WARN] 状态码: 429 (速率限制)")
        print(f"   响应: {response.text[:200]}")
    else:
        print(f"   [ERROR] 状态码: {response.status_code}")
        print(f"   响应: {response.text[:500]}")
except httpx.TimeoutException:
    print(f"   [ERROR] 请求超时（>30秒）")
except Exception as e:
    print(f"   [ERROR] 请求失败: {str(e)}")

print()
print("=" * 60)
print("测试完成")
print("=" * 60)

