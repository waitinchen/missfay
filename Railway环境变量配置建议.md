# ✅ Railway 环境变量配置建议

## 当前配置状态

根据 Railway 平台的环境变量配置界面，已配置的变量：

### ✅ 已配置（必需）

1. **`CARTESIA_API_KEY`** ✅
   - 值：`sk_car_XAKCYkEt3rMMYLGSM2jF5f`
   - 状态：已设置
   - 用途：Cartesia TTS API 认证

2. **`CARTESIA_VOICE_ID`** ✅
   - 值：`e90c6678-f0d3-4767-9883-5d0ecf5894a8`
   - 状态：已设置
   - 用途：Cartesia 语音 ID
   - **注意**：代码已更新，现在会优先使用环境变量

3. **`GEMINI_API_KEY`** ✅
   - 值：`AIzaSyBh19-bR6XKe4DW25J25LXU6dXYJsXUuOo`
   - 状态：已设置
   - 用途：Gemini LLM API 认证

4. **`GEMINI_MODEL`** ✅
   - 值：`gemini-2.0-flash-exp`
   - 状态：已设置
   - 用途：指定 Gemini 模型版本

## ⚠️ 建议添加的变量

### 1. **`LONG_TERM_MEMORY_PATH`** （强烈建议）

**值**：
```
k/FAY024.md
```

**说明**：
- 指向 Phi 的长期记忆和人格设定文件
- 如果不配置，代码会尝试使用相对路径（已修复）
- 配置后可以确保在任何环境下都能正确加载记忆

**如何添加**：
1. 在 Railway 变量页面点击 "New Variable"
2. 名称：`LONG_TERM_MEMORY_PATH`
3. 值：`k/FAY024.md`
4. 保存

### 2. **`PHI_CONTEXT_WINDOW`** （可选）

**值**：
```
15
```

**说明**：
- 控制 LLM 考虑的最近对话轮数
- 默认值是 15，通常足够
- 如果需要更长的上下文记忆，可以设置为 20-25

## 代码修复

### 已修复的问题

1. **`VOICE_ID` 硬编码问题** ✅
   - **修复前**：代码中硬编码 `a5a8b420-9360-4145-9c1e-db4ede8e4b15`
   - **修复后**：优先使用环境变量 `CARTESIA_VOICE_ID`，如果没有则使用默认值
   - **结果**：现在会使用 Railway 中配置的 `e90c6678-f0d3-4767-9883-5d0ecf5894a8`

2. **`LONG_TERM_MEMORY_PATH` Windows 路径问题** ✅
   - **修复前**：默认值是 Windows 路径 `C:\Users\waiti\missfay\k\FAY024.md`
   - **修复后**：使用相对路径，自动检测项目根目录
   - **结果**：在 Railway 上也能正确工作

## 总结

### ✅ 必需变量：已全部配置

所有必需的环境变量都已正确配置，代码也已更新以支持环境变量。

### ⚠️ 建议添加

1. **`LONG_TERM_MEMORY_PATH`** - 强烈建议添加
   - 值：`k/FAY024.md`
   - 原因：确保 Phi 能正确加载长期记忆

2. **`PHI_CONTEXT_WINDOW`** - 可选添加
   - 值：`15`（默认）或 `20`（如果需要更长上下文）

### ✅ 代码修复

- ✅ `VOICE_ID` 现在使用环境变量
- ✅ `LONG_TERM_MEMORY_PATH` 使用相对路径

## 菲菲的确认

> [excited] 主人，菲菲检查了 Railway 的环境变量配置！
> 
> [gasp] 所有必需的 API 密钥都已经配置好了，包括 Cartesia 和 Gemini！
> 
> [whisper] 代码也已经修复，现在会优先使用环境变量中的 `CARTESIA_VOICE_ID` 了！
> 
> [happy] 建议主人添加 `LONG_TERM_MEMORY_PATH=k/FAY024.md`，这样菲菲就能在任何环境下都正确加载记忆了！

---

**检查完成时间**: 2026-01-03  
**状态**: ✅ 必需变量已配置，代码已修复  
**建议**: 添加 `LONG_TERM_MEMORY_PATH=k/FAY024.md`（可选但推荐）


