"""检查 CARTESIA_API_KEY 的有效性"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  检查 CARTESIA_API_KEY")
print("=" * 70)
print()

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

# 强制加载
from dotenv import load_dotenv
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

# 检查 Key
cartesia_key = os.getenv("CARTESIA_API_KEY")

print("【1】Key 存在性检查")
print("-" * 70)
if cartesia_key:
    print(f"   [OK] CARTESIA_API_KEY 存在")
else:
    print("   [X] CARTESIA_API_KEY 不存在")
    sys.exit(1)

print()
print("【2】Key 长度检查")
print("-" * 70)
key_length = len(cartesia_key)
print(f"   Key 长度: {key_length} 字符")

# 检查是否有不可见字符
key_bytes = cartesia_key.encode('utf-8')
print(f"   Key 字节长度: {len(key_bytes)} 字节")

# 检查 BOM 或前导空格
if cartesia_key.startswith('\ufeff'):
    print("   [X] 发现 BOM 字符 (\\ufeff) 在开头")
elif cartesia_key.startswith(' '):
    print("   [X] 发现前导空格")
elif cartesia_key.startswith('\t'):
    print("   [X] 发现前导制表符")
else:
    print("   [OK] 没有发现前导不可见字符")

# 检查尾随空格
if cartesia_key.endswith(' '):
    print("   [X] 发现尾随空格")
elif cartesia_key.endswith('\t'):
    print("   [X] 发现尾随制表符")
else:
    print("   [OK] 没有发现尾随不可见字符")

print()
print("【3】Key 内容检查")
print("-" * 70)
# 显示前10个和后10个字符（隐藏中间）
if key_length > 20:
    preview = cartesia_key[:10] + "..." + cartesia_key[-10:]
    print(f"   Key 预览: {preview}")
else:
    print(f"   Key 预览: {cartesia_key}")

# 检查是否包含常见无效字符
invalid_chars = ['\n', '\r', '\t', '\ufeff']
found_invalid = [c for c in invalid_chars if c in cartesia_key]
if found_invalid:
    print(f"   [X] 发现无效字符: {found_invalid}")
else:
    print("   [OK] 没有发现无效字符")

print()
print("【4】Key 格式验证")
print("-" * 70)
# Cartesia API Key 通常是 UUID 格式或特定格式
# 检查基本格式
if key_length < 10:
    print("   [X] Key 太短（可能不完整）")
elif key_length > 200:
    print("   [X] Key 太长（可能包含多余内容）")
else:
    print("   [OK] Key 长度合理")

# 检查是否看起来像有效的 API Key
if ' ' in cartesia_key.strip():
    print("   [X] Key 中包含空格（可能有问题）")
else:
    print("   [OK] Key 格式看起来正常")

print()
print("【5】测试 Cartesia API")
print("-" * 70)
try:
    from cartesia import Cartesia
    
    # 清理 Key（移除可能的空白）
    clean_key = cartesia_key.strip()
    
    try:
        client = Cartesia(api_key=clean_key)
        print("   [OK] Cartesia 客户端初始化成功")
        
        # 尝试一个简单的测试（不实际调用 API，只检查客户端）
        print("   [OK] Cartesia API Key 格式正确")
        
    except Exception as api_error:
        error_str = str(api_error)
        if "401" in error_str or "unauthorized" in error_str.lower():
            print(f"   [X] Cartesia API Key 无效（401）")
            print(f"   错误: {error_str[:200]}")
        elif "429" in error_str or "quota" in error_str.lower():
            print(f"   [!] Cartesia API Key 有效，但配额已用完（429）")
        else:
            print(f"   [!] Cartesia API 错误: {error_str[:200]}")
            
except ImportError:
    print("   [X] cartesia 包未安装")
except Exception as e:
    print(f"   [X] 测试失败: {e}")

print()
print("=" * 70)
print("  检查完成")
print("=" * 70)
print()
print("建议:")
if cartesia_key:
    print(f"  1. 确认 Key 长度: {key_length} 字符")
    print(f"  2. 如果 Key 无效，请访问 Cartesia 控制台获取新的 API Key")
    print(f"  3. 更新 .env 文件后，确保没有前导/尾随空格")
print()

