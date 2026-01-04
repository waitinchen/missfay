"""
本地 LLM 测试脚本
测试 GEMINI_API_KEY 是否有效，以及 PhiBrain 是否能正常工作
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_gemini_key():
    """测试 GEMINI_API_KEY 是否有效"""
    print("=" * 60)
    print("🔍 测试 GEMINI_API_KEY")
    print("=" * 60)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY 未设置")
        print("   请在 .env 文件中设置 GEMINI_API_KEY")
        return False
    
    print(f"✅ GEMINI_API_KEY 存在 (长度: {len(gemini_key)})")
    print(f"   前5个字符: {gemini_key[:5]}")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        
        # 尝试列出模型
        print("\n📋 正在验证 API Key...")
        models = genai.list_models()
        model_names = [m.name for m in models]
        
        print(f"✅ GEMINI_API_KEY 有效！")
        print(f"   可用模型数量: {len(model_names)}")
        
        # 检查默认模型
        default_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        target_model = f"models/{default_model}"
        
        if target_model in model_names or any(default_model in name for name in model_names):
            print(f"✅ 模型 '{default_model}' 可用")
        else:
            print(f"⚠️  模型 '{default_model}' 可能不可用")
            print(f"   可用模型示例: {model_names[:3] if model_names else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ GEMINI_API_KEY 验证失败: {str(e)}")
        return False

def test_phi_brain():
    """测试 PhiBrain 初始化"""
    print("\n" + "=" * 60)
    print("🧠 测试 PhiBrain 初始化")
    print("=" * 60)
    
    try:
        from phi_brain import PhiBrain, PersonalityMode
        
        print("正在初始化 PhiBrain...")
        brain = PhiBrain(
            api_type="gemini",
            personality=PersonalityMode.MIXED
        )
        print("✅ PhiBrain 初始化成功")
        
        # 测试生成回复
        print("\n💬 测试生成回复...")
        test_message = "你好"
        print(f"   输入: {test_message}")
        
        response, metadata = brain.generate_response(test_message)
        print(f"✅ 回复生成成功")
        print(f"   输出: {response[:100]}..." if len(response) > 100 else f"   输出: {response}")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"❌ PhiBrain 测试失败: {str(e)}")
        print(f"\n详细错误:")
        traceback.print_exc()
        return False

def test_api_endpoint():
    """测试 API 端点是否可访问"""
    print("\n" + "=" * 60)
    print("🌐 测试 API 端点")
    print("=" * 60)
    
    import requests
    
    base_url = "http://localhost:8000"
    
    # 测试健康检查
    try:
        print(f"测试 {base_url}/health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过")
            print(f"   LLM 状态: {data.get('brain_status', 'unknown')}")
            print(f"   TTS 状态: {data.get('cartesia_status', 'unknown')}")
        else:
            print(f"⚠️  健康检查返回: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到 {base_url}")
        print(f"   请确保服务已启动: python voice_bridge.py 或 uvicorn voice_bridge:app")
        return False
    except Exception as e:
        print(f"❌ 健康检查失败: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("\n🚀 开始本地 LLM 测试\n")
    
    # 测试 1: GEMINI_API_KEY
    gemini_ok = test_gemini_key()
    
    # 测试 2: PhiBrain
    if gemini_ok:
        brain_ok = test_phi_brain()
    else:
        print("\n⚠️  跳过 PhiBrain 测试（GEMINI_API_KEY 无效）")
        brain_ok = False
    
    # 测试 3: API 端点
    api_ok = test_api_endpoint()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"GEMINI_API_KEY: {'✅ 有效' if gemini_ok else '❌ 无效'}")
    print(f"PhiBrain: {'✅ 正常' if brain_ok else '❌ 异常'}")
    print(f"API 端点: {'✅ 可访问' if api_ok else '❌ 不可访问'}")
    print()
    
    if gemini_ok and brain_ok and api_ok:
        print("🎉 所有测试通过！LLM 服务正常")
    else:
        print("⚠️  部分测试失败，请检查上述错误信息")

