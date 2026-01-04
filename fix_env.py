"""修复 .env 文件，确保 OPENROUTER_API_KEY 正确配置"""
import os
import sys

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

api_key = "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"

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

print("=" * 60)
print("修复 .env 文件配置")
print("=" * 60)
print()

# 检查文件是否存在
if os.path.exists(env_path):
    print(f"✓ 找到 .env 文件: {env_path}")
    
    # 读取现有内容
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有 API Key
    if f"OPENROUTER_API_KEY={api_key}" in content:
        print("✓ OPENROUTER_API_KEY 已正确配置")
    else:
        # 检查是否有其他值
        if "OPENROUTER_API_KEY=" in content:
            print("⚠ 发现 OPENROUTER_API_KEY，但值可能不正确，将更新...")
            # 替换现有的 API Key 行
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if line.strip().startswith("OPENROUTER_API_KEY="):
                    new_lines.append(f"OPENROUTER_API_KEY={api_key}")
                else:
                    new_lines.append(line)
            content = "\n".join(new_lines)
        else:
            print("⚠ 未找到 OPENROUTER_API_KEY，将添加...")
            # 添加 API Key
            if content and not content.endswith("\n"):
                content += "\n"
            content += f"\n# OpenRouter API Key\nOPENROUTER_API_KEY={api_key}\n"
        
        # 写入文件
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ 已更新 .env 文件")
else:
    print(f"⚠ .env 文件不存在，正在创建...")
    # 创建新的 .env 文件
    env_content = f"""# Phi 系统环境变量配置

# OpenRouter API Key
OPENROUTER_API_KEY={api_key}

# OpenRouter 模型配置
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct:nitro

# GPT-SoVITS 配置
GPT_SOVITS_URL=http://127.0.0.1:9880
GPT_SOVITS_API_VERSION=v2

# Cartesia TTS 配置（如果需要）
CARTESIA_API_KEY=

# 记忆窗口配置（可选）
PHI_CONTEXT_WINDOW=15
"""
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✓ 已创建 .env 文件")

print()
print("=" * 60)
print("验证配置...")
print("=" * 60)

# 验证
from dotenv import load_dotenv
load_dotenv(env_path, override=True)

loaded_key = os.getenv("OPENROUTER_API_KEY")
if loaded_key == api_key:
    print("✓ OPENROUTER_API_KEY 已正确加载")
    print(f"  值: {loaded_key[:20]}...{loaded_key[-10:]}")
else:
    print("⚠ 警告: OPENROUTER_API_KEY 加载失败或不匹配")
    if loaded_key:
        print(f"  当前值: {loaded_key[:20]}...{loaded_key[-10:]}")
    else:
        print("  当前值: None")

print()
print("完成！请重启 Voice Bridge 服务以使配置生效。")


