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

def verify_api_key():
    """验证 OpenRouter API Key"""
    print("=" * 60)
    print("验证 OpenRouter API Key")
    print("=" * 60)
    print()
    
    # 获取 API Key
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("错误: 未找到 OPENROUTER_API_KEY")
        print("请运行 .\\配置OpenRouter.ps1 配置 API Key")
        return False
    
    print(f"找到 API Key: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # 检查格式
    print("检查 API Key 格式...")
    if api_key.startswith("sk-or-v1-"):
        print("  API Key 格式正确 (OpenRouter v1)")
    else:
        print("  警告: API Key 格式可能不正确")
    print()
    
    # 发送测试请求
    print("发送测试请求到 OpenRouter...")
    
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
                "content": "Hello, this is a test. Please respond with 'API Key is valid'."
            }
        ],
        "max_tokens": 50
    }
    
    try:
        print("  正在发送请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"  状态码: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("  API Key 有效！")
            print()
            
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                reply = data["choices"][0]["message"]["content"]
                print("  响应内容:")
                print(f"    {reply}")
                print()
            
            if "usage" in data:
                usage = data["usage"]
                print("  使用统计:")
                print(f"    提示词 tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"    完成 tokens: {usage.get('completion_tokens', 'N/A')}")
                print(f"    总计 tokens: {usage.get('total_tokens', 'N/A')}")
                print()
            
            return True
            
        elif response.status_code == 401:
            print("  API Key 无效或已过期")
            try:
                error_data = response.json()
                print(f"  错误信息: {error_data}")
            except:
                print(f"  错误信息: {response.text[:200]}")
            return False
            
        elif response.status_code == 429:
            print("  请求频率限制（Rate Limit）")
            print("  API Key 有效，但需要等待")
            return True
            
        else:
            print(f"  请求失败，状态码: {response.status_code}")
            try:
                error_data = response.json()
                print(f"  错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"  响应: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("  请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"  请求错误: {str(e)}")
        return False
    except Exception as e:
        print(f"  未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print()
    print("启动 OpenRouter API Key 验证")
    print()
    
    is_valid = verify_api_key()
    
    print()
    print("=" * 60)
    if is_valid:
        print("API Key 验证完成，系统可以正常使用")
        sys.exit(0)
    else:
        print("API Key 验证失败，请检查配置")
        sys.exit(1)



