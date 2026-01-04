"""
测试 FAY Voice ID: a5a8b420-9360-4145-9c1e-db4ede8e4b15
"""

import os
import sys

# 设置 UTF-8 编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dotenv import load_dotenv
load_dotenv()

FAY_VOICE_ID = "a5a8b420-9360-4145-9c1e-db4ede8e4b15"
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

print("=" * 60)
print("测试 FAY Voice ID")
print("=" * 60)
print()

print(f"目标 Voice ID: {FAY_VOICE_ID}")
print(f"当前环境变量 CARTESIA_VOICE_ID: {os.getenv('CARTESIA_VOICE_ID', '未设置')}")
print()

if not CARTESIA_API_KEY:
    print("[ERROR] CARTESIA_API_KEY 未设置")
    sys.exit(1)

try:
    from cartesia import Cartesia
    
    print("正在初始化 Cartesia 客户端...")
    client = Cartesia(api_key=CARTESIA_API_KEY)
    print("[OK] Cartesia 客户端初始化成功")
    print()
    
    print(f"正在测试 FAY Voice ID: {FAY_VOICE_ID}")
    print("生成测试音频（文本: '你好，我是菲菲'）...")
    print()
    
    # 使用正确的 Cartesia API 调用方式
    tts_args = {
        "model_id": "sonic-multilingual",
        "transcript": "你好，我是菲菲",
        "voice": {"mode": "id", "id": FAY_VOICE_ID},
        "output_format": {
            "container": "mp3",
            "sample_rate": 44100,
            "bit_rate": 128000,
        },
        "language": "zh",
        "generation_config": {
            "speed": 1.0,
            "pitch": 1.0,
        }
    }
    
    audio_stream = client.tts.bytes(**tts_args)
    audio_data = b"".join(audio_stream)
    
    if audio_data and len(audio_data) > 0:
        print(f"[SUCCESS] FAY Voice ID 有效！")
        print(f"   生成的音频大小: {len(audio_data)} 字节")
        print(f"   音频格式: MP3")
        print()
        print("[OK] FAY 声音可以正常使用！")
        print()
        print("=" * 60)
        print("✅ 验证完成")
        print("=" * 60)
        print()
        print("提示:")
        print("1. 确保 .env 文件中 CARTESIA_VOICE_ID=a5a8b420-9360-4145-9c1e-db4ede8e4b15")
        print("2. 如果服务正在运行，需要重启服务才能生效")
        print("3. 重启命令: .\\start_voice_bridge.ps1")
    else:
        print("[WARN] 生成了空音频")
        
except Exception as e:
    error_str = str(e)
    print(f"[ERROR] 测试失败: {error_str}")
    
    if "404" in error_str or "not found" in error_str.lower():
        print("   原因: Voice ID 不存在或无效")
    elif "401" in error_str:
        print("   原因: API Key 无效")
    else:
        print("   原因: 未知错误")
    
    sys.exit(1)

