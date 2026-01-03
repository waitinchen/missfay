import requests
import time
import threading
from datetime import datetime

results = []
lock = threading.Lock()

def send_request(request_id):
    url = "http://localhost:8000/tts"
    payload = {
        "text": f"瘚?霂瑟? {request_id}",
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
                "success": response.status_code == 200
            })
    except Exception as e:
        elapsed = time.time() - start_time
        with lock:
            results.append({
                "id": request_id,
                "status": "ERROR",
                "time": elapsed,
                "success": False,
                "error": str(e)
            })

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
print("Performance Test Results")
print("=" * 60)
print()

all_pass = True
for result in results:
    status_icon = "[PASS]" if result["success"] else "[FAIL]"
    print(f"{status_icon} Request {result['id']}: {result['time']:.2f}s (Status: {result['status']})")
    
    if result["time"] > 2.0:
        print(f"  WARN: Response time {result['time']:.2f}s exceeds 2s threshold")
        all_pass = False
    elif not result["success"]:
        all_pass = False

print()
if all_pass:
    print("PASS: All requests completed within 2s threshold")
    exit(0)
else:
    print("FAIL: Some requests failed or exceeded threshold")
    exit(1)
