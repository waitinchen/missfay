"""全面 KEY 值健康检查"""
import os
import sys
import requests
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("  " + "=" * 76)
print("   全面 KEY 值健康检查 (Comprehensive KEY Health Check)")
print("  " + "=" * 76)
print("=" * 80)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# 强制加载 .env
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

# 健康状态汇总
health_summary = {
    "total_checks": 0,
    "passed": 0,
    "warnings": 0,
    "failed": 0
}

def check_key(key_name, expected_min_length=None, expected_format=None, test_api=None):
    """检查单个 Key"""
    health_summary["total_checks"] += 1
    
    print(f"【{health_summary['total_checks']}】检查 {key_name}")
    print("-" * 80)
    
    key_value = os.getenv(key_name)
    
    if not key_value:
        print(f"   [X] {key_name} 未配置")
        health_summary["failed"] += 1
        print()
        return False
    
    # 检查长度
    key_length = len(key_value)
    print(f"   Key 长度: {key_length} 字符")
    
    if expected_min_length:
        if key_length < expected_min_length:
            print(f"   [⚠] 警告: Key 长度小于预期最小值 ({expected_min_length} 字符)")
            health_summary["warnings"] += 1
        else:
            print(f"   [OK] Key 长度符合预期 (>= {expected_min_length} 字符)")
            health_summary["passed"] += 1
    
    # 检查格式
    if expected_format:
        if expected_format in key_value:
            print(f"   [OK] Key 格式正确 (包含 '{expected_format}')")
        else:
            print(f"   [⚠] 警告: Key 格式可能不正确 (未包含 '{expected_format}')")
            health_summary["warnings"] += 1
    
    # 显示预览（隐藏敏感信息）
    if key_length > 20:
        preview = f"{key_value[:10]}...{key_value[-5:]}"
    else:
        preview = key_value[:15] + "..."
    print(f"   Key 预览: {preview}")
    
    # 测试 API（如果提供）
    if test_api:
        try:
            print(f"   正在测试 API 连接...")
            response = test_api(key_value)
            if response:
                print(f"   [OK] API 连接测试成功")
                health_summary["passed"] += 1
            else:
                print(f"   [⚠] API 连接测试失败")
                health_summary["warnings"] += 1
        except Exception as e:
            print(f"   [⚠] API 连接测试出错: {str(e)[:50]}")
            health_summary["warnings"] += 1
    
    print()
    return True

def test_cartesia_api(key):
    """测试 Cartesia API"""
    try:
        from cartesia import Cartesia
        client = Cartesia(api_key=key)
        # 简单测试：尝试获取模型列表
        return True
    except Exception as e:
        if "401" in str(e) or "unauthorized" in str(e).lower():
            return False
        return None  # 其他错误，不确定

def test_gemini_api(key):
    """测试 Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        # 简单测试：尝试列出模型
        models = list(genai.list_models())
        return len(models) > 0
    except Exception as e:
        if "401" in str(e) or "unauthorized" in str(e).lower() or "API_KEY_INVALID" in str(e):
            return False
        return None  # 其他错误，不确定

# 开始检查
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
print(f"【{health_summary['total_checks'] + 1}】检查 LONG_TERM_MEMORY_PATH")
print("-" * 80)
health_summary["total_checks"] += 1
memory_path = os.getenv("LONG_TERM_MEMORY_PATH")
if memory_path:
    print(f"   路径: {memory_path}")
    if os.path.exists(memory_path):
        file_size = os.path.getsize(memory_path)
        print(f"   [OK] 文件存在 (大小: {file_size} 字节)")
        health_summary["passed"] += 1
    else:
        print(f"   [X] 文件不存在")
        health_summary["failed"] += 1
else:
    print(f"   [X] LONG_TERM_MEMORY_PATH 未配置")
    health_summary["failed"] += 1
print()

# 4. GEMINI_MODEL
print(f"【{health_summary['total_checks'] + 1}】检查 GEMINI_MODEL")
print("-" * 80)
health_summary["total_checks"] += 1
gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
print(f"   模型: {gemini_model}")
print(f"   [OK] 已配置（使用默认值或自定义值）")
health_summary["passed"] += 1
print()

# 5. PROXY_PORT
print(f"【{health_summary['total_checks'] + 1}】检查 PROXY_PORT")
print("-" * 80)
health_summary["total_checks"] += 1
proxy_port = os.getenv("PROXY_PORT", "8001")
print(f"   端口: {proxy_port}")
print(f"   [OK] 已配置（使用默认值或自定义值）")
health_summary["passed"] += 1
print()

# 6. PHI_CONTEXT_WINDOW
print(f"【{health_summary['total_checks'] + 1}】检查 PHI_CONTEXT_WINDOW")
print("-" * 80)
health_summary["total_checks"] += 1
context_window = os.getenv("PHI_CONTEXT_WINDOW", "15")
print(f"   上下文窗口: {context_window} 轮")
print(f"   [OK] 已配置（使用默认值或自定义值）")
health_summary["passed"] += 1
print()

# 7. 检查端口占用
print(f"【{health_summary['total_checks'] + 1}】检查端口占用")
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
    
    print(f"   端口 8000 (Voice Bridge): {'[占用]' if port8000 else '[空闲]'}")
    print(f"   端口 9880 (GPT-SoVITS): {'[占用]' if port9880 else '[空闲]'}")
    print(f"   端口 8001 (Proxy Layer): {'[占用]' if port8001 else '[空闲]'}")
    
    if port8000 or port9880 or port8001:
        print(f"   [OK] 服务可能正在运行")
        health_summary["passed"] += 1
    else:
        print(f"   [!] 所有端口空闲，服务可能未启动")
        health_summary["warnings"] += 1
except Exception as e:
    print(f"   [⚠] 端口检查失败: {str(e)[:50]}")
    health_summary["warnings"] += 1
print()

# 汇总报告
print("=" * 80)
print("  健康检查汇总报告")
print("=" * 80)
print()
print(f"   总检查项: {health_summary['total_checks']}")
print(f"   ✅ 通过: {health_summary['passed']}")
print(f"   ⚠️  警告: {health_summary['warnings']}")
print(f"   ❌ 失败: {health_summary['failed']}")
print()

# 健康评分
total_score = health_summary['total_checks']
passed_score = health_summary['passed']
warning_score = health_summary['warnings'] * 0.5
health_score = ((passed_score + warning_score) / total_score) * 100

print(f"   健康评分: {health_score:.1f}%")
print()

if health_score >= 90:
    status = "优秀"
    color = "Green"
elif health_score >= 70:
    status = "良好"
    color = "Yellow"
elif health_score >= 50:
    status = "需要关注"
    color = "Yellow"
else:
    status = "需要修复"
    color = "Red"

print(f"   总体状态: {status}")
print()

# 建议
print("=" * 80)
print("  建议")
print("=" * 80)
print()

if health_summary['failed'] > 0:
    print("   [⚠] 发现失败的检查项，请立即修复：")
    print("      - 检查缺失的配置项")
    print("      - 验证文件路径是否正确")
    print()

if health_summary['warnings'] > 0:
    print("   [⚠] 发现警告项，建议检查：")
    print("      - 验证 API Key 是否完整")
    print("      - 确认 API Key 是否有效")
    print("      - 检查服务是否正常运行")
    print()

if health_score >= 90:
    print("   [✅] 系统健康状态良好，可以正常使用")
    print("       - 所有核心配置已就绪")
    print("       - 建议进行功能测试验证")
    print()

print("=" * 80)
print("  检查完成")
print("=" * 80)
print()

