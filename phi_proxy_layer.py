"""
Phi Proxy Layer - API 安全封装层
对外仅暴露 POST /api/v1/phi_voice 接口
隐藏所有敏感信息：CARTESIA_API_KEY, Voice ID, FAY024.md 等

使用说明：
1. 此代理层运行在独立端口（默认 8001）
2. 外部客户端应连接到此代理层，而非直接访问 voice_bridge
3. 所有敏感配置（API Key、Voice ID、内存文件路径）均在服务器端，不会暴露给客户端
"""

import os
import sys
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
from dotenv import load_dotenv

# ============================================
# 强制重新加载 .env 环境变量（修复 401 错误）
# ============================================
_base_dir = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_base_dir, ".env")

# 强制覆盖旧变量
load_dotenv(_env_path, override=True)

# 手动加载并处理可能的 BOM（双重保险）
try:
    with open(_env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
    logging.info("Manually parsed .env to bypass potential BOM issues.")
except Exception as e:
    logging.error(f"Manual .env parse failed: {e}")
    load_dotenv(_env_path, override=True)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建代理层 FastAPI 应用
proxy_app = FastAPI(
    title="Phi Proxy API",
    description="Phi 语音系统安全代理层 - 隐藏内部实现细节",
    version="1.0.0"
)

# 配置 CORS
proxy_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 内部服务地址（voice_bridge 运行地址）
INTERNAL_VOICE_BRIDGE_URL = os.getenv("INTERNAL_VOICE_BRIDGE_URL", "http://127.0.0.1:8000")


class ProxyPhiVoiceRequest(BaseModel):
    """代理层请求模型 - 仅暴露必要字段给外部客户端"""
    user_input: str = Field(..., description="用户输入文本")
    session_id: Optional[str] = Field("default", description="会话ID（可选）")


@proxy_app.post("/api/v1/phi_voice")
async def proxy_phi_voice(request: ProxyPhiVoiceRequest):
    """
    代理端点 - 转发请求到内部 voice_bridge 服务
    
    安全特性：
    - 隐藏 CARTESIA_API_KEY（在服务器端）
    - 隐藏 Voice ID（在服务器端）
    - 隐藏 FAY024.md 等敏感文件路径（在服务器端）
    - 外部客户端只需提供 user_input 和可选的 session_id
    """
    try:
        # 转发请求到内部 voice_bridge 服务
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{INTERNAL_VOICE_BRIDGE_URL}/api/v1/phi_voice",
                json={
                    "user_input": request.user_input,
                    "session_id": request.session_id or "default"
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Internal service error: {response.status_code}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Internal service error: {response.text}"
                )
            
            # 如果是流式响应，直接转发
            content_type = response.headers.get("content-type", "")
            if "audio" in content_type or "stream" in content_type:
                return StreamingResponse(
                    response.iter_bytes(),
                    media_type=content_type
                )
            else:
                return response.json()
        
    except httpx.TimeoutException:
        logger.error("Request timeout")
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        logger.error(f"Proxy Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@proxy_app.get("/health")
async def health_check():
    """健康检查端点"""
    # 检查内部服务是否可用
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            internal_response = await client.get(f"{INTERNAL_VOICE_BRIDGE_URL}/health")
            internal_status = "ok" if internal_response.status_code == 200 else "error"
    except Exception as e:
        internal_status = f"error: {str(e)}"
    
    return {
        "status": "ok",
        "service": "Phi Proxy Layer",
        "version": "1.0.0",
        "internal_service": internal_status
    }


if __name__ == "__main__":
    import uvicorn
    proxy_port = int(os.getenv("PROXY_PORT", "8001"))
    logger.info(f"Starting Phi Proxy Layer on port {proxy_port}...")
    logger.info(f"Internal Voice Bridge URL: {INTERNAL_VOICE_BRIDGE_URL}")
    logger.info("This layer hides sensitive information from external clients")
    logger.info("External clients should connect to this proxy, not voice_bridge directly")
    uvicorn.run(proxy_app, host="0.0.0.0", port=proxy_port)

