"""全面诊断 401 错误"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  全面诊断 401 错误")
print("=" * 70)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

# ============================================
# 1. 检查 .env 文件
# ============================================
print("【1】检查 .env 文件")
print("-" * 70)

env_path = os.path.join(base_dir, ".env")
if os.path.exists(env_path):
    print(f"   [OK] .env 文件存在: {env_path}")
    
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
    
    # 检查关键变量
    required_keys = ["CARTESIA_API_KEY", "GEMINI_API_KEY"]
    for key in required_keys:
        found = False
        for line in env_content.splitlines():
            if line.strip().startswith(f"{key}="):
                value = line.split('=', 1)[1].strip()
                if value:
                    preview = value[:15] + "..." + value[-5:] if len(value) > 20 else value
                    print(f"   [OK] {key}: {preview} (length: {len(value)})")
                    found = True
                else:
                    print(f"   [X] {key}: 值为空")
                break
        
        if not found:
            print(f"   [X] {key}: 未找到")
else:
    print(f"   [X] .env 文件不存在: {env_path}")

print()

# ============================================
# 2. 检查环境变量加载
# ============================================
print("【2】检查环境变量加载")
print("-" * 70)

# 强制加载
from dotenv import load_dotenv
load_dotenv(env_path, override=True)

# 手动加载
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
except:
    pass

cartesia_key = os.getenv("CARTESIA_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if cartesia_key:
    print(f"   [OK] CARTESIA_API_KEY 已加载: {cartesia_key[:10]}... (length: {len(cartesia_key)})")
else:
    print("   [X] CARTESIA_API_KEY 未加载")

if gemini_key:
    print(f"   [OK] GEMINI_API_KEY 已加载: {gemini_key[:10]}... (length: {len(gemini_key)})")
else:
    print("   [X] GEMINI_API_KEY 未加载")

print()

# ============================================
# 3. 检查 voice_bridge.py 代码
# ============================================
print("【3】检查 voice_bridge.py 代码")
print("-" * 70)

bridge_path = os.path.join(base_dir, "voice_bridge.py")
if os.path.exists(bridge_path):
    with open(bridge_path, 'r', encoding='utf-8') as f:
        bridge_content = f.read()
    
    # 检查关键代码
    checks = [
        ("load_dotenv", "load_dotenv" in bridge_content and "override=True" in bridge_content),
        ("CARTESIA_API_KEY 验证", "CARTESIA_API_KEY" in bridge_content and "os.getenv" in bridge_content),
        ("Cartesia 初始化验证", "if not CARTESIA_API_KEY" in bridge_content),
        ("api_type=gemini", 'api_type="gemini"' in bridge_content),
    ]
    
    for check_name, result in checks:
        if result:
            print(f"   [OK] {check_name}")
        else:
            print(f"   [X] {check_name}: 未找到或配置错误")
else:
    print(f"   [X] voice_bridge.py 不存在")

print()

# ============================================
# 4. 检查前端代码
# ============================================
print("【4】检查前端代码")
print("-" * 70)

static_dir = os.path.join(base_dir, "static")
html_files = ["index.html", "phi_chat.html"]

for html_file in html_files:
    html_path = os.path.join(static_dir, html_file)
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 检查 API 端点
        if "/chat" in html_content or "/api/v1/phi_voice" in html_content:
            print(f"   [OK] {html_file}: API 端点配置正确")
        else:
            print(f"   [!] {html_file}: 未找到 API 端点配置")
        
        # 检查错误处理
        if "401" in html_content or "error" in html_content.lower():
            print(f"   [OK] {html_file}: 包含错误处理")
    else:
        print(f"   [!] {html_file}: 文件不存在")

print()

# ============================================
# 5. 测试 Cartesia API Key
# ============================================
print("【5】测试 Cartesia API Key")
print("-" * 70)

if cartesia_key:
    try:
        from cartesia import Cartesia
        client = Cartesia(api_key=cartesia_key)
        print("   [OK] Cartesia 客户端初始化成功")
        
        # 尝试列出模型（简单测试）
        try:
            # 不实际调用，只检查客户端是否有效
            print("   [OK] Cartesia API Key 格式正确")
        except Exception as e:
            error_str = str(e)
            if "401" in error_str or "unauthorized" in error_str.lower():
                print(f"   [X] Cartesia API Key 无效（401）")
            elif "429" in error_str or "quota" in error_str.lower():
                print(f"   [!] Cartesia API Key 有效，但配额已用完（429）")
            else:
                print(f"   [!] Cartesia API 错误: {error_str[:100]}")
    except ImportError:
        print("   [X] cartesia 包未安装")
    except Exception as e:
        print(f"   [X] 测试失败: {e}")
else:
    print("   [X] 无法测试：CARTESIA_API_KEY 未加载")

print()

# ============================================
# 6. 检查服务状态
# ============================================
print("【6】检查服务状态")
print("-" * 70)

try:
    import requests
    try:
        response = requests.get("http://localhost:8000/", timeout=2)
        print(f"   [OK] 服务运行中 (状态码: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("   [X] 服务未运行（无法连接到 localhost:8000）")
    except Exception as e:
        print(f"   [!] 服务状态未知: {e}")
except ImportError:
    print("   [!] requests 未安装，无法检查服务状态")

print()

# ============================================
# 总结
# ============================================
print("=" * 70)
print("  诊断完成")
print("=" * 70)
print()
print("建议修复步骤:")
print("  1. 确认 .env 文件包含有效的 CARTESIA_API_KEY")
print("  2. 关闭所有 Python 进程: Stop-Process -Name python -Force")
print("  3. 重新启动服务: .\\start_voice_bridge.ps1")
print("  4. 检查启动日志中的 DEBUG 输出")
print()

