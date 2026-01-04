"""
列出 Cartesia 中所有可用的 Voice ID
"""

import os
import sys
import json

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
print("列出 Cartesia 可用的 Voice ID")
print("=" * 60)
print()

try:
    from cartesia import Cartesia
    
    print("正在初始化 Cartesia 客户端...")
    client = Cartesia(api_key=CARTESIA_API_KEY)
    print("[OK] Cartesia 客户端初始化成功")
    print()
    
    print("正在获取可用的 Voices...")
    try:
        # 尝试获取 voices 列表（返回的是 SyncPager，需要迭代）
        voices_pager = client.voices.list()
        voices = list(voices_pager)  # 转换为列表
        
        print(f"[OK] 找到 {len(voices)} 个可用的 Voice")
        print()
        print("=" * 60)
        print("可用的 Voice ID 列表:")
        print("=" * 60)
        print()
        
        for i, voice in enumerate(voices, 1):
            # 处理不同的 voice 对象格式
            if isinstance(voice, dict):
                voice_id = voice.get("id", "N/A")
                name = voice.get("name", voice.get("voice_name", "N/A"))
                description = voice.get("description", "")
                language = voice.get("language", "N/A")
            else:
                # 如果是对象，尝试访问属性
                voice_id = getattr(voice, "id", "N/A")
                name = getattr(voice, "name", getattr(voice, "voice_name", "N/A"))
                description = getattr(voice, "description", "")
                language = getattr(voice, "language", "N/A")
            
            print(f"{i}. Voice ID: {voice_id}")
            print(f"   名称: {name}")
            if description:
                print(f"   描述: {description}")
            if language and language != "N/A":
                print(f"   语言: {language}")
            print()
        
        # 显示当前使用的 Voice ID
        current_voice_id = os.getenv("CARTESIA_VOICE_ID", "e90c6678-f0d3-4767-9883-5d0ecf5894a8")
        print("=" * 60)
        print(f"当前使用的 Voice ID: {current_voice_id}")
        
        # 检查当前 Voice ID 是否在列表中
        voice_ids = []
        for v in voices:
            if isinstance(v, dict):
                voice_ids.append(v.get("id"))
            else:
                voice_ids.append(getattr(v, "id", None))
        
        if current_voice_id in voice_ids:
            current_voice = None
            for v in voices:
                v_id = v.get("id") if isinstance(v, dict) else getattr(v, "id", None)
                if v_id == current_voice_id:
                    current_voice = v
                    break
            
            if current_voice:
                print(f"✅ 当前 Voice ID 有效")
                if isinstance(current_voice, dict):
                    print(f"   名称: {current_voice.get('name', current_voice.get('voice_name', 'N/A'))}")
                    print(f"   描述: {current_voice.get('description', 'N/A')}")
                else:
                    print(f"   名称: {getattr(current_voice, 'name', getattr(current_voice, 'voice_name', 'N/A'))}")
                    print(f"   描述: {getattr(current_voice, 'description', 'N/A')}")
        else:
            print(f"⚠️  当前 Voice ID 不在可用列表中")
            print(f"   建议: 请从上面的列表中选择一个正确的 Voice ID")
        
        print()
        print("=" * 60)
        print("提示: 如果声音不对，请:")
        print("1. 从上面的列表中找到正确的 Voice ID")
        print("2. 更新 .env 文件中的 CARTESIA_VOICE_ID")
        print("3. 或者在 Railway 环境变量中更新 CARTESIA_VOICE_ID")
        print("=" * 60)
        
    except AttributeError:
        # 如果 client.voices.list() 不存在，尝试其他方法
        print("[WARN] 无法直接列出 voices，尝试其他方法...")
        print()
        print("请访问 Cartesia 控制台查看可用的 Voice ID:")
        print("https://play.cartesia.ai/")
        print()
        print("或者，您可以:")
        print("1. 登录 Cartesia 控制台")
        print("2. 查看 'Voices' 或 'My Voices' 部分")
        print("3. 找到您想要的声音，复制其 Voice ID")
        print("4. 更新环境变量 CARTESIA_VOICE_ID")
        
    except Exception as e:
        error_str = str(e)
        print(f"[ERROR] 获取 voices 列表失败: {error_str}")
        print()
        print("请尝试以下方法:")
        print("1. 访问 Cartesia 控制台: https://play.cartesia.ai/")
        print("2. 查看 'Voices' 或 'My Voices' 部分")
        print("3. 找到您想要的声音，复制其 Voice ID")
        print("4. 更新环境变量 CARTESIA_VOICE_ID")
        
except ImportError:
    print("[ERROR] cartesia 包未安装")
    print("   请运行: pip install cartesia")
    sys.exit(1)
    
except Exception as e:
    error_str = str(e)
    print(f"[ERROR] Cartesia 客户端初始化失败")
    print(f"   错误: {error_str}")
    
    if "401" in error_str or "unauthorized" in error_str.lower():
        print("   原因: CARTESIA_API_KEY 无效或已过期")
    else:
        print("   原因: 未知错误，请检查网络连接和 API Key")
    
    sys.exit(1)

