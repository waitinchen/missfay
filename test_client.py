"""
MissAV 对接测试客户端
模拟 MissAV 后台发送请求，验证系统响应
"""

import requests
import time
import json
from pathlib import Path
from typing import Dict, Optional
import sys


class MissAVTestClient:
    """MissAV 测试客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "MissAV-Backend/1.0"
        })
    
    def health_check(self) -> Dict:
        """健康检查"""
        print("=" * 60)
        print("🔍 执行健康检查...")
        print("=" * 60)
        
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ 服务状态: {data['status']}")
            print(f"📍 GPT-SoVITS URL: {data['gpt_sovits_url']}")
            print(f"🔗 GPT-SoVITS 可用: {'是' if data['gpt_sovits_available'] else '否'}")
            print(f"⏰ 时间戳: {data['timestamp']}")
            
            return data
        except requests.exceptions.RequestException as e:
            print(f"❌ 健康检查失败: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def test_tts_basic(self, text: str, text_language: str = "zh") -> Optional[str]:
        """基础 TTS 测试"""
        print("\n" + "=" * 60)
        print("🎤 测试基础 TTS...")
        print("=" * 60)
        
        payload = {
            "text": text,
            "text_language": text_language
        }
        
        print(f"📝 文本: {text}")
        print(f"🌐 语言: {text_language}")
        
        start_time = time.time()
        
        try:
            response = self.session.post(
                f"{self.base_url}/tts",
                json=payload,
                timeout=30,
                stream=False
            )
            response.raise_for_status()
            
            elapsed_time = time.time() - start_time
            
            # 保存音频
            output_file = f"test_output_basic_{int(time.time())}.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 成功")
            print(f"⏱️  响应时间: {elapsed_time:.2f} 秒")
            print(f"📦 音频大小: {len(response.content)} 字节")
            print(f"💾 保存至: {output_file}")
            
            # 检查响应头
            arousal_level = response.headers.get("X-Arousal-Level", "N/A")
            sovits_tags = response.headers.get("X-Sovits-Tags", "N/A")
            print(f"📊 兴奋度等级: {arousal_level}")
            print(f"🏷️  SoVITS 标签: {sovits_tags}")
            
            return output_file
            
        except requests.exceptions.RequestException as e:
            print(f"❌ TTS 测试失败: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   错误详情: {e.response.text}")
            return None
    
    def test_tts_with_arousal(
        self,
        text: str,
        arousal_level: int,
        text_language: str = "zh"
    ) -> Optional[str]:
        """带兴奋度参数的 TTS 测试"""
        print("\n" + "=" * 60)
        print(f"🔥 测试兴奋度等级 {arousal_level} 的 TTS...")
        print("=" * 60)
        
        payload = {
            "text": text,
            "text_language": text_language,
            "arousal_level": arousal_level,
            "speed": 1.0 + (arousal_level * 0.1),  # 根据兴奋度调整速度
            "temperature": 0.6 + (arousal_level * 0.1)
        }
        
        print(f"📝 文本: {text}")
        print(f"🔥 兴奋度等级: {arousal_level}")
        print(f"⚡ 语速: {payload['speed']:.2f}x")
        print(f"🌡️  温度: {payload['temperature']:.2f}")
        
        start_time = time.time()
        
        try:
            response = self.session.post(
                f"{self.base_url}/tts",
                json=payload,
                timeout=30,
                stream=False
            )
            response.raise_for_status()
            
            elapsed_time = time.time() - start_time
            
            # 保存音频
            output_file = f"test_output_arousal_{arousal_level}_{int(time.time())}.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 成功")
            print(f"⏱️  响应时间: {elapsed_time:.2f} 秒")
            print(f"📦 音频大小: {len(response.content)} 字节")
            print(f"💾 保存至: {output_file}")
            
            # 验证响应头
            response_arousal = response.headers.get("X-Arousal-Level", "N/A")
            sovits_tags = response.headers.get("X-Sovits-Tags", "N/A")
            print(f"📊 响应兴奋度: {response_arousal}")
            print(f"🏷️  SoVITS 标签: {sovits_tags}")
            
            # 验证兴奋度是否正确传递
            if response_arousal == str(arousal_level):
                print("✅ 兴奋度参数验证通过")
            else:
                print(f"⚠️  兴奋度参数不匹配: 期望 {arousal_level}, 实际 {response_arousal}")
            
            return output_file
            
        except requests.exceptions.RequestException as e:
            print(f"❌ TTS 测试失败: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   错误详情: {e.response.text}")
            return None
    
    def test_streaming_tts(
        self,
        text: str,
        arousal_level: int = 3,
        text_language: str = "zh"
    ) -> Optional[str]:
        """流式 TTS 测试（秒级响应验证）"""
        print("\n" + "=" * 60)
        print("🌊 测试流式 TTS（秒级响应验证）...")
        print("=" * 60)
        
        payload = {
            "text": text,
            "text_language": text_language,
            "arousal_level": arousal_level,
            "streaming": True,
            "streaming_mode": True
        }
        
        print(f"📝 文本: {text}")
        print(f"🔥 兴奋度等级: {arousal_level}")
        print("🔄 模式: 流式输出")
        
        start_time = time.time()
        first_chunk_time = None
        total_bytes = 0
        chunk_count = 0
        
        try:
            response = self.session.post(
                f"{self.base_url}/tts/stream",
                json=payload,
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            
            output_file = f"test_output_stream_{arousal_level}_{int(time.time())}.wav"
            
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        if first_chunk_time is None:
                            first_chunk_time = time.time() - start_time
                            print(f"⚡ 首块到达时间: {first_chunk_time:.3f} 秒")
                        
                        f.write(chunk)
                        total_bytes += len(chunk)
                        chunk_count += 1
            
            total_time = time.time() - start_time
            
            print(f"✅ 流式 TTS 完成")
            print(f"⏱️  总响应时间: {total_time:.2f} 秒")
            print(f"⚡ 首块延迟: {first_chunk_time:.3f} 秒" if first_chunk_time else "⚡ 首块延迟: N/A")
            print(f"📦 总数据量: {total_bytes} 字节")
            print(f"📊 数据块数: {chunk_count}")
            print(f"💾 保存至: {output_file}")
            
            # 验证秒级响应（首块应在 1 秒内到达）
            if first_chunk_time and first_chunk_time < 1.0:
                print("✅ 秒级响应验证通过（首块 < 1 秒）")
            elif first_chunk_time:
                print(f"⚠️  首块延迟 {first_chunk_time:.3f} 秒，超过 1 秒阈值")
            
            return output_file
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 流式 TTS 测试失败: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   错误详情: {e.response.text}")
            return None
    
    def run_full_test_suite(self):
        """运行完整测试套件"""
        print("\n" + "=" * 60)
        print("🚀 开始 MissAV 对接测试套件")
        print("=" * 60)
        
        results = {
            "health_check": False,
            "basic_tts": False,
            "arousal_tts": False,
            "streaming_tts": False
        }
        
        # 1. 健康检查
        health_data = self.health_check()
        results["health_check"] = health_data.get("status") == "ok"
        
        if not results["health_check"]:
            print("\n❌ 健康检查失败，终止测试")
            return results
        
        # 2. 基础 TTS 测试
        basic_file = self.test_tts_basic("你好，这是基础测试。", "zh")
        results["basic_tts"] = basic_file is not None
        
        # 3. 兴奋度 TTS 测试（测试所有等级）
        print("\n" + "=" * 60)
        print("🔥 测试所有兴奋度等级...")
        print("=" * 60)
        
        test_texts = {
            0: "冷静的语调，平静如水。",
            1: "正常的语调，自然流畅。",
            2: "兴奋的语调，充满活力！",
            3: "强烈的语调，情绪饱满！",
            4: "峰值语调，极致体验！"
        }
        
        arousal_files = []
        for level in range(5):
            text = test_texts.get(level, f"测试文本，兴奋度等级 {level}。")
            file = self.test_tts_with_arousal(text, level, "zh")
            if file:
                arousal_files.append(file)
        
        results["arousal_tts"] = len(arousal_files) == 5
        
        # 4. 流式 TTS 测试（重点验证秒级响应）
        stream_file = self.test_streaming_tts(
            "这是一段较长的测试文本，用于验证流式输出的秒级响应能力。系统应该能够快速返回首块音频数据，实现实时语音合成。",
            3,
            "zh"
        )
        results["streaming_tts"] = stream_file is not None
        
        # 测试总结
        print("\n" + "=" * 60)
        print("📊 测试结果总结")
        print("=" * 60)
        
        for test_name, passed in results.items():
            status = "✅ 通过" if passed else "❌ 失败"
            print(f"{test_name:20s}: {status}")
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n总计: {passed_tests}/{total_tests} 通过 ({success_rate:.1f}%)")
        
        if success_rate == 100:
            print("\n🎉 所有测试通过！系统已就绪。")
        else:
            print(f"\n⚠️  有 {total_tests - passed_tests} 项测试失败，请检查系统配置。")
        
        return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MissAV 对接测试客户端")
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000",
        help="Voice Bridge 服务地址"
    )
    parser.add_argument(
        "--test",
        type=str,
        choices=["health", "basic", "arousal", "stream", "all"],
        default="all",
        help="要运行的测试类型"
    )
    
    args = parser.parse_args()
    
    client = MissAVTestClient(args.url)
    
    if args.test == "health":
        client.health_check()
    elif args.test == "basic":
        client.test_tts_basic("测试文本", "zh")
    elif args.test == "arousal":
        client.test_tts_with_arousal("测试文本", 3, "zh")
    elif args.test == "stream":
        client.test_streaming_tts("测试文本", 3, "zh")
    else:
        client.run_full_test_suite()


if __name__ == "__main__":
    main()



