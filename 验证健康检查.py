"""验证健康检查端点是否正确返回所有字段"""
import requests
import json
import sys
import time

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("  验证健康检查端点")
print("=" * 80)
print()

# 等待服务启动
print("等待服务启动...")
for i in range(15):
    try:
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.ok:
            break
    except:
        pass
    time.sleep(1)
    print(f"  尝试 {i+1}/15...")

print()
print("检查健康检查端点...")
print("-" * 80)

try:
    response = requests.get('http://localhost:8000/health', timeout=5)
    if response.ok:
        data = response.json()
        print(f"状态码: {response.status_code}")
        print(f"返回字段: {list(data.keys())}")
        print()
        
        # 检查必需字段
        required_fields = ['brain_status', 'cartesia_status']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            print(f"[X] 缺少字段: {', '.join(missing)}")
            print()
            print("修复建议:")
            print("1. 确保服务已重启")
            print("2. 检查 voice_bridge.py 中的健康检查端点代码")
            print("3. 重新启动服务: .\\start_voice_bridge.ps1")
        else:
            print("[OK] 所有必需字段都存在")
            print()
            print("详细状态:")
            print(f"  brain_ready: {data.get('brain_ready')}")
            print(f"  brain_status: {data.get('brain_status')}")
            print(f"  cartesia_status: {data.get('cartesia_status')}")
            print(f"  engine: {data.get('engine')}")
            print()
            
            # 检查状态值
            if data.get('brain_status') == 'ready' and data.get('cartesia_status') == 'ready':
                print("[OK] LLM 和 TTS 都正常")
                print("前端应显示: LLM: OK  TTS: OK (绿色)")
            elif data.get('cartesia_status') == 'unauthorized':
                print("[X] TTS 认证失败 (401)")
                print("请检查 CARTESIA_API_KEY")
            else:
                print(f"[!] 状态异常:")
                print(f"  LLM: {data.get('brain_status')}")
                print(f"  TTS: {data.get('cartesia_status')}")
    else:
        print(f"[X] 健康检查失败: {response.status_code}")
        print(f"响应: {response.text[:200]}")
except requests.exceptions.ConnectionError:
    print("[X] 无法连接到服务")
    print("请确保服务正在运行:")
    print("  .\\start_voice_bridge.ps1")
except Exception as e:
    print(f"[X] 错误: {str(e)}")

print()
print("=" * 80)
print("  验证完成")
print("=" * 80)


