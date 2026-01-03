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

