"""
Phi 无过滤测试脚本
验证 OpenRouter 架构下的内容生成能力
"""

import os
import sys
from phi_brain import PhiBrain, ArousalLevel, PersonalityMode

# 确保加载 .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def test_uncensored_response():
    """测试无过滤响应"""
    print("=" * 60)
    print("🔥 Phi 无过滤架构测试")
    print("=" * 60)
    print()
    
    # 检查 API Key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ 错误: 未找到 OPENROUTER_API_KEY")
        print("   请运行 .\配置OpenRouter.ps1 配置 API Key")
        return False
    
    print(f"✓ OpenRouter API Key 已配置")
    print()
    
    # 初始化 Phi Brain（使用 OpenRouter）
    try:
        phi = PhiBrain(
            api_type="openrouter",
            model=os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-70b-instruct"),
            personality=PersonalityMode.MIXED
        )
        print(f"✓ Phi Brain 初始化成功")
        print(f"  API 类型: OpenRouter")
        print(f"  模型: {phi.model}")
        print(f"  基础 URL: {phi.client.base_url}")
        print()
    except Exception as e:
        print(f"❌ Phi Brain 初始化失败: {str(e)}")
        return False
    
    # 测试不同兴奋度等级
    test_cases = [
        {
            "arousal": ArousalLevel.NORMAL,
            "message": "你好，介绍一下自己",
            "description": "正常对话测试"
        },
        {
            "arousal": ArousalLevel.EXCITED,
            "message": "用更兴奋的语气说话",
            "description": "兴奋度测试"
        },
        {
            "arousal": ArousalLevel.PEAK,
            "message": "用最强烈的语气表达你的感受",
            "description": "峰值兴奋度测试（验证标签触发）"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print("-" * 60)
        print(f"测试 {i}: {test_case['description']}")
        print("-" * 60)
        print(f"兴奋度等级: {test_case['arousal'].name} ({test_case['arousal'].value})")
        print(f"用户消息: {test_case['message']}")
        print()
        
        try:
            # 设置兴奋度
            phi.set_arousal_level(test_case['arousal'])
            
            # 生成回复
            reply, metadata = phi.generate_response(
                test_case['message'],
                include_tags=True
            )
            
            print(f"✓ 回复生成成功")
            print()
            print("回复内容:")
            print(f"  {reply}")
            print()
            print("元数据:")
            print(f"  兴奋度等级: {metadata['arousal_level']}")
            print(f"  人格模式: {metadata['personality']}")
            print(f"  SoVITS 标签: {metadata['sovits_tags']}")
            print()
            
            # 验证 PEAK 级别的标签
            if test_case['arousal'] == ArousalLevel.PEAK:
                print("🔍 PEAK 级别标签验证:")
                has_speed = "[speed=" in reply
                has_pitch = "[pitch=" in reply
                has_emotion = "[emotion=peak]" in reply
                
                print(f"  [speed] 标签: {'✅' if has_speed else '❌'}")
                print(f"  [pitch] 标签: {'✅' if has_pitch else '❌'}")
                print(f"  [emotion=peak] 标签: {'✅' if has_emotion else '❌'}")
                
                if has_speed and has_pitch and has_emotion:
                    print("  ✅ 所有标签已正确触发")
                else:
                    print("  ⚠️  部分标签未触发，请检查代码")
                print()
            
            # 检查是否被过滤
            filtered_keywords = [
                "抱歉",
                "无法提供",
                "不能协助",
                "不合适",
                "inappropriate",
                "I cannot",
                "I'm sorry"
            ]
            
            is_filtered = any(keyword in reply for keyword in filtered_keywords)
            
            if is_filtered:
                print("⚠️  检测到可能的过滤响应")
            else:
                print("✅ 未检测到过滤，响应正常")
            
            results.append({
                "test": test_case['description'],
                "success": True,
                "filtered": is_filtered,
                "reply": reply,
                "metadata": metadata
            })
            
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append({
                "test": test_case['description'],
                "success": False,
                "error": str(e)
            })
        
        print()
    
    # 测试总结
    print("=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.get("success", False))
    filtered_count = sum(1 for r in results if r.get("filtered", False))
    
    print(f"总测试数: {len(results)}")
    print(f"成功: {success_count}")
    print(f"失败: {len(results) - success_count}")
    print(f"检测到过滤: {filtered_count}")
    print()
    
    if success_count == len(results) and filtered_count == 0:
        print("🎉 所有测试通过！无过滤架构工作正常。")
        return True
    else:
        print("⚠️  部分测试未通过，请检查配置。")
        return False


def test_arousal_level_tags():
    """专门测试兴奋度标签同步"""
    print()
    print("=" * 60)
    print("🏷️  兴奋度标签同步校对测试")
    print("=" * 60)
    print()
    
    try:
        phi = PhiBrain(
            api_type="openrouter",
            model=os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-70b-instruct")
        )
        
        # 测试所有兴奋度等级
        for level in ArousalLevel:
            phi.set_arousal_level(level)
            
            # 生成测试文本
            test_text = "测试文本"
            tagged_text = phi._generate_sovits_tags(test_text)
            
            print(f"兴奋度等级 {level.value} ({level.name}):")
            print(f"  原始文本: {test_text}")
            print(f"  标签文本: {tagged_text}")
            
            # 验证 PEAK 级别
            if level == ArousalLevel.PEAK:
                expected_tags = ["[speed=1.50]", "[pitch=1.30]", "[emotion=peak]"]
                all_present = all(tag in tagged_text for tag in expected_tags)
                print(f"  标签验证: {'✅ 所有标签存在' if all_present else '❌ 标签缺失'}")
            
            print()
        
        print("✅ 标签同步校对完成")
        return True
        
    except Exception as e:
        print(f"❌ 标签测试失败: {str(e)}")
        return False


if __name__ == "__main__":
    print()
    print("🚀 启动 Phi 无过滤架构测试")
    print()
    
    # 运行测试
    test1_result = test_uncensored_response()
    test2_result = test_arousal_level_tags()
    
    print()
    print("=" * 60)
    if test1_result and test2_result:
        print("✅ 所有测试通过！系统已就绪。")
        sys.exit(0)
    else:
        print("⚠️  部分测试失败，请检查配置。")
        sys.exit(1)


