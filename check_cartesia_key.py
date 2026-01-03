"""Check CARTESIA_API_KEY validity"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  Check CARTESIA_API_KEY")
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

# Check Key
cartesia_key = os.getenv("CARTESIA_API_KEY")

print("[1] Key Existence Check")
print("-" * 70)
if cartesia_key:
    print(f"   [OK] CARTESIA_API_KEY exists")
else:
    print("   [X] CARTESIA_API_KEY not found")
    sys.exit(1)

print()
print("[2] Key Length Check")
print("-" * 70)
key_length = len(cartesia_key)
print(f"   Key length: {key_length} characters")
print(f"   Key bytes: {len(cartesia_key.encode('utf-8'))} bytes")

# Check for invisible chars
if cartesia_key.startswith('\ufeff'):
    print("   [X] BOM character (\\ufeff) found at start")
elif cartesia_key.startswith(' '):
    print("   [X] Leading space found")
else:
    print("   [OK] No leading invisible characters")

if cartesia_key.endswith(' '):
    print("   [X] Trailing space found")
else:
    print("   [OK] No trailing invisible characters")

print()
print("[3] Key Content Check")
print("-" * 70)
if key_length > 20:
    preview = cartesia_key[:10] + "..." + cartesia_key[-10:]
    print(f"   Key preview: {preview}")
else:
    print(f"   Key preview: {cartesia_key}")

print()
print("[4] Test Cartesia API")
print("-" * 70)
try:
    from cartesia import Cartesia
    
    clean_key = cartesia_key.strip().lstrip('\ufeff')
    
    try:
        client = Cartesia(api_key=clean_key)
        print("   [OK] Cartesia client initialized successfully")
        print("   [OK] Cartesia API Key format is correct")
    except Exception as api_error:
        error_str = str(api_error)
        if "401" in error_str or "unauthorized" in error_str.lower():
            print(f"   [X] Cartesia API Key is invalid (401)")
            print(f"   Error: {error_str[:200]}")
        elif "429" in error_str or "quota" in error_str.lower():
            print(f"   [!] Cartesia API Key is valid but quota exceeded (429)")
        else:
            print(f"   [!] Cartesia API error: {error_str[:200]}")
            
except ImportError:
    print("   [X] cartesia package not installed")
except Exception as e:
    print(f"   [X] Test failed: {e}")

print()
print("=" * 70)
print("  Check Complete")
print("=" * 70)
print()

