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
    phase1_1 = True
else:
    print("   [X] GEMINI_API_KEY 未找到或格式不正确")
    phase1_1 = False

# 1.2 檢查 phi_brain.py 是否使用 Gemini
print("\n1.2 檢查 phi_brain.py 配置...")
try:
    with open(os.path.join(base_dir, "phi_brain.py"), 'r', encoding='utf-8') as f:
        brain_content = f.read()
    
    has_gemini_init = "api_type == \"gemini\"" in brain_content
    has_safety_none = "BLOCK_NONE" in brain_content and "safety_settings" in brain_content
    has_all_categories = all(cat in brain_content for cat in [
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_HARASSMENT", 
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_DANGEROUS_CONTENT"
    ])
    
    if has_gemini_init:
        print("   [OK] phi_brain.py 已配置 Gemini 支持")
    else:
        print("   [X] phi_brain.py 未找到 Gemini 配置")
    
    if has_safety_none and has_all_categories:
        print("   [OK] safety_settings 已全數配置为 BLOCK_NONE (4个类别)")
        phase1_2 = True
    else:
        print("   [X] safety_settings 未完整配置")
        phase1_2 = False
        
except Exception as e:
    print(f"   [X] 检查失败: {e}")
    phase1_2 = False

# 1.3 檢查 voice_bridge.py 是否使用 Gemini
print("\n1.3 檢查 voice_bridge.py 配置...")
try:
    with open(os.path.join(base_dir, "voice_bridge.py"), 'r', encoding='utf-8') as f:
        bridge_content = f.read()
    
    uses_gemini = "api_type=\"gemini\"" in bridge_content or "api_type='gemini'" in bridge_content
    
    if uses_gemini:
        print("   [OK] voice_bridge.py 已配置使用 Gemini")
        phase1_3 = True
    else:
        print("   [!] voice_bridge.py 可能仍使用旧配置")
        phase1_3 = False
        
except Exception as e:
    print(f"   [X] 检查失败: {e}")
    phase1_3 = False

# ============================================
# 第二階段：感官邏輯同步
# ============================================
print("\n\n【第二階段】感官邏輯同步")
print("-" * 70)

# 2.1 物理常識固化檢查
print("\n2.1 檢查 _logic_refiner()...")
phase2_1 = False
try:
    from phi_brain import PhiBrain, PersonalityMode, ArousalLevel
    
    brain = PhiBrain(api_type="gemini", personality=PersonalityMode.MIXED)
    
    # 測試邏輯修正
    test_cases = [
        ("主人，我想被幹小豆豆", ["舔弄", "舔"]),
        ("插小豆豆", ["撥弄"]),
        ("捅陰核", ["舔弄", "舔"]),
    ]
    
    all_passed = True
    for test_input, expected_keywords in test_cases:
        refined = brain._logic_refiner(test_input)
        if any(kw in refined for kw in expected_keywords):
            print(f"   [OK] 測試通過: '{test_input}' -> 包含正確動詞")
        else:
            print(f"   [X] 測試失敗: '{test_input}' -> '{refined}'")
            all_passed = False
    
    if all_passed:
        print("   [OK] _logic_refiner() 正常工作，物理常識已固化")
        phase2_1 = True
    else:
        print("   [X] _logic_refiner() 需要檢查")
        
except Exception as e:
    print(f"   [X] 測試失敗: {e}")
    import traceback
    traceback.print_exc()

# 2.2 情緒標籤注入檢查
print("\n2.2 檢查 _auto_map_emotion_tags()...")
phase2_2 = False
try:
    brain.set_arousal_level(ArousalLevel.PEAK)
    test_text = "主人好興奮"
    tagged = brain._auto_map_emotion_tags(test_text)
    
    has_tags = any(tag in tagged for tag in ["[gasp]", "[moan]", "[squeal]", "[laughter]", "[giggle]"])
    
    if has_tags:
        print(f"   [OK] _auto_map_emotion_tags() 正常工作")
        print(f"   示例: '{test_text}' -> '{tagged[:80]}...'")
        phase2_2 = True
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
phase3_1 = False
try:
    with open(os.path.join(base_dir, "voice_bridge.py"), 'r', encoding='utf-8') as f:
        bridge_content = f.read()
    
    has_clause_buffer = "_clause_buffer" in bridge_content
    has_cartesia_tags = "cartesia_tags_whitelist" in bridge_content
    has_tag_protection = "__CARTESIA_TAG_" in bridge_content or "tag_map" in bridge_content
    
    if has_clause_buffer:
        print("   [OK] _clause_buffer() 函數存在")
    else:
        print("   [X] _clause_buffer() 函數未找到")
    
    if has_cartesia_tags and has_tag_protection:
        print("   [OK] Cartesia 標籤保護機制完整")
        phase3_1 = True
    else:
        print("   [X] Cartesia 標籤保護機制不完整")
        
except Exception as e:
    print(f"   [X] 檢查失敗: {e}")

# 3.2 流式傳輸檢查
print("\n3.2 檢查流式傳輸配置...")
phase3_2 = False
try:
    has_streaming = "StreamingResponse" in bridge_content
    has_cartesia = "Cartesia" in bridge_content or "cartesia" in bridge_content
    has_bytes = "tts.bytes" in bridge_content
    
    if has_streaming:
        print("   [OK] StreamingResponse 已配置")
    else:
        print("   [X] StreamingResponse 未找到")
    
    if has_cartesia and has_bytes:
        print("   [OK] Cartesia API 流式傳輸已配置")
        phase3_2 = True
    else:
        print("   [X] Cartesia API 流式傳輸配置不完整")
        
except Exception as e:
    print(f"   [X] 檢查失敗: {e}")

# ============================================
# 總結
# ============================================
print("\n\n" + "=" * 70)
print("  驗證總結")
print("=" * 70)

results = {
    "第一階段": {
        "Gemini 接入": phase1_1,
        "安全設置": phase1_2,
        "Voice Bridge 配置": phase1_3
    },
    "第二階段": {
        "物理常識固化": phase2_1,
        "情緒標籤注入": phase2_2
    },
    "第三階段": {
        "子句緩衝": phase3_1,
        "流式傳輸": phase3_2
    }
}

all_passed = True
for phase, checks in results.items():
    print(f"\n{phase}:")
    for check_name, status in checks.items():
        status_str = "[OK]" if status else "[X]"
        print(f"  {status_str} {check_name}")
        if not status:
            all_passed = False

print("\n" + "=" * 70)
if all_passed:
    print("  ✅ 所有檢查通過！系統已準備就緒")
else:
    print("  ⚠️  部分檢查未通過，請修復後重試")
print("=" * 70)
print()
print("下一步：")
print("  1. 確認所有 [OK] 項目")
if not all_passed:
    print("  2. 修復所有 [X] 項目")
print("  3. 重啟 start_voice_bridge.ps1")
print()


