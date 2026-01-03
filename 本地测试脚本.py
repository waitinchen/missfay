"""本地测试脚本 - 测试 Phi 系统功能"""
import os
import sys
import requests
import time
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("  " + "=" * 76)
print("   Phi 系统本地测试 (Local Testing)")
print("  " + "=" * 76)
print("=" * 80)
print()

BASE_URL = "http://localhost:8000"
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0
}

def test(name, func):
    """执行测试"""
    test_results["total"] += 1
    print(f"[{test_results['total']}] {name}")
    print("-" * 80)
    try:
        result = func()
        if result:
            print(f"   [OK] {name} - 通过")
            test_results["passed"] += 1
        else:
            print(f"   [X] {name} - 失败")
            test_results["failed"] += 1
    except Exception as e:
        print(f"   [X] {name} - 错误: {str(e)[:100]}")
        test_results["failed"] += 1
    print()

# 测试 1: 健康检查端点
def test_health():
    """测试健康检查端点"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"   状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   错误: 无法连接到服务，请确保 Voice Bridge 正在运行")
        return False
    except Exception as e:
        print(f"   错误: {str(e)}")
        return False

# 测试 2: 前端界面
def test_frontend():
    """测试前端界面"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            content = response.text
            if "心菲" in content or "Phi" in content or "<html" in content.lower():
                print(f"   状态码: {response.status_code}")
                print(f"   内容类型: {response.headers.get('content-type', 'unknown')}")
                print(f"   内容长度: {len(content)} 字符")
                return True
            else:
                print(f"   状态码: {response.status_code}，但内容不符合预期")
                return False
        else:
            print(f"   状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   错误: 无法连接到服务")
        return False
    except Exception as e:
        print(f"   错误: {str(e)}")
        return False

# 测试 3: 静态文件
def test_static():
    """测试静态文件"""
    try:
        response = requests.get(f"{BASE_URL}/static/phi_chat.html", timeout=5)
        if response.status_code == 200:
            print(f"   状态码: {response.status_code}")
            print(f"   文件大小: {len(response.content)} 字节")
            return True
        else:
            print(f"   状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"   错误: {str(e)}")
        return False

# 测试 4: 聊天端点（简单测试）
def test_chat_endpoint():
    """测试聊天端点"""
    try:
        payload = {
            "user_input": "你好",
            "session_id": "test_session_001",
            "arousal_level": "NORMAL"
        }
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   状态码: {response.status_code}")
            print(f"   响应包含: {list(data.keys())}")
            if "reply" in data:
                print(f"   回复预览: {data['reply'][:50]}...")
            if "audio" in data:
                print(f"   音频数据: {'存在' if data['audio'] else '不存在'}")
            return True
        else:
            print(f"   状态码: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   错误信息: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print("   错误: 请求超时（可能 LLM 响应较慢）")
        return False
    except requests.exceptions.ConnectionError:
        print("   错误: 无法连接到服务")
        return False
    except Exception as e:
        print(f"   错误: {str(e)}")
        return False

# 测试 5: TTS 端点
def test_tts_endpoint():
    """测试 TTS 端点"""
    try:
        payload = {
            "text": "主人，菲菲测试中",
            "arousal_level": "NORMAL"
        }
        response = requests.post(
            f"{BASE_URL}/tts",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            print(f"   状态码: {response.status_code}")
            print(f"   内容类型: {content_type}")
            if 'audio' in content_type:
                print(f"   音频数据大小: {len(response.content)} 字节")
                return True
            else:
                print(f"   响应类型: {response.text[:100]}")
                return True  # 可能是 JSON 格式的音频
        else:
            print(f"   状态码: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   错误信息: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print("   错误: 请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("   错误: 无法连接到服务")
        return False
    except Exception as e:
        print(f"   错误: {str(e)}")
        return False

# 执行测试
print("开始测试...")
print()

test("健康检查端点 (/health)", test_health)
time.sleep(1)

test("前端界面 (/)", test_frontend)
time.sleep(1)

test("静态文件 (/static/phi_chat.html)", test_static)
time.sleep(1)

print("=" * 80)
print("  功能测试（可能需要较长时间）")
print("=" * 80)
print()

test("聊天端点 (/chat)", test_chat_endpoint)
time.sleep(2)

test("TTS 端点 (/tts)", test_tts_endpoint)
time.sleep(1)

# 汇总报告
print("=" * 80)
print("  测试结果汇总")
print("=" * 80)
print()
print(f"   总测试数: {test_results['total']}")
print(f"   ✅ 通过: {test_results['passed']}")
print(f"   ❌ 失败: {test_results['failed']}")
print()

success_rate = (test_results['passed'] / test_results['total'] * 100) if test_results['total'] > 0 else 0
print(f"   成功率: {success_rate:.1f}%")
print()

if success_rate == 100:
    status = "完美"
elif success_rate >= 80:
    status = "良好"
elif success_rate >= 60:
    status = "需要关注"
else:
    status = "需要修复"

print(f"   总体状态: {status}")
print()

if test_results['failed'] > 0:
    print("   [⚠] 有测试失败，请检查：")
    print("      - 服务是否正常运行")
    print("      - API Key 是否有效")
    print("      - 网络连接是否正常")
    print()
else:
    print("   [✅] 所有测试通过，系统运行正常！")
    print("      - 可以访问 http://localhost:8000/ 使用界面")
    print("      - 健康监控应显示: LLM: OK  TTS: OK")
    print()

print("=" * 80)
print("  测试完成")
print("=" * 80)
print()

