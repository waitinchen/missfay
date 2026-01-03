# 🌐 Phi 系统本地测试 URL

## 核心服务 URL

### GPT-SoVITS API
- **服务地址**: `http://127.0.0.1:9880`
- **健康检查**: `http://127.0.0.1:9880/health`
- **API 文档**: `http://127.0.0.1:9880/docs` (如果支持)

### Voice Bridge (Phi 系统)
- **服务地址**: `http://localhost:8000`
- **健康检查**: `http://localhost:8000/health`
- **API 文档**: `http://localhost:8000/docs`
- **TTS 端点**: `http://localhost:8000/tts`

---

## 测试端点

### 1. Voice Bridge - TTS 生成

**URL**: `http://localhost:8000/tts`

**方法**: `POST`

**请求体**:
```json
{
  "text": "主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]",
  "text_language": "zh",
  "arousal_level": 2,
  "speed": 1.0,
  "temperature": 0.7
}
```

**响应**: WAV 音频流

**cURL 示例**:
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"测试文本\",\"text_language\":\"zh\",\"arousal_level\":2}" \
  --output test.wav
```

### 2. Voice Bridge - 健康检查

**URL**: `http://localhost:8000/health`

**方法**: `GET`

**响应**:
```json
{
  "status": "healthy",
  "gpt_sovits_connected": true
}
```

### 3. GPT-SoVITS - 健康检查

**URL**: `http://127.0.0.1:9880/health`

**方法**: `GET`

---

## 浏览器测试

### 快速测试 Voice Bridge

1. **健康检查**: 在浏览器打开
   ```
   http://localhost:8000/health
   ```

2. **API 文档**: 在浏览器打开
   ```
   http://localhost:8000/docs
   ```
   可以在这里直接测试 API

### 快速测试 GPT-SoVITS

1. **健康检查**: 在浏览器打开
   ```
   http://127.0.0.1:9880/health
   ```

---

## Python 测试示例

```python
import requests

# 测试 Voice Bridge
url = "http://localhost:8000/tts"
payload = {
    "text": "主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]",
    "text_language": "zh",
    "arousal_level": 2
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    with open("test.wav", "wb") as f:
        f.write(response.content)
    print("Audio saved to test.wav")
```

---

## PowerShell 测试示例

```powershell
# 测试健康检查
Invoke-WebRequest -Uri "http://localhost:8000/health"

# 测试 TTS
$body = @{
    text = "测试文本"
    text_language = "zh"
    arousal_level = 2
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/tts" -Method POST -Body $body -ContentType "application/json"
$response.Content | Set-Content -Path "test.wav" -Encoding Byte
```

---

## 端口说明

- **8000**: Voice Bridge (Phi 系统主服务)
- **9880**: GPT-SoVITS API (TTS 引擎)
- **9874**: GPT-SoVITS WebUI (如果启动)

---

## 快速访问

**复制这些 URL 到浏览器**:

- Voice Bridge 健康检查: `http://localhost:8000/health`
- Voice Bridge API 文档: `http://localhost:8000/docs`
- GPT-SoVITS 健康检查: `http://127.0.0.1:9880/health`

