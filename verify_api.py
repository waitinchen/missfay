"""验证 OpenRouter API Key"""
import os
import sys
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

api_key = os.getenv("OPENROUTER_API_KEY", "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")

print("=" * 60)
print("Verify OpenRouter API Key")
print("=" * 60)
print(f"\nAPI Key: {api_key[:20]}...{api_key[-10:]}\n")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/Project-Phi",
    "X-Title": "Project Phi"
}
payload = {
    "model": "meta-llama/llama-3-70b-instruct",
    "messages": [{"role": "user", "content": "Say 'API Key is valid' if you can read this."}],
    "max_tokens": 30
}

try:
    print("Sending test request...")
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        print("SUCCESS: API Key is VALID!")
        print(f"Response: {reply}\n")
        if "usage" in data:
            print(f"Tokens used: {data['usage']['total_tokens']}")
        sys.exit(0)
    elif response.status_code == 401:
        print("ERROR: API Key is INVALID or EXPIRED")
        print(f"Error: {response.text[:200]}")
        sys.exit(1)
    else:
        print(f"Request failed: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        sys.exit(1)
except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)

