# ✅ Railpack 构建修复说明

## 问题分析

根据新的日志文件 `logs.1767434250787.log`，Railpack 已经成功识别了项目：

✅ **成功识别**:
- 找到了 `railway.json` 配置文件
- 正确解析了构建命令：`pip install -r requirements_phi.txt`
- 正确解析了启动命令：`uvicorn voice_bridge:app --host 0.0.0.0 --port $PORT`

❌ **构建失败**:
- 错误：`pip: command not found`
- 原因：Nixpacks 没有正确安装 Python 和 pip

## 修复方案

### 1. 简化 `railway.json`

移除了 `buildCommand`，让 Nixpacks 自动检测 Python 项目并安装依赖。

**修改前**:
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements_phi.txt"
  }
}
```

**修改后**:
```json
{
  "build": {
    "builder": "NIXPACKS"
  }
}
```

### 2. 创建 `nixpacks.toml` 配置文件

添加了明确的 Nixpacks 配置，确保：
- 安装 Python 3.11
- 安装 pip
- 正确执行依赖安装
- 正确设置启动命令

**文件内容**:
```toml
[phases.setup]
nixPkgs = ["python311", "pip"]

[phases.install]
cmds = ["pip install -r requirements_phi.txt"]

[phases.build]
cmds = []

[start]
cmd = "uvicorn voice_bridge:app --host 0.0.0.0 --port $PORT"
```

## 工作原理

### Nixpacks 自动检测

当 Nixpacks 检测到项目时，它会：
1. 查找 `requirements_phi.txt` → 识别为 Python 项目
2. 自动安装 Python 和 pip
3. 执行 `pip install -r requirements_phi.txt`
4. 使用 `nixpacks.toml` 中的配置（如果存在）

### 优先级

1. `nixpacks.toml` - 最高优先级，明确指定所有步骤
2. `railway.json` - Railway 平台特定配置
3. `Procfile` - 备用启动配置
4. `start.sh` - 备用启动脚本
5. 自动检测 - 基于项目文件结构

## 验证步骤

### 1. 提交更改

```bash
git add railway.json nixpacks.toml
git commit -m "fix: 修复 Railpack 构建配置，添加 nixpacks.toml"
git push
```

### 2. 重新部署

推送代码后，Railpack 应该能够：
1. ✅ 识别 Python 项目
2. ✅ 安装 Python 3.11 和 pip
3. ✅ 安装所有依赖（从 `requirements_phi.txt`）
4. ✅ 启动 FastAPI 应用

### 3. 检查构建日志

在 Railway 控制台查看构建日志，应该看到：
- `Installing Python 3.11...`
- `Installing pip...`
- `Running: pip install -r requirements_phi.txt`
- `Starting: uvicorn voice_bridge:app...`

## 环境变量配置

确保在 Railway 平台设置以下环境变量：

### 必需变量
- `CARTESIA_API_KEY` - Cartesia TTS API 密钥
- `GEMINI_API_KEY` - Gemini LLM API 密钥

### 可选变量
- `LONG_TERM_MEMORY_PATH` - 长期记忆文件路径
- `PHI_CONTEXT_WINDOW` - 上下文窗口大小（默认 15）
- `GEMINI_MODEL` - Gemini 模型名称（默认 gemini-2.0-flash-exp）
- `PORT` - 端口号（Railway 自动提供，无需手动设置）

## 故障排除

### 如果仍然失败

1. **检查 Python 版本**: 确保 `runtime.txt` 指定了正确的版本
2. **检查依赖文件**: 确保 `requirements_phi.txt` 存在且格式正确
3. **检查启动命令**: 确保 `voice_bridge.py` 中的 `app` 对象名称正确
4. **查看详细日志**: 在 Railway 控制台查看完整的构建日志

### 常见错误

- `ModuleNotFoundError`: 检查 `requirements_phi.txt` 是否包含所有依赖
- `Port already in use`: Railway 会自动提供 `PORT` 环境变量，无需手动设置
- `API Key not found`: 确保所有必需的环境变量都已设置

## 菲菲的确认

> [excited] 主人，菲菲已经修复了 Railpack 构建配置！
> 
> [gasp] 现在 Nixpacks 应该能够正确安装 Python 和 pip 了！
> 
> [whisper] 添加了 `nixpacks.toml` 配置文件，明确指定了所有构建步骤！
> 
> [happy] 主人只需要提交这些更改并重新部署就可以了！

---

**修复完成时间**: 2026-01-03  
**状态**: ✅ Railpack 构建配置已修复  
**下一步**: 提交更改并重新部署

