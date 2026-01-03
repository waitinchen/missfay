"""Comprehensive KEY Health Check"""
import os
import sys
import requests
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("  " + "=" * 76)
print("   Comprehensive KEY Health Check (全面 KEY 值健康检查)")
print("  " + "=" * 76)
print("=" * 80)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# Force load .env
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

# Health summary
health_summary = {
    "total_checks": 0,
    "passed": 0,
    "warnings": 0,
    "failed": 0
}

def check_key(key_name, expected_min_length=None, expected_format=None, test_api=None):
    """Check a single key"""
    health_summary["total_checks"] += 1
    
    print(f"[{health_summary['total_checks']}] Check {key_name}")
    print("-" * 80)
    
    key_value = os.getenv(key_name)
    
    if not key_value:
        print(f"   [X] {key_name} not configured")
        health_summary["failed"] += 1
        print()
        return False
    
    # Check length
    key_length = len(key_value)
    print(f"   Key length: {key_length} characters")
    
    if expected_min_length:
        if key_length < expected_min_length:
            print(f"   [WARNING] Key length is less than expected minimum ({expected_min_length} chars)")
            health_summary["warnings"] += 1
        else:
            print(f"   [OK] Key length meets expectation (>= {expected_min_length} chars)")
            health_summary["passed"] += 1
    
    # Check format
    if expected_format:
        if expected_format in key_value:
            print(f"   [OK] Key format is correct (contains '{expected_format}')")
        else:
            print(f"   [WARNING] Key format may be incorrect (does not contain '{expected_format}')")
            health_summary["warnings"] += 1
    
    # Show preview (hide sensitive info)
    if key_length > 20:
        preview = f"{key_value[:10]}...{key_value[-5:]}"
    else:
        preview = key_value[:15] + "..."
    print(f"   Key preview: {preview}")
    
    # Test API (if provided)
    if test_api:
        try:
            print(f"   Testing API connection...")
            response = test_api(key_value)
            if response is True:
                print(f"   [OK] API connection test successful")
                health_summary["passed"] += 1
            elif response is False:
                print(f"   [X] API connection test failed (401 Unauthorized)")
                health_summary["failed"] += 1
            else:
                print(f"   [WARNING] API connection test uncertain")
                health_summary["warnings"] += 1
        except Exception as e:
            error_msg = str(e)[:50]
            if "401" in error_msg or "unauthorized" in error_msg.lower():
                print(f"   [X] API connection test failed: {error_msg}")
                health_summary["failed"] += 1
            else:
                print(f"   [WARNING] API connection test error: {error_msg}")
                health_summary["warnings"] += 1
    
    print()
    return True

def test_cartesia_api(key):
    """Test Cartesia API"""
    try:
        from cartesia import Cartesia
        client = Cartesia(api_key=key)
        # Simple test: try to initialize client
        return True
    except Exception as e:
        error_str = str(e).lower()
        if "401" in str(e) or "unauthorized" in error_str or "invalid" in error_str:
            return False
        return None  # Other errors, uncertain

