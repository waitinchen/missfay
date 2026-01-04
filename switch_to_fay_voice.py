"""
切换到 FAY 声音
"""

import os
import sys
import re

# 设置 UTF-8 编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dotenv import load_dotenv
load_dotenv()

env_file = ".env"
fay_voice_id = "a5a8b420-9360-4145-9c1e-db4ede8e4b15"  # FAY 声音

print("=" * 60)
print("切换到 FAY 声音")
print("=" * 60)
print()

print(f"FAY Voice ID: {fay_voice_id}")
print()

if os.path.exists(env_file):
    # 读取现有内容
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有 CARTESIA_VOICE_ID
    if re.search(r'CARTESIA_VOICE_ID\s*=', content):
        # 替换现有的 Voice ID
        old_match = re.search(r'CARTESIA_VOICE_ID\s*=\s*([^\s\n]+)', content)
        if old_match:
            old_voice_id = old_match.group(1)
            print(f"当前 Voice ID: {old_voice_id}")
        
        content = re.sub(r'CARTESIA_VOICE_ID\s*=.*', f'CARTESIA_VOICE_ID={fay_voice_id}', content)
        print(f"[OK] 已更新 CARTESIA_VOICE_ID 为 FAY 声音")
    else:
        # 添加新的 Voice ID
        content += f'\nCARTESIA_VOICE_ID={fay_voice_id}\n'
        print(f"[OK] 已添加 CARTESIA_VOICE_ID (FAY 声音)")
    
    # 写入文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] .env 文件已更新")
else:
    # 创建新文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(f'CARTESIA_VOICE_ID={fay_voice_id}\n')
    print("[OK] 已创建 .env 文件")

print()
print("=" * 60)
print("✅ 已切换到 FAY 声音")
print("=" * 60)
print()
print("下一步:")
print("1. 重启服务: .\\start_voice_bridge.ps1")
print("2. 或者停止当前服务并重新启动")
print("3. 测试新的声音")
print()

