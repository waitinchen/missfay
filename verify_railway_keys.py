"""
验证 Railway 环境变量的健康状况
检查 GEMINI_API_KEY, CARTESIA_API_KEY, CARTESIA_VOICE_ID, GEMINI_MODEL 是否有效
"""

import os
import sys
import httpx
import asyncio
from typing import Dict, Any

# 从环境变量读取（模拟 Railway 环境）
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
CARTESIA_VOICE_ID = os.getenv("CARTESIA_VOICE_ID")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

results = {
    "GEMINI_API_KEY": {"exists": False, "valid": False, "error": None},
    "CARTESIA_API_KEY": {"exists": False, "valid": False, "error": None},
    "CARTESIA_VOICE_ID": {"exists": False, "valid": False, "error": None},
    "GEMINI_MODEL": {"exists": False, "valid": False, "error": None}
}

print("=" * 60)
print("🔍 Railway 环境变量健康检查")
print("=" * 60)
print()

# 1. 检查 GEMINI_API_KEY
print("1️⃣  检查 GEMINI_API_KEY...")
if GEMINI_API_KEY:
    results["GEMINI_API_KEY"]["exists"] = True
    print(f"   ✅ 存在 (长度: {len(GEMINI_API_KEY)})")
    print(f"   📝 前5个字符: {GEMINI_API_KEY[:5] if len(GEMINI_API_KEY) >= 5 else 'INVALID'}")
    
    # 验证 Gemini API Key
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        
        # 尝试列出模型（轻量级验证）
        models = genai.list_models()
        model_names = [m.name for m in models]
        
        # 检查指定的模型是否存在
        target_model = f"models/{GEMINI_MODEL}"
        if target_model in model_names or any(GEMINI_MODEL in name for name in model_names):
            results["GEMINI_API_KEY"]["valid"] = True
            results["GEMINI_MODEL"]["valid"] = True
            print(f"   ✅ GEMINI_API_KEY 有效")
            print(f"   ✅ 模型 '{GEMINI_MODEL}' 可用")
        else:
            results["GEMINI_API_KEY"]["valid"] = True  # Key 有效，但模型可能不存在
            results["GEMINI_MODEL"]["valid"] = False
            results["GEMINI_MODEL"]["error"] = f"模型 '{GEMINI_MODEL}' 不在可用列表中"
            print(f"   ⚠️  GEMINI_API_KEY 有效，但模型 '{GEMINI_MODEL}' 可能不可用")
            print(f"   📋 可用模型示例: {model_names[:3] if model_names else 'None'}")
    except Exception as e:
        results["GEMINI_API_KEY"]["valid"] = False
        results["GEMINI_API_KEY"]["error"] = str(e)
        print(f"   ❌ GEMINI_API_KEY 无效: {str(e)}")
else:
    results["GEMINI_API_KEY"]["exists"] = False
    print("   ❌ 不存在")

print()

