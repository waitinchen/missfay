"""诊断 401 错误"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  诊断 401 错误")
print("=" * 70)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

# 加载环境变量
env_path = os.path.join(base_dir, ".env")
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

print("1. 检查环境变量...")
print("-" * 70)

gemini_key = os.getenv("GEMINI_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

if gemini_key:
    preview = gemini_key[:20] + "..." + gemini_key[-10:] if len(gemini_key) > 30 else gemini_key
    print(f"   [OK] GEMINI_API_KEY: {preview}")
else:
    print("   [X] GEMINI_API_KEY 未找到")

if openrouter_key:
    preview = openrouter_key[:20] + "..." + openrouter_key[-10:] if len(openrouter_key) > 30 else openrouter_key
    print(f"   [!] OPENROUTER_API_KEY 仍存在: {preview}")
else:
    print("   [OK] OPENROUTER_API_KEY 不存在（已迁移）")

print()
print("2. 检查 phi_brain.py 配置...")
print("-" * 70)

try:
    with open(os.path.join(base_dir, "phi_brain.py"), 'r', encoding='utf-8') as f:
        brain_content = f.read()
    
    default_api = "api_type: str = \"gemini\"" in brain_content or 'api_type="gemini"' in brain_content
    if default_api:
        print("   [OK] phi_brain.py 默认使用 Gemini")
    else:
        print("   [X] phi_brain.py 可能仍使用旧配置")
        
except Exception as e:
    print(f"   [X] 检查失败: {e}")

print()
print("3. 检查 voice_bridge.py 配置...")
print("-" * 70)

try:
    with open(os.path.join(base_dir, "voice_bridge.py"), 'r', encoding='utf-8') as f:
        bridge_content = f.read()
    
    uses_gemini = "api_type=\"gemini\"" in bridge_content or "api_type='gemini'" in bridge_content
    if uses_gemini:
        print("   [OK] voice_bridge.py 使用 Gemini")
    else:
        print("   [X] voice_bridge.py 可能仍使用旧配置")
        
    # 检查是否有 OPENROUTER_API_KEY 检查
    has_openrouter_check = "OPENROUTER_API_KEY" in bridge_content
    if has_openrouter_check:
        print("   [!] voice_bridge.py 中仍有 OPENROUTER_API_KEY 检查（可能需要清理）")
        
except Exception as e:
    print(f"   [X] 检查失败: {e}")

print()
print("4. 测试 Gemini API Key...")
print("-" * 70)

try:
    import google.generativeai as genai
    
    if gemini_key:
        genai.configure(api_key=gemini_key)
        
        # 尝试列出模型
        try:
            models = list(genai.list_models())
            print("   [OK] Gemini API Key 有效，可以访问 API")
        except Exception as api_error:
            error_str = str(api_error)
            if "429" in error_str or "quota" in error_str.lower():
                print("   [!] Gemini API Key 有效，但配额已用完（429）")
            elif "401" in error_str or "unauthorized" in error_str.lower():
                print("   [X] Gemini API Key 无效（401）")
            else:
                print(f"   [!] Gemini API 错误: {error_str[:100]}")
    else:
        print("   [X] 无法测试：GEMINI_API_KEY 未找到")
        
except ImportError:
    print("   [X] google-generativeai 未安装")
except Exception as e:
    print(f"   [X] 测试失败: {e}")

print()
print("=" * 70)
print("  诊断完成")
print("=" * 70)
print()
print("建议：")
print("  1. 如果服务正在运行，请重启服务")
print("  2. 确认 GEMINI_API_KEY 有效且未超配额")
print("  3. 检查 voice_bridge.py 是否已更新为使用 Gemini")
print()


