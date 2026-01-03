"""对齐计划执行验证脚本"""
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("  菲菲对齐计划执行验证")
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

# ============================================
# 第一階段：核心靈魂移植
# ============================================
print("【第一階段】核心靈魂移植")
print("-" * 70)

# 1.1 Gemini 2.0 接入檢查
print("\n1.1 Gemini 2.0 接入檢查...")
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key and "AIzaSyBhl9" in gemini_key:
    preview = gemini_key[:20] + "..." + gemini_key[-10:]
    print(f"   [OK] GEMINI_API_KEY 已配置: {preview}")
else:
    print("   [X] GEMINI_API_KEY 未找到或格式不正确")
    sys.exit(1)

# 1.2 檢查 phi_brain.py 是否使用 Gemini
print("\n1.2 檢查 phi_brain.py 配置...")
try:
    with open(os.path.join(base_dir, "phi_brain.py"), 'r', encoding='utf-8') as f:
        brain_content = f.read()
    
    has_gemini_init = "api_type == \"gemini\"" in brain_content or "api_type=\"gemini\"" in brain_content
    has_safety_none = "BLOCK_NONE" in brain_content and "safety_settings" in brain_content
    
    if has_gemini_init:
        print("   [OK] phi_brain.py 已配置 Gemini 支持")
    else:
        print("   [X] phi_brain.py 未找到 Gemini 配置")
    
    if has_safety_none:
        print("   [OK] safety_settings 已配置为 BLOCK_NONE")
    else:
        print("   [X] safety_settings 未找到或未正确配置")
        
except Exception as e:
    print(f"   [X] 检查失败: {e}")

# 1.3 檢查 voice_bridge.py 是否使用 Gemini
print("\n1.3 檢查 voice_bridge.py 配置...")
try:
    with open(os.path.join(base_dir, "voice_bridge.py"), 'r', encoding='utf-8') as f:
        bridge_content = f.read()
    
    uses_gemini = "api_type=\"gemini\"" in bridge_content or "api_type='gemini'" in bridge_content
    
    if uses_gemini:
        print("   [OK] voice_bridge.py 已配置使用 Gemini")
    else:
        print("   [!] voice_bridge.py 可能仍使用旧配置，建议检查")
        
except Exception as e:
    print(f"   [X] 检查失败: {e}")

# ============================================
# 第二階段：感官邏輯同步
# ============================================
print("\n\n【第二階段】感官邏輯同步")
print("-" * 70)

# 2.1 物理常識固化檢查
print("\n2.1 檢查 _logic_refiner()...")
try:
    from phi_brain import PhiBrain, PersonalityMode, ArousalLevel
    
    brain = PhiBrain(api_type="gemini", personality=PersonalityMode.MIXED)
    
    # 測試邏輯修正
    test_cases = [
        ("主人，我想被幹小豆豆", "舔弄小豆豆"),
        ("插小豆豆", "撥弄小豆豆"),
        ("捅陰核", "舔弄陰核"),
    ]
    
    all_passed = True
    for test_input, expected_keyword in test_cases:
        refined = brain._logic_refiner(test_input)
        if expected_keyword in refined or "舔" in refined or "撥弄" in refined:
            print(f"   [OK] 測試通過: '{test_input}' -> 包含正確動詞")
        else:
            print(f"   [X] 測試失敗: '{test_input}' -> '{refined}'")
            all_passed = False
    
    if all_passed:
        print("   [OK] _logic_refiner() 正常工作")
    else:
        print("   [X] _logic_refiner() 需要檢查")
        
except Exception as e:
    print(f"   [X] 測試失敗: {e}")

# 2.2 情緒標籤注入檢查
print("\n2.2 檢查 _auto_map_emotion_tags()...")
try:
    brain.set_arousal_level(ArousalLevel.PEAK)
    test_text = "主人好興奮"
    tagged = brain._auto_map_emotion_tags(test_text)
    
    has_tags = any(tag in tagged for tag in ["[gasp]", "[moan]", "[squeal]", "[laughter]"])
    
    if has_tags:
        print(f"   [OK] _auto_map_emotion_tags() 正常工作")
        print(f"   示例: '{test_text}' -> '{tagged[:80]}...'")
    else:
        print(f"   [X] _auto_map_emotion_tags() 可能未生效")
        print(f"   結果: '{tagged}'")
        
except Exception as e:
    print(f"   [X] 測試失敗: {e}")

# ============================================
# 第三階段：聲帶穩定性強化
# ============================================
print("\n\n【第三階段】聲帶穩定性強化")
print("-" * 70)

# 3.1 子句緩衝檢查
print("\n3.1 檢查 _clause_buffer()...")
try:
    with open(os.path.join(base_dir, "voice_bridge.py"), 'r', encoding='utf-8') as f:
        bridge_content = f.read()
    
    has_clause_buffer = "_clause_buffer" in bridge_content
    has_cartesia_tags = "cartesia_tags_whitelist" in bridge_content or "cartesia_tag" in bridge_content
    
    if has_clause_buffer:
        print("   [OK] _clause_buffer() 函數存在")
    else:
        print("   [X] _clause_buffer() 函數未找到")
    
    if has_cartesia_tags:
        print("   [OK] Cartesia 標籤保護機制存在")
    else:
        print("   [!] Cartesia 標籤保護機制可能需要檢查")
        
except Exception as e:
    print(f"   [X] 檢查失敗: {e}")

# 3.2 流式傳輸檢查
print("\n3.2 檢查流式傳輸配置...")
try:
    has_streaming = "StreamingResponse" in bridge_content
    has_cartesia = "Cartesia" in bridge_content or "cartesia" in bridge_content
    
    if has_streaming:
        print("   [OK] StreamingResponse 已配置")
    else:
        print("   [X] StreamingResponse 未找到")
    
    if has_cartesia:
        print("   [OK] Cartesia API 集成存在")
    else:
        print("   [X] Cartesia API 集成未找到")
        
except Exception as e:
    print(f"   [X] 檢查失敗: {e}")

# ============================================
# 總結
# ============================================
print("\n\n" + "=" * 70)
print("  驗證完成")
print("=" * 70)
print()
print("下一步：")
print("  1. 確認所有 [OK] 項目")
print("  2. 修復所有 [X] 項目")
print("  3. 重啟 start_voice_bridge.ps1")
print()

