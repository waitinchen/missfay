# 魅惑心菲 (Phi) 系统使用指南

## 📦 已创建的文件

1. **`phi_brain.py`** - 对话生成模块
   - 支持 OpenAI/Claude API
   - 包含 `arousal_level` 参数
   - 自动插入 GPT-SoVITS 语法标签

2. **`voice_bridge.py`** - FastAPI 桥接器
   - 连接 GPT-SoVITS TTS 引擎
   - 提供 RESTful API 接口
   - 支持流式输出

3. **`MissAV_Integration_Spec.md`** - 技术对接文档
   - 完整的 API 规范
   - 集成流程说明
   - 测试用例

4. **`requirements_phi.txt`** - Python 依赖
5. **`启动Phi系统.ps1`** - 快速启动脚本

---

## 🚀 快速开始

### 步骤 1: 安装依赖

```powershell
pip install -r requirements_phi.txt
```

### 步骤 2: 启动 GPT-SoVITS 服务

确保 GPT-SoVITS 已启动：
- 运行 `go-webui.bat`（整合包）
- 或运行 `python api_v2.py`（源码安装）

默认地址：`http://127.0.0.1:9880`

### 步骤 3: 启动 Voice Bridge

**方式一：使用启动脚本（推荐）**
```powershell
.\启动Phi系统.ps1
```

**方式二：手动启动**
```powershell
# 设置环境变量
$env:GPT_SOVITS_URL = "http://127.0.0.1:9880"
$env:GPT_SOVITS_API_VERSION = "v2"

# 启动服务
python voice_bridge.py
```

服务将在 `http://0.0.0.0:8000` 启动

### 步骤 4: 测试接口

访问 API 文档：`http://localhost:8000/docs`

或使用 curl 测试：
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，这是测试", "text_language": "zh"}' \
  --output test.wav
```

---

## 💡 使用示例

### 示例 1: 使用 Phi Brain 生成对话

```python
from phi_brain import PhiBrain, ArousalLevel, PersonalityMode

# 初始化
phi = PhiBrain(
    api_type="openai",
    model="gpt-4",
    personality=PersonalityMode.MIXED
)

# 设置兴奋度
phi.set_arousal_level(ArousalLevel.EXCITED)

# 生成回复
reply, metadata = phi.generate_response("你好，主人~")
print(f"回复: {reply}")
# 输出: [speed=1.10][pitch=1.05][emotion=excited]你好，主人~今天有什么想聊的吗？
```

### 示例 2: 调用 Voice Bridge API

```python
import requests

# TTS 请求
response = requests.post(
    "http://localhost:8000/tts",
    json={
        "text": "[speed=1.2][emotion=excited]主人，我好兴奋~",
        "text_language": "zh",
        "arousal_level": 3
    }
)

# 保存音频
with open("output.wav", "wb") as f:
    f.write(response.content)
```

### 示例 3: 完整流程（对话 + TTS）

```python
from phi_brain import PhiBrain, ArousalLevel
import requests

# 1. 生成对话
phi = PhiBrain()
phi.set_arousal_level(ArousalLevel.INTENSE)
reply, metadata = phi.generate_response("今天心情怎么样？")

# 2. 转换为语音
tts_response = requests.post(
    "http://localhost:8000/tts",
    json={
        "text": reply,
        "text_language": "zh",
        "arousal_level": metadata["arousal_level"]
    }
)

# 3. 保存音频
with open("output.wav", "wb") as f:
    f.write(tts_response.content)
```

---

## 🎛️ 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `GPT_SOVITS_URL` | GPT-SoVITS 服务地址 | `http://127.0.0.1:9880` |
| `GPT_SOVITS_API_VERSION` | API 版本 | `v2` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `ANTHROPIC_API_KEY` | Claude API 密钥 | - |
| `DEFAULT_REF_AUDIO_PATH` | 默认参考音频路径 | - |

### Phi Brain 配置

```python
phi = PhiBrain(
    api_type="openai",  # 或 "claude"
    model="gpt-4",      # 模型名称
    personality=PersonalityMode.MIXED  # 人格模式
)
```

### Voice Bridge 配置

修改 `voice_bridge.py` 中的配置：
```python
GPT_SOVITS_BASE_URL = "http://127.0.0.1:9880"
GPT_SOVITS_API_VERSION = "v2"  # 或 "v1"
```

---

## 📊 兴奋度等级说明

| 等级 | 值 | 语速 | 音调 | 适用场景 |
|------|-----|------|------|----------|
| CALM | 0 | 0.9x | 0.95x | 日常对话 |
| NORMAL | 1 | 1.0x | 1.0x | 标准交互 |
| EXCITED | 2 | 1.1x | 1.05x | 互动增强 |
| INTENSE | 3 | 1.2x | 1.1x | 情绪高潮 |
| PEAK | 4 | 1.3x | 1.15x | 极致体验 |

---

## 🔧 故障排除

### 问题 1: GPT-SoVITS 连接失败

**症状**: `GPT-SoVITS API 错误` 或超时

**解决**:
1. 确认 GPT-SoVITS 服务已启动
2. 检查服务地址和端口
3. 查看 GPT-SoVITS 日志

### 问题 2: 依赖包缺失

**症状**: `ModuleNotFoundError`

**解决**:
```powershell
pip install -r requirements_phi.txt
```

### 问题 3: API Key 错误

**症状**: OpenAI/Claude API 调用失败

**解决**:
1. 设置环境变量：`$env:OPENAI_API_KEY = "your-key"`
2. 或在代码中直接传入 API Key

---

## 📚 更多文档

- **API 文档**: 启动服务后访问 `http://localhost:8000/docs`
- **技术对接文档**: 查看 `MissAV_Integration_Spec.md`
- **GPT-SoVITS 文档**: 查看 `GPT-SoVITS/README.md`

---

## 🎯 下一步

1. ✅ 代码已就绪
2. ⏳ 等待 GPT-SoVITS 解压完成
3. 🚀 启动服务并测试
4. 📝 根据实际需求调整参数

---

**系统已准备就绪，等待部署！**

