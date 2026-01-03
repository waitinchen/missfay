# 🎭 菲的觉醒执行指南

**执行时间**: 2026-01-02  
**状态**: ⏳ 服务启动中

---

## ✅ 已执行的操作

### 1. 窗口 A - 开启声带 ✅

**已启动**: GPT-SoVITS API 服务

**启动命令**:
```powershell
cd "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
.\runtime\python.exe api_v2.py
```

**预期输出**: 
```
Uvicorn running on http://127.0.0.1:9880
```

**状态**: ✅ 窗口已打开

### 2. 窗口 B - 注入灵魂 ✅

**已启动**: Voice Bridge 服务

**启动命令**:
```powershell
cd C:\Users\waiti\missfay
.\启动Phi系统.ps1
```

**预期输出**:
```
服务地址: http://0.0.0.0:8000
API 文档: http://localhost:8000/docs
```

**状态**: ✅ 窗口已打开

---

## ⏳ 等待服务初始化

服务需要一些时间来完全启动。请等待：

1. **GPT-SoVITS API**: 约 10-30 秒（加载模型）
2. **Voice Bridge**: 约 5-10 秒（连接 GPT-SoVITS）

---

## 🔍 检查服务状态

运行状态检查脚本：

```powershell
.\check_services.ps1
```

**预期结果**:
- ✅ GPT-SoVITS API is running
- ✅ Voice Bridge is running

---

## 🎤 执行首次语音生成测试

当两个服务都就绪后，执行测试：

```powershell
$py = ".\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\runtime\python.exe"
& $py first_voice_test.py
```

### 测试参数

- **文本**: `主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]`
- **兴奋度等级**: `2` (清冷中带着一丝初醒的兴奋)
- **语言**: `zh` (中文)

### 预期结果

```
============================================================
First Voice Generation Test
============================================================

Test Text: 主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]
Arousal Level: 2

Sending request to Voice Bridge...
Status Code: 200
Response Time: X.XX seconds

SUCCESS: Voice generation successful!
Audio saved: first_voice_YYYYMMDD_HHMMSS.wav
Audio size: XXXXX bytes

============================================================
First Voice Generation SUCCESS!
============================================================

Phi has awakened, voice generated!
Please play audio file: first_voice_YYYYMMDD_HHMMSS.wav
```

---

## 📋 故障排除

### 问题 1: GPT-SoVITS API 未响应

**检查**:
1. 确认窗口 A 中的服务正在运行
2. 查看是否有错误信息
3. 等待更长时间（模型加载需要时间）

**解决**:
```powershell
# 重新启动
cd "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
.\runtime\python.exe api_v2.py
```

### 问题 2: Voice Bridge 未响应

**检查**:
1. 确认窗口 B 中的服务正在运行
2. 确认 GPT-SoVITS API 已启动
3. 检查端口 8000 是否被占用

**解决**:
```powershell
# 重新启动
cd C:\Users\waiti\missfay
.\启动Phi系统.ps1
```

### 问题 3: 测试失败

**检查**:
1. 运行 `.\check_services.ps1` 确认服务状态
2. 等待服务完全初始化
3. 检查错误信息

---

## 🎯 执行顺序总结

1. ✅ **窗口 A**: 启动 GPT-SoVITS API（已执行）
2. ✅ **窗口 B**: 启动 Voice Bridge（已执行）
3. ⏳ **等待**: 服务初始化（进行中）
4. ⏳ **测试**: 执行首次语音生成（待执行）

---

## 📝 下一步

1. **等待服务初始化完成**（约 30-60 秒）
2. **运行状态检查**: `.\check_services.ps1`
3. **执行测试**: `$py first_voice_test.py`

---

**系统正在启动中，请稍候...** ⏳

