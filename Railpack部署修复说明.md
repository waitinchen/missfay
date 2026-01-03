# ✅ Railpack 部署修复说明

## 问题分析

根据日志文件 `logs.1767433860257.log`，Railpack 构建失败的原因：

1. **缺少启动脚本**: Railpack 找不到 `start.sh` 脚本
2. **无法识别项目类型**: 虽然项目包含 Python 文件，但 Railpack 无法自动确定如何构建

## 修复方案

### 已创建的文件

1. **`start.sh`** - Railpack 启动脚本
   - 设置环境变量 `PYTHONUNBUFFERED=1`
   - 从环境变量读取 `PORT`（Railway/Railpack 会自动提供）
   - 使用 `uvicorn` 启动 FastAPI 应用

2. **`Procfile`** - 备用启动配置
   - 提供标准的 Procfile 格式
   - 适用于 Railway 和其他支持 Procfile 的平台

3. **`runtime.txt`** - Python 版本指定
   - 指定 Python 3.11.0
   - 确保使用兼容的 Python 版本

4. **`railway.json`** - Railway 平台配置（可选）
   - 明确指定构建命令和启动命令
   - 配置重启策略

### 文件内容

#### `start.sh`
```bash
#!/bin/bash
# Railpack 启动脚本
# 启动 Voice Bridge 服务

# 设置环境变量
export PYTHONUNBUFFERED=1

# 检查端口环境变量（Railway/Railpack 会提供 PORT）
if [ -z "$PORT" ]; then
    PORT=8000
fi

# 启动 FastAPI 应用
exec uvicorn voice_bridge:app --host 0.0.0.0 --port $PORT
```

#### `Procfile`
```
web: uvicorn voice_bridge:app --host 0.0.0.0 --port $PORT
```

#### `runtime.txt`
```
python-3.11.0
```

## 部署步骤

### 1. 确保文件已提交到 Git

```bash
git add start.sh Procfile runtime.txt railway.json
git commit -m "feat: 添加 Railpack 部署配置文件"
git push
```

### 2. 环境变量配置

在 Railway/Railpack 平台设置以下环境变量：

- `CARTESIA_API_KEY` - Cartesia TTS API 密钥
- `GEMINI_API_KEY` - Gemini LLM API 密钥
- `LONG_TERM_MEMORY_PATH` - 长期记忆文件路径（可选）
- `PHI_CONTEXT_WINDOW` - 上下文窗口大小（可选，默认 15）
- `GEMINI_MODEL` - Gemini 模型名称（可选，默认 gemini-2.0-flash-exp）

### 3. 重新部署

推送代码后，Railpack 应该能够：
1. 识别 Python 项目（通过 `requirements_phi.txt`）
2. 找到启动脚本（`start.sh`）
3. 正确构建和部署应用

## 验证

部署成功后，应该能够访问：
- `https://your-app.railway.app/` - 聊天界面
- `https://your-app.railway.app/health` - 健康检查端点
- `https://your-app.railway.app/chat` - API 端点

## 注意事项

1. **端口配置**: Railway/Railpack 会自动提供 `PORT` 环境变量，应用会自动使用
2. **静态文件**: 确保 `static/` 目录中的所有文件都已提交到 Git
3. **环境变量**: 不要在代码中硬编码 API 密钥，必须使用环境变量
4. **依赖安装**: `requirements_phi.txt` 必须包含所有必需的依赖

## 菲菲的确认

> [excited] 主人，菲菲已经创建了 Railpack 部署所需的配置文件！
> 
> [gasp] 包括启动脚本、Procfile、Python 版本指定，所有必要的文件都有了！
> 
> [whisper] 现在 Railpack 应该能够正确识别和构建菲菲的项目了！
> 
> [happy] 主人只需要提交这些文件并重新部署就可以了！

---

**修复完成时间**: 2026-01-03  
**状态**: ✅ Railpack 部署配置文件已创建  
**下一步**: 提交文件并重新部署

