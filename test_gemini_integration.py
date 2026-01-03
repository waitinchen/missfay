"""测试 Gemini 2.0 Flash 集成"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 加载环境变量
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")

if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()

sys.path.insert(0, base_dir)

print("=" * 60)
print("  测试 Gemini 2.0 Flash 集成")
print("=" * 60)
print()

# 测试 1: 检查 API Key
print("1. 检查 GEMINI_API_KEY...")
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    preview = api_key[:20] + "..." + api_key[-10:] if len(api_key) > 30 else api_key
    print(f"   [OK] GEMINI_API_KEY 已加载: {preview}")
else:
    print("   [X] GEMINI_API_KEY 未找到")
    sys.exit(1)

print()

# 测试 2: 检查 SDK
print("2. 检查 google-generativeai SDK...")
try:
    import google.generativeai as genai
    print("   [OK] google-generativeai 已安装")
except ImportError:
    print("   [X] google-generativeai 未安装")
    print("   请运行: pip install google-generativeai")
    sys.exit(1)

print()

# 测试 3: 初始化 PhiBrain
print("3. 初始化 PhiBrain (Gemini)...")
try:
    from phi_brain import PhiBrain, PersonalityMode, ArousalLevel
    
    brain = PhiBrain(
        api_type="gemini",
        personality=PersonalityMode.MIXED
    )
    print(f"   [OK] PhiBrain 初始化成功")
    print(f"   模型: {brain.model}")
    print(f"   安全设置: BLOCK_NONE")
except Exception as e:
    print(f"   [X] PhiBrain 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# 测试 4: 测试生成
print("4. 测试文本生成...")
try:
    reply, metadata = brain.generate_response("主人，菲菲测试一下新的 Gemini 大脑~")
    print(f"   [OK] 生成成功")
    print(f"   回复: {reply[:100]}...")
    print(f"   兴奋度: {metadata.get('arousal_level', 'N/A')}")
except Exception as e:
    print(f"   [X] 生成失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# 测试 5: 测试逻辑链
print("5. 测试逻辑链继承...")
try:
    # 测试 logic_refiner
    test_text = "主人，我想被幹小豆豆"
    refined = brain._logic_refiner(test_text)
    if "舔弄" in refined or "撥弄" in refined:
        print("   [OK] _logic_refiner 正常工作")
    else:
        print("   [!] _logic_refiner 可能未生效")
    
    # 测试 auto_map_emotion_tags
    brain.set_arousal_level(ArousalLevel.PEAK)
    tagged = brain._auto_map_emotion_tags("主人好兴奋")
    if "[gasp]" in tagged or "[moan]" in tagged or "[laughter]" in tagged:
        print("   [OK] _auto_map_emotion_tags 正常工作")
    else:
        print("   [!] _auto_map_emotion_tags 可能未生效")
except Exception as e:
    print(f"   [X] 逻辑链测试失败: {e}")

print()
print("=" * 60)
print("  测试完成")
print("=" * 60)

