"""
验证 OpenRouter API Key 是否有效
"""

import os
import sys
import requests
import json

# 加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def verify_openrouter_api_key():
    """验证 OpenRouter API Key"""
    print("=" * 60)
    print("🔍 验证 OpenRouter API Key")
    print("=" * 60)
    print()
    
    # 获取 API Key
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ 错误: 未找到 OPENROUTER_API_KEY")
        print("   请运行 .\配置OpenRouter.ps1 配置 API Key")
        return False
    
    print(f"✓ 找到 API Key: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # 测试 1: 检查 API Key 格式
    print("测试 1: 检查 API Key 格式...")
    if api_key.startswith("sk-or-v1-"):
        print("  ✅ API Key 格式正确 (OpenRouter v1)")
    else:
        print("  ⚠️  API Key 格式可能不正确")
    print()
    
    # 测试 2: 发送测试请求
    print("测试 2: 发送测试请求到 OpenRouter...")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Project-Phi",
        "X-Title": "Project Phi"
    }
    
    payload = {
        "model": "meta-llama/llama-3-70b-instruct",
        "messages": [
            {
                "role": "user",
                "content": "Hello, this is a test. Please respond with 'API Key is valid' if you can read this."
            }
        ],
        "max_tokens": 50
    }
    
    try:
        print("  正在发送请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✅ API Key 有效！")
            print()
            
            # 解析响应
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                reply = data["choices"][0]["message"]["content"]
                print("  响应内容:")
                print(f"    {reply}")
                print()
            
            # 显示使用信息
            if "usage" in data:
                usage = data["usage"]
                print("  使用统计:")
                print(f"    提示词 tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"    完成 tokens: {usage.get('completion_tokens', 'N/A')}")
                print(f"    总计 tokens: {usage.get('total_tokens', 'N/A')}")
                print()
            
            return True
            
        elif response.status_code == 401:
            print("  ❌ API Key 无效或已过期")
            print(f"  错误信息: {response.text}")
            return False
            
        elif response.status_code == 429:
            print("  ⚠️  请求频率限制（Rate Limit）")
            print("  API Key 有效，但需要等待")
            return True
            
        else:
            print(f"  ⚠️  请求失败，状态码: {response.status_code}")
            print(f"  响应: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ❌ 请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 请求错误: {str(e)}")
        return False
    except Exception as e:
        print(f"  ❌ 未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_api_models():
    """检查可用的模型列表"""
    print()
    print("=" * 60)
    print("📋 检查可用模型")
    print("=" * 60)
    print()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ 未找到 API Key")
        return
    
    url = "https://openrouter.ai/api/v1/models"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/Project-Phi",
        "X-Title": "Project Phi"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if "data" in data:
                models = data["data"]
                print(f"✓ 找到 {len(models)} 个可用模型")
                print()
                
                # 查找配置的模型
                target_models = [
                    "meta-llama/llama-3-70b-instruct",
                    "gryphe/mythomax-l2-13b"
                ]
                
                print("检查配置的模型:")
                for target in target_models:
                    found = any(m.get("id") == target for m in models)
                    status = "✅ 可用" if found else "❌ 不可用"
                    print(f"  {target}: {status}")
                
                print()
                print("前 10 个可用模型:")
                for i, model in enumerate(models[:10], 1):
                    model_id = model.get("id", "N/A")
                    print(f"  {i}. {model_id}")
        else:
            print(f"⚠️  无法获取模型列表，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 检查模型列表时出错: {str(e)}")

if __name__ == "__main__":
    print()
    print("🚀 启动 OpenRouter API Key 验证")
    print()
    
    # 验证 API Key
    is_valid = verify_openrouter_api_key()
    
    # 如果有效，检查可用模型
    if is_valid:
        check_api_models()
    
    print()
    print("=" * 60)
    if is_valid:
        print("✅ API Key 验证完成，系统可以正常使用")
        sys.exit(0)
    else:
        print("❌ API Key 验证失败，请检查配置")
        sys.exit(1)




