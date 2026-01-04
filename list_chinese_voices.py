"""
列出 Cartesia 中所有中文 (zh) 声音
"""

import os
import sys

# 设置 UTF-8 编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dotenv import load_dotenv
load_dotenv()

CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

if not CARTESIA_API_KEY:
    print("[ERROR] CARTESIA_API_KEY 未设置")
    sys.exit(1)

print("=" * 60)
print("Cartesia 中文 (zh) 声音列表")
print("=" * 60)
print()

try:
    from cartesia import Cartesia
    
    client = Cartesia(api_key=CARTESIA_API_KEY)
    voices = list(client.voices.list())
    
    # 筛选中文声音
    zh_voices = []
    for v in voices:
        if isinstance(v, dict):
            lang = v.get("language", "")
        else:
            lang = getattr(v, "language", "")
        
        if lang == "zh":
            zh_voices.append(v)
    
    if not zh_voices:
        print("[WARN] 未找到中文声音")
        print("   当前使用的可能是英文声音")
    else:
        print(f"找到 {len(zh_voices)} 个中文声音:\n")
        
        for i, voice in enumerate(zh_voices, 1):
            if isinstance(voice, dict):
                voice_id = voice.get("id", "N/A")
                name = voice.get("name", voice.get("voice_name", "N/A"))
                description = voice.get("description", "")
            else:
                voice_id = getattr(voice, "id", "N/A")
                name = getattr(voice, "name", getattr(voice, "voice_name", "N/A"))
                description = getattr(voice, "description", "")
            
            print(f"{i}. {name}")
            print(f"   Voice ID: {voice_id}")
            if description:
                print(f"   描述: {description}")
            print()
        
        # 显示当前使用的 Voice ID
        current_voice_id = os.getenv("CARTESIA_VOICE_ID", "e90c6678-f0d3-4767-9883-5d0ecf5894a8")
        print("=" * 60)
        print(f"当前使用的 Voice ID: {current_voice_id}")
        
        # 检查当前 Voice ID 是否是中文
        current_voice = None
        for v in voices:
            v_id = v.get("id") if isinstance(v, dict) else getattr(v, "id", None)
            if v_id == current_voice_id:
                current_voice = v
                break
        
        if current_voice:
            if isinstance(current_voice, dict):
                lang = current_voice.get("language", "")
                name = current_voice.get("name", "N/A")
            else:
                lang = getattr(current_voice, "language", "")
                name = getattr(current_voice, "name", "N/A")
            
            if lang == "zh":
                print(f"✅ 当前声音是中文: {name}")
            else:
                print(f"⚠️  当前声音不是中文: {name} (语言: {lang})")
                print(f"   建议: 从上面的列表中选择一个中文 Voice ID")
        
        print()
        print("=" * 60)
        print("如何更换 Voice ID:")
        print("1. 从上面的列表中选择一个中文 Voice ID")
        print("2. 更新 .env 文件: CARTESIA_VOICE_ID=<新的Voice ID>")
        print("3. 或者在 Railway 环境变量中更新 CARTESIA_VOICE_ID")
        print("4. 重启服务")
        print("=" * 60)
        
except Exception as e:
    print(f"[ERROR] {str(e)}")
    sys.exit(1)

