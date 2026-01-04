"""
测试 CARTESIA_VOICE_ID 是否有效
"""

import os
import sys

# 设置 UTF-8 编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 从环境变量读取
from dotenv import load_dotenv
load_dotenv()

VOICE_ID = os.getenv("CARTESIA_VOICE_ID", "e90c6678-f0d3-4767-9883-5d0ecf5894a8")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

print("=" * 60)
print("测试 CARTESIA_VOICE_ID")
print("=" * 60)
print()

print(f"Voice ID: {VOICE_ID}")
print(f"Voice ID 长度: {len(VOICE_ID)}")
print()

# 1. 检查格式（UUID 格式）
import re
uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
if re.match(uuid_pattern, VOICE_ID, re.IGNORECASE):
    print("[OK] Voice ID 格式有效 (UUID 格式)")
else:
    print("[ERROR] Voice ID 格式无效 (应为 UUID 格式)")
    sys.exit(1)

print()

# 2. 检查 API Key
if not CARTESIA_API_KEY:
    print("[ERROR] CARTESIA_API_KEY 未设置，无法测试 Voice ID")
    sys.exit(1)

print(f"[OK] CARTESIA_API_KEY 已设置 (长度: {len(CARTESIA_API_KEY)})")
print()

# 3. 尝试使用 Cartesia API 验证 Voice ID
try:
    from cartesia import Cartesia
    
    print("正在初始化 Cartesia 客户端...")
    client = Cartesia(api_key=CARTESIA_API_KEY)
    print("[OK] Cartesia 客户端初始化成功")
    print()
    
    # 尝试使用这个 Voice ID 生成一个简单的测试音频
    print(f"正在测试 Voice ID: {VOICE_ID}")
    print("生成测试音频（文本: '你好'）...")
    
    try:
        # 使用正确的 Cartesia API 调用方式
        tts_args = {
            "model_id": "sonic-multilingual",
            "transcript": "你好",
            "voice": {"mode": "id", "id": VOICE_ID},
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
        
        # 收集音频数据
        audio_data = b"".join(audio_stream)
        
        if audio_data and len(audio_data) > 0:
            print(f"[SUCCESS] Voice ID 有效！")
            print(f"   生成的音频大小: {len(audio_data)} 字节")
            print(f"   音频格式: MP3")
            print()
            print("[OK] CARTESIA_VOICE_ID 完全有效，可以正常使用！")
        else:
            print("[WARN] 生成了空音频，但 Voice ID 可能仍然有效")
            
    except Exception as e:
        error_str = str(e)
        print(f"[ERROR] 使用 Voice ID 生成音频时出错")
        print(f"   错误: {error_str}")
        print()
        
        # 分析错误类型
        if "404" in error_str or "not found" in error_str.lower() or "invalid" in error_str.lower():
            print("   原因: Voice ID 不存在或无效")
            print(f"   建议: 请检查 Cartesia 控制台中的 Voice ID 是否正确")
        elif "401" in error_str or "unauthorized" in error_str.lower():
            print("   原因: API Key 无效或权限不足")
        elif "429" in error_str:
            print("   原因: 请求频率过高（429）")
        else:
            print("   原因: 未知错误，请检查网络连接和 API 配置")
        
        sys.exit(1)
        
except ImportError:
    print("[ERROR] cartesia 包未安装")
    print("   请运行: pip install cartesia")
    sys.exit(1)
    
except Exception as e:
    error_str = str(e)
    print(f"[ERROR] Cartesia 客户端初始化失败")
    print(f"   错误: {error_str}")
    print()
    
    if "401" in error_str or "unauthorized" in error_str.lower():
        print("   原因: CARTESIA_API_KEY 无效或已过期")
    else:
        print("   原因: 未知错误，请检查网络连接和 API Key")
    
    sys.exit(1)

print()
print("=" * 60)
print("测试完成")
print("=" * 60)

