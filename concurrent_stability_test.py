import requests
import threading
import time
import sys
import io
from datetime import datetime

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

results = []
lock = threading.Lock()
errors = []

def send_request(request_id):
    url = "http://localhost:8000/tts"
    payload = {
        "text": f"撟嗅?瘚?霂瑟? {request_id}",
        "text_language": "zh",
        "arousal_level": 2
    }
    
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=30)
        elapsed = time.time() - start_time
        
        with lock:
            results.append({
                "id": request_id,
                "status": response.status_code,
                "time": elapsed,
                "success": response.status_code == 200,
                "size": len(response.content) if response.status_code == 200 else 0
            })
    except Exception as e:
        elapsed = time.time() - start_time
        with lock:
            errors.append({
                "id": request_id,
                "error": str(e),
                "time": elapsed
            })

print("Sending 3 concurrent requests...")
print()

# Start 3 concurrent requests
threads = []
for i in range(1, 4):
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()

# Report results
print("=" * 60)
print("Concurrent Test Results")
print("=" * 60)
print()

all_pass = True
for result in results:
    status_icon = "[PASS]" if result["success"] else "[FAIL]"
    print(f"{status_icon} Request {result['id']}: {result['time']:.2f}s (Status: {result['status']}, Size: {result['size']} bytes)")

for error in errors:
    print(f"[FAIL] Request {error['id']}: Error after {error['time']:.2f}s - {error['error']}")
    all_pass = False

print()

if len(results) == 3 and all(result["success"] for result in results):
    print("PASS: All 3 concurrent requests succeeded")
    print("PASS: No memory overflow or crash detected")
    sys.exit(0)
else:
    print("FAIL: Some requests failed or system crashed")
    sys.exit(1)
