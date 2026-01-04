"""菲菲 401 错误紧急恢复检查"""
import os
import sys

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("  菲菲 401 错误紧急恢复检查")
print("=" * 60)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# 1. 检查 .env 文件
print("1. 检查 .env 文件...")
if os.path.exists(env_path):
    print(f"  [OK] .env 文件存在: {env_path}")
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_openrouter = "OPENROUTER_API_KEY" in content and "OPENROUTER_API_KEY=" in content
    has_cartesia = "CARTESIA_API_KEY" in content and "CARTESIA_API_KEY=" in content
    
    # 检查是否有实际值
    openrouter_value = None
    cartesia_value = None
    
    for line in content.splitlines():
        if line.strip().startswith("OPENROUTER_API_KEY="):
            value = line.split('=', 1)[1].strip()
            if value and value != "":
                openrouter_value = value
                has_openrouter = True
        elif line.strip().startswith("CARTESIA_API_KEY="):
            value = line.split('=', 1)[1].strip()
            if value and value != "":
                cartesia_value = value
                has_cartesia = True
    
    if has_openrouter and openrouter_value:
        preview = openrouter_value[:20] + "..." if len(openrouter_value) > 20 else openrouter_value
        print(f"  [OK] OPENROUTER_API_KEY 已配置: {preview}")
    else:
        print(f"  [X] OPENROUTER_API_KEY 未配置或为空")
    
    if has_cartesia and cartesia_value:
        preview = cartesia_value[:20] + "..." if len(cartesia_value) > 20 else cartesia_value
        print(f"  [OK] CARTESIA_API_KEY 已配置: {preview}")
    else:
        print(f"  [!] CARTESIA_API_KEY 未配置（可选）")
else:
    print(f"  [X] .env 文件不存在: {env_path}")
    print("  请创建 .env 文件并配置 API Key")
print()

# 2. 检查 voice_bridge.py 的 load_dotenv
print("2. 检查 voice_bridge.py 的 load_dotenv...")
voice_bridge_path = os.path.join(base_dir, "voice_bridge.py")
if os.path.exists(voice_bridge_path):
    with open(voice_bridge_path, 'r', encoding='utf-8') as f:
        bridge_content = f.read()
    
    if "load_dotenv" in bridge_content or "手动加载" in bridge_content or "Manually parsed" in bridge_content:
        print("  [OK] voice_bridge.py 包含环境变量加载逻辑")
    else:
        print("  [X] voice_bridge.py 未找到环境变量加载代码")
else:
    print("  [X] voice_bridge.py 文件不存在")
print()

# 3. 检查 phi_brain.py 的环境变量加载
print("3. 检查 phi_brain.py 的环境变量加载...")
phi_brain_path = os.path.join(base_dir, "phi_brain.py")
if os.path.exists(phi_brain_path):
    with open(phi_brain_path, 'r', encoding='utf-8') as f:
        brain_content = f.read()
    
    if "load_dotenv" in brain_content or "手动加载" in brain_content:
        print("  [OK] phi_brain.py 包含环境变量加载逻辑")
    else:
        print("  [X] phi_brain.py 未找到环境变量加载代码")
else:
    print("  [X] phi_brain.py 文件不存在")
print()

# 4. 检查端口配置
print("4. 检查端口配置...")
print("  Voice Bridge (voice_bridge.py): 端口 8000")
print("  Proxy Layer (phi_proxy_layer.py): 端口 8001")
print("  GPT-SoVITS: 端口 9880")
print()

# 5. 测试环境变量加载
print("5. 测试环境变量加载...")
try:
    # 手动加载 .env
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read().lstrip('\ufeff')
            for line in env_content.splitlines():
                if '=' in line and not line.startswith('#') and line.strip():
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()
    
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    cartesia_key = os.getenv("CARTESIA_API_KEY")
    
    if openrouter_key:
        preview = openrouter_key[:20] + "..." if len(openrouter_key) > 20 else openrouter_key
        print(f"  [OK] OPENROUTER_API_KEY 已加载: {preview}")
    else:
        print("  [X] OPENROUTER_API_KEY 未加载到环境变量")
    
    if cartesia_key:
        preview = cartesia_key[:20] + "..." if len(cartesia_key) > 20 else cartesia_key
        print(f"  [OK] CARTESIA_API_KEY 已加载: {preview}")
    else:
        print("  [!] CARTESIA_API_KEY 未加载（可选）")
except Exception as e:
    print(f"  [X] 环境变量加载失败: {e}")
print()

# 6. 生成重启指令
print("6. 重启服务顺序建议：")
print("  步骤 1: 关闭所有运行中的终端窗口（当前有 2 个 Python 进程）")
print("  步骤 2: 启动 GPT-SoVITS (端口 9880)")
print("          cd GPT-SoVITS-v3lora-20250228\\GPT-SoVITS-v3lora-20250228")
print("          .\\runtime\\python.exe api_v2.py")
print("  步骤 3: 启动 Voice Bridge (端口 8000)")
print("          .\\start_voice_bridge.ps1")
print("  步骤 4: （可选）启动 Proxy Layer (端口 8001)")
print("          python phi_proxy_layer.py")
print()

print("=" * 60)
print("  检查完成")
print("=" * 60)


