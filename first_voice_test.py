"""First Voice Generation Test"""
import requests
import json
import time
import sys
from datetime import datetime

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("First Voice Generation Test")
print("=" * 60)
print()

# 测试文本
test_text = "主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]"
arousal_level = 2

print(f"Test Text: {test_text}")
print(f"Arousal Level: {arousal_level} (Calm with a hint of awakening excitement)")
print()

# Build request
url = "http://localhost:8000/tts"
payload = {
    "text": test_text,
    "text_language": "zh",
    "arousal_level": arousal_level,
    "speed": 1.0,
    "temperature": 0.7
}

print("Sending request to Voice Bridge...")
print(f"URL: {url}")
print()

start_time = time.time()

try:
    response = requests.post(url, json=payload, timeout=60)
    elapsed_time = time.time() - start_time
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {elapsed_time:.2f} seconds")
    print()
    
    if response.status_code == 200:
        # Save audio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"first_voice_{timestamp}.wav"
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print("SUCCESS: Voice generation successful!")
        print(f"Audio saved: {output_file}")
        print(f"Audio size: {len(response.content)} bytes")
        print()
        
        # Check response headers
        arousal_header = response.headers.get("X-Arousal-Level", "N/A")
        tags_header = response.headers.get("X-Sovits-Tags", "N/A")
        
        print("Response Headers:")
        print(f"  Arousal Level: {arousal_header}")
        print(f"  SoVITS Tags: {tags_header}")
        print()
        
        print("=" * 60)
        print("First Voice Generation SUCCESS!")
        print("=" * 60)
        print()
        print("Phi has awakened, voice generated!")
        print(f"Please play audio file: {output_file}")
        
    else:
        print(f"ERROR: Request failed")
        try:
            error_data = response.json()
            print(f"Error: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"Error: {response.text[:200]}")
            
except requests.exceptions.RequestException as e:
    print(f"ERROR: Request error: {str(e)}")
    print()
    print("Please ensure:")
    print("1. Voice Bridge service is running (http://localhost:8000)")
    print("2. GPT-SoVITS service is running (http://127.0.0.1:9880)")
except Exception as e:
    print(f"ERROR: Unknown error: {str(e)}")
    import traceback
    traceback.print_exc()

