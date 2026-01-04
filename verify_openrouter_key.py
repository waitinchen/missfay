"""验证 OPENROUTER_API_KEY 是否有效"""
import os
import sys
import requests
import json

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("  OPENROUTER_API_KEY 验证检查")
print("=" * 60)
print()

# 加载环境变量
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

print("1. 检查 .env 文件...")
if os.path.exists(env_path):
    print(f"   [OK] .env 文件存在: {env_path}")
    
    # 读取 .env 文件内容
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
    
    # 查找 OPENROUTER_API_KEY
    openrouter_key_in_file = None
    for line in env_content.splitlines():
        line = line.strip()
        if line.startswith("OPENROUTER_API_KEY="):
            value = line.split('=', 1)[1].strip()
            if value:
                openrouter_key_in_file = value
                break
    
    if openrouter_key_in_file:
        preview = openrouter_key_in_file[:20] + "..." + openrouter_key_in_file[-10:] if len(openrouter_key_in_file) > 30 else openrouter_key_in_file
        print(f"   [OK] 在 .env 文件中找到: {preview}")
    else:
        print("   [X] .env 文件中未找到 OPENROUTER_API_KEY 或值为空")
        sys.exit(1)
else:
    print(f"   [X] .env 文件不存在: {env_path}")
    sys.exit(1)

print()

# 手动加载环境变量
print("2. 加载环境变量...")
for line in env_content.splitlines():
    if '=' in line and not line.startswith('#') and line.strip():
        k, v = line.split('=', 1)
        os.environ[k.strip()] = v.strip()

api_key = os.getenv("OPENROUTER_API_KEY")
if api_key:
    preview = api_key[:20] + "..." + api_key[-10:] if len(api_key) > 30 else api_key
    print(f"   [OK] 环境变量已加载: {preview}")
else:
    print("   [X] 环境变量加载失败")
    sys.exit(1)

print()

# 验证 API Key 格式
print("3. 检查 API Key 格式...")
if api_key.startswith("sk-or-v1-"):
    print("   [OK] API Key 格式正确 (OpenRouter v1)")
elif api_key.startswith("sk-or-"):
    print("   [!] API Key 格式可能是旧版本")
else:
    print("   [X] API Key 格式不正确")
    print(f"       当前格式: {api_key[:10]}...")
    sys.exit(1)

print()

# 测试 API Key
print("4. 测试 API Key 有效性...")
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
            "content": "Say 'OK' if you can read this."
        }
    ],
    "max_tokens": 10
}

try:
    print("   正在发送测试请求...")
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"]
            print(f"   [OK] API Key 有效！")
            print(f"   响应: {reply}")
            if "usage" in data:
                print(f"   Tokens: {data['usage']['total_tokens']}")
        else:
            print("   [!] API Key 可能有效，但响应格式异常")
    elif response.status_code == 401:
        print("   [X] API Key 无效或已过期 (401)")
        try:
            error_data = response.json()
            if "error" in error_data and "message" in error_data["error"]:
                print(f"   错误信息: {error_data['error']['message']}")
            else:
                print(f"   错误详情: {error_data}")
        except:
            print(f"   错误响应: {response.text[:200]}")
        sys.exit(1)
    elif response.status_code == 429:
        print("   [!] 请求频率限制 (429) - API Key 有效，但需要等待")
    else:
        print(f"   [X] 请求失败，状态码: {response.status_code}")
        try:
            error_data = response.json()
            print(f"   错误详情: {error_data}")
        except:
            print(f"   错误响应: {response.text[:200]}")
        sys.exit(1)
        
except requests.exceptions.Timeout:
    print("   [X] 请求超时")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"   [X] 请求错误: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"   [X] 未知错误: {str(e)}")
    sys.exit(1)

print()
print("=" * 60)
print("  验证完成 - API Key 有效")
print("=" * 60)


