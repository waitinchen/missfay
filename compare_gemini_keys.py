"""
比较本地和生产环境的 GEMINI_API_KEY
"""

import os
import sys
import httpx

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dotenv import load_dotenv
load_dotenv()

# 本地 Key
local_key = os.getenv("GEMINI_API_KEY", "")

# 生产环境 Key（从图片中看到的）
production_key_from_image = "AIzaSyBh19-bR6xKe4DW2525LXU6dxYJSxUuOo"

# 之前测试的 Key
tested_key = "AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo"

print("=" * 60)
print("比较 GEMINI_API_KEY")
print("=" * 60)
print()

print("1. 本地环境变量中的 Key:")
if local_key:
    print(f"   Key: {local_key}")
    print(f"   长度: {len(local_key)}")
    print(f"   前10字符: {local_key[:10]}")
    print(f"   后5字符: {local_key[-5:]}")
else:
    print("   [未设置]")
print()

print("2. 生产环境 Key (从图片中):")
print(f"   Key: {production_key_from_image}")
print(f"   长度: {len(production_key_from_image)}")
print(f"   前10字符: {production_key_from_image[:10]}")
print(f"   后5字符: {production_key_from_image[-5:]}")
print()

print("3. 之前测试的 Key:")
print(f"   Key: {tested_key}")
print(f"   长度: {len(tested_key)}")
print(f"   前10字符: {tested_key[:10]}")
print(f"   后5字符: {tested_key[-5:]}")
print()

print("=" * 60)
print("比较结果:")
print("=" * 60)
print()

# 比较本地和生产环境
if local_key and production_key_from_image:
    if local_key == production_key_from_image:
        print("✅ 本地 Key 与生产环境 Key 相同")
    else:
        print("❌ 本地 Key 与生产环境 Key 不同")
        print()
        print("差异分析:")
        if len(local_key) != len(production_key_from_image):
            print(f"   - 长度不同: 本地={len(local_key)}, 生产={len(production_key_from_image)}")
        
        # 找出不同的字符位置
        min_len = min(len(local_key), len(production_key_from_image))
        diff_positions = []
        for i in range(min_len):
            if local_key[i] != production_key_from_image[i]:
                diff_positions.append((i, local_key[i], production_key_from_image[i]))
        
        if diff_positions:
            print(f"   - 发现 {len(diff_positions)} 个字符差异:")
            for pos, local_char, prod_char in diff_positions[:10]:  # 只显示前10个
                print(f"     位置 {pos}: 本地='{local_char}', 生产='{prod_char}'")
            if len(diff_positions) > 10:
                print(f"     ... 还有 {len(diff_positions) - 10} 个差异")
else:
    if not local_key:
        print("⚠️  本地 Key 未设置")
    if not production_key_from_image:
        print("⚠️  无法获取生产环境 Key")

print()

# 比较本地和测试的 Key
if local_key and tested_key:
    if local_key == tested_key:
        print("✅ 本地 Key 与测试 Key 相同")
    else:
        print("❌ 本地 Key 与测试 Key 不同")

print()

# 尝试从生产环境获取实际使用的 Key
print("4. 尝试从生产环境获取 Key 信息...")
try:
    response = httpx.get("https://missfay.tonetown.ai/verify-keys", timeout=10.0)
    if response.status_code == 200:
        data = response.json()
        prod_key_info = data.get("keys", {}).get("GEMINI_API_KEY", {})
        
        if prod_key_info.get("exists"):
            prod_key_length = prod_key_info.get("length", 0)
            print(f"   [OK] 生产环境 Key 存在")
            print(f"   - 长度: {prod_key_length}")
            
            if local_key:
                if len(local_key) == prod_key_length:
                    print("   ✅ 长度匹配（可能是同一个 Key）")
                else:
                    print(f"   ❌ 长度不匹配: 本地={len(local_key)}, 生产={prod_key_length}")
        else:
            print("   [ERROR] 生产环境 Key 不存在")
    else:
        print(f"   [ERROR] 无法连接到生产环境: {response.status_code}")
except Exception as e:
    print(f"   [ERROR] 连接失败: {str(e)}")

print()
print("=" * 60)
print("建议:")
print("=" * 60)
print()

if local_key and production_key_from_image and local_key != production_key_from_image:
    print("⚠️  Key 不一致，建议:")
    print("1. 确认生产环境应该使用哪个 Key")
    print("2. 如果生产环境 Key 正确，更新本地 .env 文件")
    print("3. 如果本地 Key 正确，更新 Railway 环境变量")
    print()
    print("正确的 Key 应该是: AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo")
    print("(之前测试验证有效的 Key)")
elif local_key == production_key_from_image:
    print("✅ Key 一致，无需更改")
else:
    print("请检查本地和生产环境的 Key 设置")

print()

