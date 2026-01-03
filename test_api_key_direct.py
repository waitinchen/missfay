"""直接测试 API Key 是否有效"""
import os
import sys
import openai

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 加载环境变量
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# 手动加载 .env
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"API Key: {'SET' if api_key else 'NOT SET'}")
if api_key:
    print(f"  Preview: {api_key[:20]}...{api_key[-10:]}")
else:
    print("  错误: 未找到 OPENROUTER_API_KEY")
    sys.exit(1)

print("\n测试 API 连接...")
try:
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/Project-Phi",
            "X-Title": "Project Phi"
        }
    )
    
    response = client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct",
        messages=[{"role": "user", "content": "Say 'OK' if you can read this."}],
        max_tokens=10
    )
    
    print("✓ API Key 有效！")
    print(f"  响应: {response.choices[0].message.content}")
    
except openai.APIError as e:
    error_code = getattr(e, 'status_code', None)
    print(f"✗ API 错误: {error_code}")
    if hasattr(e, 'response') and e.response:
        try:
            error_body = e.response.json()
            print(f"  错误详情: {error_body}")
        except:
            print(f"  错误信息: {e.response.text[:200] if hasattr(e.response, 'text') else str(e)}")
    else:
        print(f"  错误信息: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"✗ 错误: {type(e).__name__}: {str(e)}")
    sys.exit(1)

