# MissAV 技术对接规范文档

**项目名称**: 魅惑心菲 (Phi) - 智能语音陪扮系统  
**版本**: v1.0  
**文档日期**: 2026-01-02  
**对接方**: MissAV 技术团队

---

## 📋 项目概述

「魅惑心菲」是一套基于 GPT-SoVITS 的智能语音合成系统，提供实时、高质量的语音陪扮服务。系统采用模块化设计，支持即插即用，可无缝集成到现有平台。

### 核心特性

- ✅ **秒级响应**: 基于 FastAPI 的异步架构，实现毫秒级语音合成
- ✅ **动态情感控制**: 支持 5 级兴奋度调节，实时切换语音风格
- ✅ **多人格模式**: 清冷少女 / 调皮小猫 / 混合模式
- ✅ **流式输出**: 支持实时音频流传输
- ✅ **RESTful API**: 标准化接口，易于集成

---

## 🏗️ 系统架构

```
┌─────────────────┐
│   MissAV 平台   │
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│  Voice Bridge    │  ← FastAPI 桥接层
│  (voice_bridge)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Phi Brain      │  ← 对话生成模块
│  (phi_brain)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GPT-SoVITS     │  ← 语音合成引擎
│  TTS Engine     │
└─────────────────┘
```

---

## 🔌 API 接口规范

### 基础信息

- **Base URL**: `http://your-server:8000`
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8

### 1. 健康检查

**端点**: `GET /health`

**响应示例**:
```json
{
  "status": "ok",
  "gpt_sovits_url": "http://127.0.0.1:9880",
  "gpt_sovits_available": true,
  "timestamp": "2026-01-02T12:00:00"
}
```

### 2. 文本转语音 (TTS)

**端点**: `POST /tts`

**请求体**:
```json
{
  "text": "[speed=1.2][emotion=excited]你好，主人~",
  "text_language": "zh",
  "arousal_level": 3,
  "ref_audio_path": "/path/to/reference.wav",
  "prompt_text": "这是参考音频的文本",
  "prompt_lang": "zh",
  "speed": 1.2,
  "temperature": 0.7,
  "streaming": false
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | ✅ | 要合成的文本（支持 GPT-SoVITS 标签） |
| `text_language` | string | ✅ | 文本语言：zh/en/ja/ko/yue |
| `arousal_level` | integer | ❌ | 兴奋度等级 0-4（默认 0） |
| `ref_audio_path` | string | ❌ | 参考音频路径 |
| `prompt_text` | string | ❌ | 参考音频对应文本 |
| `prompt_lang` | string | ❌ | 参考音频语言 |
| `speed` | float | ❌ | 语速倍数（默认 1.0） |
| `temperature` | float | ❌ | 温度参数（默认 0.6） |
| `streaming` | boolean | ❌ | 是否流式返回（默认 false） |

**响应**:
- **成功**: 返回 WAV 音频流，HTTP 200
- **失败**: 返回 JSON 错误信息，HTTP 4xx/5xx

**响应头**:
```
Content-Type: audio/wav
X-Arousal-Level: 3
X-Sovits-Tags: {"speed":1.2,"emotion":"excited"}
```

### 3. 流式 TTS

**端点**: `POST /tts/stream`

参数与 `/tts` 相同，但强制启用流式模式，实时返回音频块。

---

## 🎭 兴奋度等级 (Arousal Level)

| 等级 | 值 | 描述 | 语速 | 音调 | 适用场景 |
|------|-----|------|------|------|----------|
| CALM | 0 | 冷静/清冷 | 0.9x | 0.95x | 日常对话 |
| NORMAL | 1 | 正常 | 1.0x | 1.0x | 标准交互 |
| EXCITED | 2 | 兴奋 | 1.1x | 1.05x | 互动增强 |
| INTENSE | 3 | 强烈 | 1.2x | 1.1x | 情绪高潮 |
| PEAK | 4 | 峰值 | 1.3x | 1.15x | 极致体验 |

---

## 🏷️ GPT-SoVITS 语法标签

系统支持在文本中嵌入语音控制标签：

### 速度控制
```
[speed=1.2]文本内容
```
- 范围: 0.5 - 2.0
- 默认: 1.0

### 音调控制
```
[pitch=1.1]文本内容
```
- 范围: 0.5 - 2.0
- 默认: 1.0

### 情感控制
```
[emotion=excited]文本内容
```
- 可选值: calm, normal, excited, intense, peak

### 组合使用
```
[speed=1.2][pitch=1.1][emotion=intense]文本内容
```

---

## 🔄 集成流程

### 步骤 1: 环境准备

1. 确保 GPT-SoVITS 服务已启动（`go-webui.bat` 或 `api_v2.py`）
2. 确认服务地址和端口（默认 `http://127.0.0.1:9880`）

