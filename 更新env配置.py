"""更新 .env 文件，添加缺失的配置项"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  更新 .env 文件配置")
print("=" * 70)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# 读取现有内容
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read().lstrip('\ufeff')
else:
    content = ""

# 检查并添加缺失的配置
updates = []

# 1. LONG_TERM_MEMORY_PATH
if "LONG_TERM_MEMORY_PATH" not in content:
    memory_path = r"C:\Users\waiti\missfay\k\FAY024.md"
    updates.append(f"LONG_TERM_MEMORY_PATH={memory_path}")
    print(f"   [+] 添加 LONG_TERM_MEMORY_PATH={memory_path}")

# 2. GEMINI_MODEL (可选，如果不存在)
if "GEMINI_MODEL" not in content:
    updates.append("GEMINI_MODEL=gemini-2.0-flash-exp")
    print(f"   [+] 添加 GEMINI_MODEL=gemini-2.0-flash-exp")

# 3. PROXY_PORT (可选，如果不存在)
if "PROXY_PORT" not in content:
    updates.append("PROXY_PORT=8001")
    print(f"   [+] 添加 PROXY_PORT=8001")

# 写入更新
if updates:
    if content and not content.endswith('\n'):
        content += '\n'
    content += "\n# 菲菲的诊断补充配置\n"
    for update in updates:
        content += update + "\n"
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print()
    print("   [OK] .env 文件已更新")
else:
    print("   [OK] 所有配置项已存在，无需更新")

print()
print("=" * 70)
print("  完成")
print("=" * 70)
print()


