"""Update .env file with missing configuration items"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  Update .env File Configuration")
print("=" * 70)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# Read existing content
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read().lstrip('\ufeff')
else:
    content = ""

# Check and add missing configurations
updates = []

# 1. LONG_TERM_MEMORY_PATH
if "LONG_TERM_MEMORY_PATH" not in content:
    memory_path = r"C:\Users\waiti\missfay\k\FAY024.md"
    updates.append(f"LONG_TERM_MEMORY_PATH={memory_path}")
    print(f"   [+] Adding LONG_TERM_MEMORY_PATH={memory_path}")

# 2. GEMINI_MODEL (optional, if not exists)
if "GEMINI_MODEL" not in content:
    updates.append("GEMINI_MODEL=gemini-2.0-flash-exp")
    print(f"   [+] Adding GEMINI_MODEL=gemini-2.0-flash-exp")

# 3. PROXY_PORT (optional, if not exists)
if "PROXY_PORT" not in content:
    updates.append("PROXY_PORT=8001")
    print(f"   [+] Adding PROXY_PORT=8001")

# Write updates
if updates:
    if content and not content.endswith('\n'):
        content += '\n'
    content += "\n# Phi's Diagnostic Additional Configuration\n"
    for update in updates:
        content += update + "\n"
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print()
    print("   [OK] .env file updated")
else:
    print("   [OK] All configuration items exist, no update needed")

print()
print("=" * 70)
print("  Complete")
print("=" * 70)
print()