### 步骤 2: 启动 Voice Bridge

```bash
# 安装依赖
pip install fastapi uvicorn httpx

# 设置环境变量
export GPT_SOVITS_URL=http://127.0.0.1:9880
export GPT_SOVITS_API_VERSION=v2
export DEFAULT_REF_AUDIO_PATH=/path/to/reference.wav

# 启动服务
python voice_bridge.py
```

### 步骤 3: 调用接口

```python
import requests

# TTS 请求
response = requests.post(
    "http://your-server:8000/tts",
    json={
        "text": "你好，主人~",
        "text_language": "zh",
        "arousal_level": 2
    }
)

# 保存音频
with open("output.wav", "wb") as f:
    f.write(response.content)
```

---

## 📊 性能指标

### 响应时间

| 文本长度 | 平均响应时间 | P95 响应时间 |
|----------|-------------|--------------|
| < 50 字 | < 1s | < 1.5s |
| 50-100 字 | 1-2s | 2.5s |
| 100-200 字 | 2-4s | 5s |

### 并发能力

- **单实例**: 支持 10-20 并发请求
- **多实例**: 可通过负载均衡扩展
- **流式模式**: 延迟 < 500ms

---

## 🔒 安全与认证

### 当前版本
- 无认证（开发阶段）
- 建议部署时添加 API Key 认证

### 生产环境建议
```python
# 在 voice_bridge.py 中添加
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/tts")
async def text_to_speech(
    request: TTSRequest,
    api_key: str = Depends(api_key_header)
):
    # 验证 API Key
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    # ...
```

---

## 🐛 错误处理

### 错误码

| 状态码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | 正常处理 |
| 400 | 请求参数错误 | 检查请求体格式 |
| 404 | 端点不存在 | 检查 URL 路径 |
| 500 | 服务器内部错误 | 查看日志，联系技术支持 |
| 504 | GPT-SoVITS 超时 | 检查 GPT-SoVITS 服务状态 |

### 错误响应格式
```json
{
  "detail": "错误描述信息"
}
```

---

## 📝 测试用例

### 测试 1: 基础 TTS
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，这是测试",
    "text_language": "zh"
  }' \
  --output test.wav
```

### 测试 2: 带兴奋度控制
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "主人，我好兴奋~",
    "text_language": "zh",
    "arousal_level": 3,
    "speed": 1.2
  }' \
  --output excited.wav
```

### 测试 3: 流式输出
```bash
curl -X POST http://localhost:8000/tts/stream \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这是一段较长的文本，用于测试流式输出功能...",
    "text_language": "zh",
    "streaming": true
  }' \
  --output stream.wav
```

---

## 🔧 部署建议

### 开发环境
- 单机部署
- 直接运行 `voice_bridge.py`

### 生产环境
- 使用 Gunicorn + Uvicorn
- 配置 Nginx 反向代理
- 启用 HTTPS
- 添加 API 认证
- 配置日志和监控

### Docker 部署（可选）
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "voice_bridge:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📞 技术支持

- **文档**: 本文档
- **代码仓库**: 项目代码目录
- **问题反馈**: 通过技术对接群组

---

## 📅 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-01-02 | 初始版本，基础 TTS 功能 |

---

**文档结束**

*本规范文档为「魅惑心菲」项目的技术对接标准，如有疑问请联系技术团队。*


