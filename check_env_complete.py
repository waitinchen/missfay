"""Check .env file completeness"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  Check .env File Completeness")
print("=" * 70)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# Force load
from dotenv import load_dotenv
load_dotenv(env_path, override=True)

# Manual load (handle BOM)
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
except Exception as e:
    print(f"   [!] Manual load failed: {e}")

print("[1] Check CARTESIA_API_KEY")
print("-" * 70)
cartesia_key = os.getenv("CARTESIA_API_KEY")
if cartesia_key:
    key_length = len(cartesia_key)
    print(f"   Key length: {key_length} characters")
    print(f"   Key preview: {cartesia_key[:15]}...{cartesia_key[-5:] if len(cartesia_key) > 20 else ''}")
    
    # Check if length is reasonable
    if key_length < 30:
        print(f"   [X] WARNING: Key length is unusually short ({key_length} chars), may be incomplete!")
        print(f"   Suggestion: Cartesia API Keys are usually longer. Please check play.cartesia.ai")
    elif key_length > 200:
        print(f"   [X] WARNING: Key length is unusually long ({key_length} chars), may contain extra content")
    else:
        print(f"   [OK] Key length looks normal")
else:
    print("   [X] CARTESIA_API_KEY not found")

print()
print("[2] Check LONG_TERM_MEMORY_PATH")
print("-" * 70)
memory_path = os.getenv("LONG_TERM_MEMORY_PATH")
if memory_path:
    print(f"   [OK] LONG_TERM_MEMORY_PATH configured: {memory_path}")
    if os.path.exists(memory_path):
        print(f"   [OK] File exists")
    else:
        print(f"   [X] File not found: {memory_path}")
else:
    print("   [X] LONG_TERM_MEMORY_PATH not configured")
    print("   Suggestion: Add LONG_TERM_MEMORY_PATH=C:\\Users\\waiti\\missfay\\k\\FAY024.md")

print()
print("[3] Check Other Configurations")
print("-" * 70)
gemini_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL")
proxy_port = os.getenv("PROXY_PORT")

if gemini_key:
    print(f"   [OK] GEMINI_API_KEY configured")
else:
    print("   [X] GEMINI_API_KEY not configured")

if gemini_model:
    print(f"   [OK] GEMINI_MODEL configured: {gemini_model}")
else:
    print("   [!] GEMINI_MODEL not configured (will use default)")

if proxy_port:
    print(f"   [OK] PROXY_PORT configured: {proxy_port}")
else:
    print("   [!] PROXY_PORT not configured (will use default 8001)")

print()
print("=" * 70)
print("  Check Complete")
print("=" * 70)
print()

