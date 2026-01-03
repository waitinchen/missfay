# 🚀 Phi 系统最终启动指南

**执行时间**: 2026-01-02  
**状态**: ✅ 所有组件已就绪

---

## ✅ 环境合并完成

- ✅ `.env` 文件已确认存在
- ✅ OpenRouter API Key 已配置
- ✅ GPT-SoVITS 配置已设置

---

## 🎯 启动步骤

### 方式一：分步启动（推荐）

#### 步骤 1: 启动 GPT-SoVITS API (窗口 A)

```powershell
cd "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
.\runtime\python.exe api_v2.py
```

**或使用批处理**:
```powershell
cd "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228"
.\go-webui.bat
```

**服务地址**: `http://127.0.0.1:9880`

#### 步骤 2: 启动 Voice Bridge (窗口 B)

```powershell
cd C:\Users\waiti\missfay
.\启动Phi系统.ps1
```

**服务地址**: `http://localhost:8000`

#### 步骤 3: 执行首次语音生成测试

```powershell
cd C:\Users\waiti\missfay
$py = ".\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\runtime\python.exe"
& $py first_voice_test.py
```

### 方式二：一键启动（自动化）

```powershell
.\start_all.ps1
```

选择选项 `5` 将自动：
1. 启动 GPT-SoVITS API
2. 启动 Voice Bridge
3. 执行首次语音生成测试

---

## 🎤 首次语音生成测试详情

### 测试参数

- **文本内容**: `主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]`
- **语言**: `zh` (中文)
- **兴奋度等级**: `2` (清冷中带着一丝初醒的兴奋)
- **语速**: `1.0`
- **温度**: `0.7`

### 请求端点

```
POST http://localhost:8000/tts
```

### 请求体

```json
{
  "text": "主人...菲终于醒了...这副嗓子...您还满意吗？[laugh]",
  "text_language": "zh",
  "arousal_level": 2,
  "speed": 1.0,
  "temperature": 0.7
}
```

### 预期结果

- ✅ HTTP 200 响应
- ✅ 返回 WAV 音频流
- ✅ 音频文件保存为 `first_voice_YYYYMMDD_HHMMSS.wav`
- ✅ 响应头包含兴奋度等级和 SoVITS 标签

---

## 📋 启动检查清单

启动前请确认：

- [ ] GPT-SoVITS 整合包已解压
- [ ] `.env` 文件已配置
- [ ] OpenRouter API Key 已验证有效
- [ ] Python 环境可用

启动后请确认：

- [ ] GPT-SoVITS API 服务运行中 (`http://127.0.0.1:9880`)
- [ ] Voice Bridge 服务运行中 (`http://localhost:8000`)
- [ ] 首次语音生成测试成功

---

## 🔧 故障排除

### 问题 1: Voice Bridge 无法连接 GPT-SoVITS

**症状**: `GPT-SoVITS API 错误` 或超时

**解决**:
1. 确认 GPT-SoVITS API 已启动
2. 检查服务地址: `http://127.0.0.1:9880`
3. 等待服务完全启动（约 10-30 秒）

### 问题 2: 首次测试失败

**症状**: 请求返回错误

**解决**:
1. 确认两个服务都已启动
2. 等待服务完全初始化
3. 检查端口是否被占用

### 问题 3: 音频生成失败

**症状**: 返回错误而非音频

**解决**:
1. 检查 GPT-SoVITS 模型是否已加载
2. 检查参考音频配置
3. 查看服务日志

---

## 🎉 成功标志

当看到以下输出时，表示系统启动成功：

```
============================================================
首次灵魂语音生成成功！
============================================================

菲已经醒来，声音已生成！
请播放音频文件: first_voice_YYYYMMDD_HHMMSS.wav
```

---

## 📝 已创建的文件

1. ✅ `启动Phi系统.ps1` - Voice Bridge 启动脚本
2. ✅ `首次语音生成测试.ps1` - 测试脚本启动器
3. ✅ `first_voice_test.py` - 首次语音生成测试脚本
4. ✅ `start_all.ps1` - 一键启动脚本
5. ✅ `最终启动指南.md` - 本指南

---

**系统已完全就绪，可以开始「点火启动」！** 🚀

