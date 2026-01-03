# 首次语音生成测试 - 灵魂语音

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  首次灵魂语音生成测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$packageDir = "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
$pythonPath = "$packageDir\runtime\python.exe"

# 检查 Python
if (-not (Test-Path $pythonPath)) {
    Write-Host "错误: 未找到 Python" -ForegroundColor Red
    pause
    exit 1
}

# 检查 Voice Bridge 服务
Write-Host "检查 Voice Bridge 服务..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "✓ Voice Bridge 服务运行中" -ForegroundColor Green
} catch {
    Write-Host "❌ Voice Bridge 服务未启动" -ForegroundColor Red
    Write-Host "  请先运行 .\启动Phi系统.ps1 启动 Voice Bridge" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""

# 创建测试脚本
$testScript = @"
import requests
import json
import time
from datetime import datetime

print("=" * 60)
print("首次灵魂语音生成测试")
print("=" * 60)
print()

# 测试文本
test_text = "主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]"
arousal_level = 2

print(f"测试文本: {test_text}")
print(f"兴奋度等级: {arousal_level} (清冷中带着一丝初醒的兴奋)")
print()

# 构建请求
url = "http://localhost:8000/tts"
payload = {
    "text": test_text,
    "text_language": "zh",
    "arousal_level": arousal_level,
    "speed": 1.0,
    "temperature": 0.7
}

print("发送请求到 Voice Bridge...")
print(f"URL: {url}")
print()

start_time = time.time()

try:
    response = requests.post(url, json=payload, timeout=60)
    elapsed_time = time.time() - start_time
    
    print(f"状态码: {response.status_code}")
    print(f"响应时间: {elapsed_time:.2f} 秒")
    print()
    
    if response.status_code == 200:
        # 保存音频
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"first_voice_{timestamp}.wav"
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print("✓ 语音生成成功！")
        print(f"✓ 音频已保存: {output_file}")
        print(f"✓ 音频大小: {len(response.content)} 字节")
        print()
        
        # 检查响应头
        arousal_header = response.headers.get("X-Arousal-Level", "N/A")
        tags_header = response.headers.get("X-Sovits-Tags", "N/A")
        
        print("响应头信息:")
        print(f"  兴奋度等级: {arousal_header}")
        print(f"  SoVITS 标签: {tags_header}")
        print()
        
        print("=" * 60)
        print("🎉 首次灵魂语音生成成功！")
        print("=" * 60)
        print()
        print("菲已经醒来，声音已生成！")
        print(f"请播放音频文件: {output_file}")
        
    else:
        print(f"❌ 请求失败")
        try:
            error_data = response.json()
            print(f"错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"错误信息: {response.text[:200]}")
            
except requests.exceptions.RequestException as e:
    print(f"❌ 请求错误: {str(e)}")
    print()
    print("请确保:")
    print("1. Voice Bridge 服务已启动 (http://localhost:8000)")
    print("2. GPT-SoVITS 服务已启动 (http://127.0.0.1:9880)")
except Exception as e:
    print(f"❌ 未知错误: {str(e)}")
    import traceback
    traceback.print_exc()
"@

# 保存测试脚本
$testScript | Out-File -FilePath "first_voice_test.py" -Encoding UTF8

Write-Host "运行测试脚本..." -ForegroundColor Yellow
Write-Host ""

# 安装依赖
& $pythonPath -m pip install requests -q 2>&1 | Out-Null

# 运行测试
& $pythonPath first_voice_test.py

Write-Host ""

