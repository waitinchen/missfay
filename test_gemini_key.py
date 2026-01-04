"""
测试 GEMINI_API_KEY 是否有效
"""

import os
import sys

# 设置 UTF-8 编码（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 设置要测试的 API Key
TEST_KEY = "AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo"

print("=" * 60)
print("测试 GEMINI_API_KEY")
print("=" * 60)
print()
print(f"测试 Key: {TEST_KEY[:10]}...{TEST_KEY[-5:]}")
print(f"Key 长度: {len(TEST_KEY)}")
print()

try:
    import google.generativeai as genai
    
    print("[OK] google-generativeai 包已安装")
    print()
    
    # 配置 API Key
    print("正在配置 API Key...")
    genai.configure(api_key=TEST_KEY)
    print("[OK] API Key 配置成功")
    print()
    
    # 尝试列出模型（轻量级验证）
    print("正在验证 API Key（列出可用模型）...")
    models = genai.list_models()
    model_names = [m.name for m in models]
    
    print(f"[OK] API Key 有效！")
    print(f"   可用模型数量: {len(model_names)}")
    print()
    
    # 显示前几个模型
    print("可用模型示例:")
    for i, model in enumerate(model_names[:5], 1):
        print(f"   {i}. {model}")
    if len(model_names) > 5:
        print(f"   ... 还有 {len(model_names) - 5} 个模型")
    print()
    
    # 检查默认模型
    default_model = "gemini-2.0-flash-exp"
    target_model = f"models/{default_model}"
    
    if target_model in model_names or any(default_model in name for name in model_names):
        print(f"[OK] 模型 '{default_model}' 可用")
    else:
        print(f"[WARN] 模型 '{default_model}' 可能不可用")
        print(f"   可用模型示例: {model_names[:3] if model_names else 'None'}")
    print()
    
    # 尝试生成一个简单的回复（完整验证）
    print("测试生成回复...")
    try:
        model = genai.GenerativeModel(default_model)
        response = model.generate_content("你好")
        print(f"[OK] 生成回复成功！")
        print(f"   回复: {response.text[:100]}..." if len(response.text) > 100 else f"   回复: {response.text}")
        print()
        print("[SUCCESS] API Key 完全有效，可以正常使用！")
    except Exception as e:
        print(f"[WARN] 生成回复时出错: {str(e)}")
        print("   但 API Key 本身是有效的（可以列出模型）")
    
except ImportError:
    print("[ERROR] google-generativeai 包未安装")
    print("   请运行: pip install google-generativeai")
    sys.exit(1)
    
except Exception as e:
    error_str = str(e)
    print(f"[ERROR] API Key 验证失败")
    print(f"   错误: {error_str}")
    print()
    
    # 分析错误类型
    if "API_KEY_INVALID" in error_str or "invalid" in error_str.lower():
        print("   原因: API Key 无效或格式错误")
    elif "PERMISSION_DENIED" in error_str or "permission" in error_str.lower():
        print("   原因: API Key 权限不足")
    elif "QUOTA_EXCEEDED" in error_str or "quota" in error_str.lower():
        print("   原因: API 配额已用完")
    elif "429" in error_str:
        print("   原因: 请求频率过高（429）")
    else:
        print("   原因: 未知错误，请检查网络连接和 API Key 格式")
    
    sys.exit(1)

print()
print("=" * 60)