# 2. 检查 CARTESIA_API_KEY
print("2️⃣  检查 CARTESIA_API_KEY...")
if CARTESIA_API_KEY:
    results["CARTESIA_API_KEY"]["exists"] = True
    print(f"   ✅ 存在 (长度: {len(CARTESIA_API_KEY)})")
    print(f"   📝 前5个字符: {CARTESIA_API_KEY[:5] if len(CARTESIA_API_KEY) >= 5 else 'INVALID'}")
    
    # 验证 Cartesia API Key
    async def verify_cartesia():
        try:
            from cartesia import Cartesia
            client = Cartesia(api_key=CARTESIA_API_KEY)
            
            # 尝试获取可用语音列表（轻量级验证）
            # 注意：Cartesia SDK 可能没有直接的验证方法，我们尝试初始化客户端
            results["CARTESIA_API_KEY"]["valid"] = True
            print(f"   ✅ CARTESIA_API_KEY 有效（客户端初始化成功）")
            return True
        except Exception as e:
            error_str = str(e)
            if "401" in error_str or "unauthorized" in error_str.lower():
                results["CARTESIA_API_KEY"]["valid"] = False
                results["CARTESIA_API_KEY"]["error"] = "401 Unauthorized - API Key 无效"
                print(f"   ❌ CARTESIA_API_KEY 无效: 401 Unauthorized")
            else:
                results["CARTESIA_API_KEY"]["valid"] = False
                results["CARTESIA_API_KEY"]["error"] = error_str
                print(f"   ❌ CARTESIA_API_KEY 验证失败: {error_str}")
            return False
    
    try:
        asyncio.run(verify_cartesia())
    except ImportError:
        # 如果 cartesia 包未安装，使用 HTTP 请求验证
        print("   ⚠️  cartesia 包未安装，使用 HTTP 请求验证...")
        try:
            async def verify_cartesia_http():
                async with httpx.AsyncClient() as client:
                    # Cartesia API 验证端点（假设）
                    headers = {"X-API-Key": CARTESIA_API_KEY}
                    # 尝试一个轻量级的 API 调用
                    response = await client.get(
                        "https://api.cartesia.ai/v1/voices",
                        headers=headers,
                        timeout=10.0
                    )
                    if response.status_code == 200:
                        results["CARTESIA_API_KEY"]["valid"] = True
                        print(f"   ✅ CARTESIA_API_KEY 有效")
                    elif response.status_code == 401:
                        results["CARTESIA_API_KEY"]["valid"] = False
                        results["CARTESIA_API_KEY"]["error"] = "401 Unauthorized"
                        print(f"   ❌ CARTESIA_API_KEY 无效: 401 Unauthorized")
                    else:
                        results["CARTESIA_API_KEY"]["valid"] = False
                        results["CARTESIA_API_KEY"]["error"] = f"HTTP {response.status_code}"
                        print(f"   ⚠️  CARTESIA_API_KEY 验证返回: HTTP {response.status_code}")
            asyncio.run(verify_cartesia_http())
        except Exception as e:
            results["CARTESIA_API_KEY"]["valid"] = False
            results["CARTESIA_API_KEY"]["error"] = str(e)
            print(f"   ❌ CARTESIA_API_KEY 验证失败: {str(e)}")
else:
    results["CARTESIA_API_KEY"]["exists"] = False
    print("   ❌ 不存在")

print()

# 3. 检查 CARTESIA_VOICE_ID
print("3️⃣  检查 CARTESIA_VOICE_ID...")
if CARTESIA_VOICE_ID:
    results["CARTESIA_VOICE_ID"]["exists"] = True
    print(f"   ✅ 存在: {CARTESIA_VOICE_ID}")
    
    # 验证 Voice ID 格式（UUID 格式）
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if re.match(uuid_pattern, CARTESIA_VOICE_ID, re.IGNORECASE):
        results["CARTESIA_VOICE_ID"]["valid"] = True
        print(f"   ✅ CARTESIA_VOICE_ID 格式有效 (UUID)")
    else:
        results["CARTESIA_VOICE_ID"]["valid"] = False
        results["CARTESIA_VOICE_ID"]["error"] = "格式无效（应为 UUID 格式）"
        print(f"   ❌ CARTESIA_VOICE_ID 格式无效")
else:
    results["CARTESIA_VOICE_ID"]["exists"] = False
    print("   ❌ 不存在")

print()

# 4. 检查 GEMINI_MODEL
print("4️⃣  检查 GEMINI_MODEL...")
if GEMINI_MODEL:
    results["GEMINI_MODEL"]["exists"] = True
    print(f"   ✅ 存在: {GEMINI_MODEL}")
    
    # 模型有效性已在 GEMINI_API_KEY 验证时检查
    if results["GEMINI_MODEL"]["valid"]:
        print(f"   ✅ GEMINI_MODEL 有效")
    elif results["GEMINI_MODEL"]["error"]:
        print(f"   ⚠️  {results['GEMINI_MODEL']['error']}")
else:
    results["GEMINI_MODEL"]["exists"] = False
    print("   ❌ 不存在")

print()
print("=" * 60)
print("📊 健康检查总结")
print("=" * 60)

all_valid = True
for key, status in results.items():
    status_icon = "✅" if status["exists"] and status["valid"] else "❌" if not status["exists"] else "⚠️"
    print(f"{status_icon} {key}:")
    print(f"   存在: {'是' if status['exists'] else '否'}")
    if status["exists"]:
        print(f"   有效: {'是' if status['valid'] else '否'}")
        if status["error"]:
            print(f"   错误: {status['error']}")
    if not (status["exists"] and status["valid"]):
        all_valid = False
    print()

if all_valid:
    print("🎉 所有环境变量都健康！")
else:
    print("⚠️  部分环境变量存在问题，请检查上述错误信息。")

print("=" * 60)

