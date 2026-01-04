"""紧急修复：检查并修复健康监控和401错误"""
import requests
import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("  紧急修复：检查健康监控和401错误")
print("=" * 80)
print()

# 1. 检查健康检查端点
print("[1] 检查健康检查端点")
print("-" * 80)
try:
    response = requests.get('http://localhost:8000/health', timeout=5)
    if response.ok:
        data = response.json()
        print(f"   状态码: {response.status_code}")
        print(f"   返回字段: {list(data.keys())}")
        print()
        
        # 检查缺失的字段
        missing_fields = []
        if 'brain_status' not in data:
            missing_fields.append('brain_status')
        if 'cartesia_status' not in data:
            missing_fields.append('cartesia_status')
        
        if missing_fields:
            print(f"   [X] 缺少字段: {', '.join(missing_fields)}")
            print(f"   [建议] 服务可能没有重启，请执行:")
            print(f"      .\\kill_python_processes.ps1")
            print(f"      .\\start_voice_bridge.ps1")
        else:
            print(f"   [OK] 所有字段都存在")
            print(f"   brain_status: {data.get('brain_status')}")
            print(f"   cartesia_status: {data.get('cartesia_status')}")
    else:
        print(f"   [X] 健康检查失败: {response.status_code}")
except Exception as e:
    print(f"   [X] 无法连接到服务: {str(e)}")
    print(f"   [建议] 请确保服务正在运行")

print()

# 2. 测试聊天端点（检查401错误）
print("[2] 测试聊天端点（检查401错误）")
print("-" * 80)
try:
    payload = {
        "text": "测试",
        "arousal_level": 0
    }
    response = requests.post('http://localhost:8000/chat', json=payload, timeout=30)
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 401:
        print(f"   [X] 401 错误：认证失败")
        print(f"   [建议] 请检查 CARTESIA_API_KEY 是否有效")
        try:
            error_data = response.json()
            print(f"   错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"   错误详情: {response.text[:200]}")
    elif response.status_code == 200:
        print(f"   [OK] 聊天端点正常")
        try:
            data = response.json()
            print(f"   响应字段: {list(data.keys())}")
        except:
            pass
    else:
        print(f"   [X] 其他错误: {response.status_code}")
        print(f"   响应: {response.text[:200]}")
except Exception as e:
    print(f"   [X] 请求失败: {str(e)}")

print()
print("=" * 80)
print("  检查完成")
print("=" * 80)
print()


