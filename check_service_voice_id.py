"""
检查服务当前使用的 Voice ID
"""

import httpx
import json
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    response = httpx.get("http://localhost:8000/verify-keys", timeout=5.0)
    data = response.json()
    
    voice_id_info = data.get("keys", {}).get("CARTESIA_VOICE_ID", {})
    
    if voice_id_info.get("exists"):
        current_voice_id = voice_id_info.get("value", "N/A")
        is_valid = voice_id_info.get("valid", False)
        
        print("=" * 60)
        print("服务当前使用的 Voice ID")
        print("=" * 60)
        print()
        print(f"Voice ID: {current_voice_id}")
        print(f"状态: {'有效' if is_valid else '无效'}")
        print()
        
        target_voice_id = "a5a8b420-9360-4145-9c1e-db4ede8e4b15"
        
        if current_voice_id == target_voice_id:
            print("✅ 服务已使用 FAY Voice ID")
            print("   无需重启，可以直接使用")
        else:
            print(f"⚠️  服务使用的 Voice ID 不是 FAY")
            print(f"   当前: {current_voice_id}")
            print(f"   目标: {target_voice_id}")
            print()
            print("需要重启服务:")
            print("1. 停止服务: Get-Process | Where-Object {$_.ProcessName -eq 'python'} | Stop-Process -Force")
            print("2. 启动服务: .\\start_voice_bridge.ps1")
    else:
        print("[ERROR] CARTESIA_VOICE_ID 未在服务中设置")
        
except Exception as e:
    print(f"[ERROR] 无法连接到服务: {str(e)}")
    print("   服务可能未运行")

