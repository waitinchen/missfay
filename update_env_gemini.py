"""更新 .env 文件，添加 GEMINI_API_KEY"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

gemini_key = "AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo"

print("=" * 60)
print("  更新 .env 文件 - 添加 GEMINI_API_KEY")
print("=" * 60)
print()

if os.path.exists(env_path):
    print(f"[OK] .env 文件存在: {env_path}")
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "GEMINI_API_KEY" in content:
        # 检查是否需要更新
        lines = content.splitlines()
        updated = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("GEMINI_API_KEY="):
                new_lines.append(f"GEMINI_API_KEY={gemini_key}")
                updated = True
            else:
                new_lines.append(line)
        
        if updated:
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            print("[OK] 已更新 GEMINI_API_KEY")
        else:
            print("[OK] GEMINI_API_KEY 已存在")
    else:
        # 添加 GEMINI_API_KEY
        if content and not content.endswith('\n'):
            content += '\n'
        content += f"\n# Google Gemini API Key\nGEMINI_API_KEY={gemini_key}\n"
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("[OK] 已添加 GEMINI_API_KEY")
else:
    print(f"[!] .env 文件不存在，正在创建...")
    content = f"""# Google Gemini API Key
GEMINI_API_KEY={gemini_key}
"""
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] 已创建 .env 文件并添加 GEMINI_API_KEY")

print()
print("=" * 60)
print("  完成")
print("=" * 60)


