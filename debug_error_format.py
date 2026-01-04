"""调试错误格式"""
import os
import sys
import openai

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 加载环境变量
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"API Key: {'SET' if api_key else 'NOT SET'}")

try:
    client = openai.OpenAI(
        api_key=api_key or "test",
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/Project-Phi",
            "X-Title": "Project Phi"
        }
    )
    
    print("\n发送测试请求...")
    response = client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct",
        messages=[{"role": "user", "content": "test"}],
        max_tokens=10
    )
    
except openai.APIError as e:
    print("\n=== OpenAI APIError 详情 ===")
    print(f"类型: {type(e).__name__}")
    print(f"str(e): {str(e)}")
    print(f"repr(e): {repr(e)}")
    print(f"hasattr status_code: {hasattr(e, 'status_code')}")
    if hasattr(e, 'status_code'):
        print(f"status_code: {e.status_code} ({type(e.status_code)})")
    print(f"hasattr code: {hasattr(e, 'code')}")
    if hasattr(e, 'code'):
        print(f"code: {e.code}")
    print(f"hasattr message: {hasattr(e, 'message')}")
    if hasattr(e, 'message'):
        print(f"message: {e.message}")
    print(f"hasattr response: {hasattr(e, 'response')}")
    if hasattr(e, 'response'):
        print(f"response type: {type(e.response)}")
        print(f"response: {e.response}")
        if hasattr(e.response, 'json'):
            try:
                error_body = e.response.json()
                print(f"response.json(): {error_body}")
            except Exception as json_err:
                print(f"response.json() 错误: {json_err}")
        if hasattr(e.response, 'text'):
            try:
                print(f"response.text: {e.response.text[:500]}")
            except Exception as text_err:
                print(f"response.text 错误: {text_err}")
    
    # 测试错误字符串格式
    error_str = str(e)
    print(f"\n=== 错误字符串分析 ===")
    print(f"error_str: {repr(error_str)}")
    print(f"'401' in error_str: {'401' in error_str}")
    
except Exception as e:
    print(f"\n=== 其他异常 ===")
    print(f"类型: {type(e).__name__}")
    print(f"str(e): {str(e)}")
    print(f"repr(e): {repr(e)}")


