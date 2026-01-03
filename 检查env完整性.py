"""检查 .env 文件完整性"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  检查 .env 文件完整性")
print("=" * 70)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# 强制加载
from dotenv import load_dotenv
load_dotenv(env_path, override=True)

# 手动加载（处理 BOM）
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
except Exception as e:
    print(f"   [!] 手动加载失败: {e}")

print("【1】检查 CARTESIA_API_KEY")
print("-" * 70)
cartesia_key = os.getenv("CARTESIA_API_KEY")
if cartesia_key:
    key_length = len(cartesia_key)
    print(f"   Key 长度: {key_length} 字符")
    print(f"   Key 预览: {cartesia_key[:15]}...{cartesia_key[-5:] if len(cartesia_key) > 20 else ''}")
    
    # 检查长度是否合理
    if key_length < 30:
        print(f"   [X] 警告：Key 长度异常短（{key_length} 字符），可能不完整！")
        print(f"   建议：Cartesia API Key 通常更长，请检查是否完整复制")
    elif key_length > 200:
        print(f"   [X] 警告：Key 长度异常长（{key_length} 字符），可能包含多余内容")
    else:
        print(f"   [OK] Key 长度看起来正常")
else:
    print("   [X] CARTESIA_API_KEY 未找到")

print()
print("【2】检查 LONG_TERM_MEMORY_PATH")
print("-" * 70)
memory_path = os.getenv("LONG_TERM_MEMORY_PATH")
if memory_path:
    print(f"   [OK] LONG_TERM_MEMORY_PATH 已配置: {memory_path}")
    if os.path.exists(memory_path):
        print(f"   [OK] 文件存在")
    else:
        print(f"   [X] 文件不存在: {memory_path}")
else:
    print("   [X] LONG_TERM_MEMORY_PATH 未配置")
    print("   建议添加: LONG_TERM_MEMORY_PATH=C:\\Users\\waiti\\missfay\\k\\FAY024.md")

print()
print("【3】检查其他配置")
print("-" * 70)
gemini_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL")
proxy_port = os.getenv("PROXY_PORT")

if gemini_key:
    print(f"   [OK] GEMINI_API_KEY 已配置")
else:
    print("   [X] GEMINI_API_KEY 未配置")

if gemini_model:
    print(f"   [OK] GEMINI_MODEL 已配置: {gemini_model}")
else:
    print("   [!] GEMINI_MODEL 未配置（将使用默认值）")

if proxy_port:
    print(f"   [OK] PROXY_PORT 已配置: {proxy_port}")
else:
    print("   [!] PROXY_PORT 未配置（将使用默认值 8001）")

print()
print("=" * 70)
print("  检查完成")
print("=" * 70)
print()