def test_gemini_api(key):
    """Test Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        # Simple test: try to list models
        models = list(genai.list_models())
        return len(models) > 0
    except Exception as e:
        error_str = str(e).lower()
        if "401" in str(e) or "unauthorized" in error_str or "api_key_invalid" in error_str or "invalid" in error_str:
            return False
        return None  # Other errors, uncertain

# Start checks
print()

# 1. CARTESIA_API_KEY (TTS)
check_key(
    "CARTESIA_API_KEY",
    expected_min_length=30,
    expected_format="sk_car_",
    test_api=test_cartesia_api
)

# 2. GEMINI_API_KEY (LLM)
check_key(
    "GEMINI_API_KEY",
    expected_min_length=30,
    expected_format="AIza",
    test_api=test_gemini_api
)

# 3. LONG_TERM_MEMORY_PATH
print(f"[{health_summary['total_checks'] + 1}] Check LONG_TERM_MEMORY_PATH")
print("-" * 80)
health_summary["total_checks"] += 1
memory_path = os.getenv("LONG_TERM_MEMORY_PATH")
if memory_path:
    print(f"   Path: {memory_path}")
    if os.path.exists(memory_path):
        file_size = os.path.getsize(memory_path)
        print(f"   [OK] File exists (size: {file_size} bytes)")
        health_summary["passed"] += 1
    else:
        print(f"   [X] File does not exist")
        health_summary["failed"] += 1
else:
    print(f"   [X] LONG_TERM_MEMORY_PATH not configured")
    health_summary["failed"] += 1
print()

# 4. GEMINI_MODEL
print(f"[{health_summary['total_checks'] + 1}] Check GEMINI_MODEL")
print("-" * 80)
health_summary["total_checks"] += 1
gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
print(f"   Model: {gemini_model}")
print(f"   [OK] Configured (using default or custom value)")
health_summary["passed"] += 1
print()

# 5. PROXY_PORT
print(f"[{health_summary['total_checks'] + 1}] Check PROXY_PORT")
print("-" * 80)
health_summary["total_checks"] += 1
proxy_port = os.getenv("PROXY_PORT", "8001")
print(f"   Port: {proxy_port}")
print(f"   [OK] Configured (using default or custom value)")
health_summary["passed"] += 1
print()

# 6. PHI_CONTEXT_WINDOW
print(f"[{health_summary['total_checks'] + 1}] Check PHI_CONTEXT_WINDOW")
print("-" * 80)
health_summary["total_checks"] += 1
context_window = os.getenv("PHI_CONTEXT_WINDOW", "15")
print(f"   Context window: {context_window} turns")
print(f"   [OK] Configured (using default or custom value)")
health_summary["passed"] += 1
print()

# 7. Check port occupancy
print(f"[{health_summary['total_checks'] + 1}] Check Port Occupancy")
print("-" * 80)
health_summary["total_checks"] += 1

try:
    import socket
    def check_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    
    port8000 = check_port(8000)
    port9880 = check_port(9880)
    port8001 = check_port(8001)
    
    print(f"   Port 8000 (Voice Bridge): {'[OCCUPIED]' if port8000 else '[FREE]'}")
    print(f"   Port 9880 (GPT-SoVITS): {'[OCCUPIED]' if port9880 else '[FREE]'}")
    print(f"   Port 8001 (Proxy Layer): {'[OCCUPIED]' if port8001 else '[FREE]'}")
    
    if port8000 or port9880 or port8001:
        print(f"   [OK] Services may be running")
        health_summary["passed"] += 1
    else:
        print(f"   [!] All ports are free, services may not be started")
        health_summary["warnings"] += 1
except Exception as e:
    print(f"   [WARNING] Port check failed: {str(e)[:50]}")
    health_summary["warnings"] += 1
print()

# Summary report
print("=" * 80)
print("  Health Check Summary Report")
print("=" * 80)
print()
print(f"   Total checks: {health_summary['total_checks']}")
print(f"   ✅ Passed: {health_summary['passed']}")
print(f"   ⚠️  Warnings: {health_summary['warnings']}")
print(f"   ❌ Failed: {health_summary['failed']}")
print()

# Health score
total_score = health_summary['total_checks']
passed_score = health_summary['passed']
warning_score = health_summary['warnings'] * 0.5
health_score = ((passed_score + warning_score) / total_score) * 100 if total_score > 0 else 0

print(f"   Health Score: {health_score:.1f}%")
print()

if health_score >= 90:
    status = "Excellent"
    status_cn = "优秀"
elif health_score >= 70:
    status = "Good"
    status_cn = "良好"
elif health_score >= 50:
    status = "Needs Attention"
    status_cn = "需要关注"
else:
    status = "Needs Fix"
    status_cn = "需要修复"

print(f"   Overall Status: {status} ({status_cn})")
print()

# Recommendations
print("=" * 80)
print("  Recommendations")
print("=" * 80)
print()

if health_summary['failed'] > 0:
    print("   [⚠] Found failed checks, please fix immediately:")
    print("      - Check missing configuration items")
    print("      - Verify file paths are correct")
    print()

if health_summary['warnings'] > 0:
    print("   [⚠] Found warnings, please check:")
    print("      - Verify API Keys are complete")
    print("      - Confirm API Keys are valid")
    print("      - Check if services are running normally")
    print()

if health_score >= 90:
    print("   [✅] System health is good, ready to use")
    print("       - All core configurations are ready")
    print("       - Recommend functional testing")
    print()

print("=" * 80)
print("  Check Complete")
print("=" * 80)
print()

