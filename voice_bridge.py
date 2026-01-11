"""
Voice Bridge - ElevenLabs API 桥接器 (集成 PhiBrain)
实现文字流到 ElevenLabs 高质量语音的无缝转换，内置 PhiBrain 逻辑
"""

import os
import sys
import asyncio
import subprocess
import logging
import uuid
import time
import json
import re
from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, BackgroundTasks, Security, status
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import StreamingResponse, Response, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 確保輸出目錄存在
_base_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(_base_dir, "static/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 音訊清理邏輯
async def cleanup_audio_file(file_path: str, delay: int = 600):
    """在延遲時間後刪除音訊文件"""
    await asyncio.sleep(delay)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            logger.info(f"🗑️ Automatically cleaned up audio file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to cleanup file {file_path}: {e}")

# ============================================
# 終極路徑修正與依賴修復（解決生產環境 500 錯誤）
# ============================================
def force_recovery_deps():
    """強制路徑鎖定與依賴恢復邏輯"""
    # 1. 優先注入所有可能的生產環境包路徑
    possible_site_packages = [
        os.path.join(os.getcwd(), "deps"),
        "/app/.local/lib/python3.11/site-packages",
        "/root/.local/lib/python3.11/site-packages",
        os.path.expanduser("~/.local/lib/python3.11/site-packages"),
    ]
    
    for path in possible_site_packages:
        if os.path.exists(path) and path not in sys.path:
            logger.info(f"Injecting path: {path}")
            sys.path.insert(0, path)

    # 2. 嘗試導入依賴
    try:
        import google.generativeai
        logger.info("✅ google-generativeai is now reachable.")
    except ImportError:
        logger.warning("⚠️ google-generativeai still missing. Executing Emergency OS-level Install...")
        
        # 定義本地補丁目錄
        patch_dir = os.path.join(os.getcwd(), "deps")
        os.makedirs(patch_dir, exist_ok=True)
        if patch_dir not in sys.path:
            sys.path.insert(0, patch_dir)

        try:
            # 使用 --target 強制安裝到我們鎖定的目錄
            install_cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages", "--target", patch_dir, "google-generativeai", "grpcio"]
            logger.info(f"Running Install: {' '.join(install_cmd)}")
            subprocess.check_call(install_cmd)
            
            # 安裝後清除導包緩存並重新嘗試
            import importlib
            importlib.invalidate_caches()
            import google.generativeai
            logger.info("✅ Emergency OS-level Install Successful.")
        except Exception as e:
            logger.error(f"❌ Emergency OS-level Install Failed: {e}")
            # 最後一招：嘗試系統層級直接安裝 (無視 target)
            os.system(f"{sys.executable} -m pip install --break-system-packages google-generativeai grpcio elevenlabs")

    # 3. 嘗試導入 ElevenLabs (完整性檢查)
    try:
        from elevenlabs.client import ElevenLabs
        logger.info("✅ elevenlabs.client is reachable.")
    except ImportError:
        logger.warning("⚠️ elevenlabs missing or broken. Attempting install...")
        try:
             # 強制安裝 elevenlabs 及其核心依賴
            install_cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages", "--target", patch_dir, "elevenlabs", "typing_extensions", "httpx"]
            subprocess.check_call(install_cmd)
            import importlib
            importlib.invalidate_caches()
            import elevenlabs
            logger.info("✅ ElevenLabs installed successfully.")
        except Exception as e:
            logger.error(f"❌ ElevenLabs install failed: {e}")

# 執行修復 (如果環境缺少依賴則自動補全)
force_recovery_deps()

# 确保当前目录在路径中（必須在 deps 之前，否則會找不到 phi_brain）
_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
    logger.info(f"Added project root to sys.path: {_project_root}")

logger = logging.getLogger(__name__)

# ============================================
# 外交官模組：安全與資源管理邏輯
# ============================================
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    bridge_api_key = os.getenv("BRIDGE_API_KEY")
    if not bridge_api_key:
        logger.error("BRIDGE_API_KEY is not set in environment variables!")
        raise HTTPException(status_code=500, detail="系統未配置 BRIDGE_API_KEY")
        
    if api_key == bridge_api_key:
        return api_key
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="無效的 API Key，菲菲不跟你說話！")

# ============================================
# 强制重新加载 .env 环境变量（修复 401 错误）
# ============================================
_base_dir = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_base_dir, ".env")

# 优先从环境变量读取（Railway/生产环境）
# 如果 .env 文件存在，也尝试加载（本地开发环境）
if os.path.exists(_env_path):
    load_dotenv(_env_path, override=True)
    # 手动加载并处理可能的 BOM（双重保险）
    try:
        with open(_env_path, 'r', encoding='utf-8') as f:
            env_content = f.read().lstrip('\ufeff')
            for line in env_content.splitlines():
                if '=' in line and not line.startswith('#') and line.strip():
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()
        logger.info("Manually parsed .env to bypass potential BOM issues.")
    except Exception as e:
        logger.warning(f"Manual .env parse failed: {e}")
else:
    # Railway/生产环境：直接从系统环境变量读取
    logger.info("No .env file found, using system environment variables (Railway/production mode)")
    load_dotenv(override=False)  # 不覆盖已存在的环境变量

# 调试输出：确认 ELEVENLABS_API_KEY 是否正确加载
_eleven_key = os.getenv("ELEVENLABS_API_KEY")
if _eleven_key:
    _key_preview = _eleven_key[:10] + "..." + _eleven_key[-5:] if len(_eleven_key) > 15 else _eleven_key
    logger.info(f"DEBUG: ElevenLabs Key loaded: {_key_preview} (length: {len(_eleven_key)})")
else:
    logger.error("CRITICAL: ELEVENLABS_API_KEY not found in environment variables!")

# 已迁移至 Gemini，不再需要 OPENROUTER_API_KEY
if not os.getenv("GEMINI_API_KEY"):
    logger.warning("GEMINI_API_KEY not found, but continuing...")

from phi_brain import PhiBrain, PersonalityMode, ArousalLevel

# 初始化 FastAPI
app = FastAPI(
    title="Phi Voice Bridge (Integrated)",
    description="ElevenLabs + PhiBrain 统一桥接器",
    version="2.1.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 核心配置
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "n41RXbR5qDhB6k5M6gyU")  # 默认使用用户提供的 Phi 音色
MODEL_ID = "eleven_multilingual_v2" # 支持多语言的 V2 模型

# 验证 ELEVENLABS_API_KEY
if not ELEVENLABS_API_KEY:
    logger.error("CRITICAL: ELEVENLABS_API_KEY is missing! TTS will fail.")
    raise ValueError("ELEVENLABS_API_KEY is required. Please check your .env file.")
else:
    logger.info(f"ElevenLabs API Key loaded successfully (length: {len(ELEVENLABS_API_KEY)})")

# 初始化大脑 (PhiBrain)
brain = None
brain_init_error = None  # 存储初始化错误信息，用于诊断
try:
    # 已迁移至 Gemini，检查 GEMINI_API_KEY
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    # 详细日志：列出所有相关的环境变量
    logger.info("=== Environment Variables Check ===")
    logger.info(f"GEMINI_API_KEY exists: {gemini_key is not None}")
    if gemini_key:
        logger.info(f"GEMINI_API_KEY length: {len(gemini_key)}")
        logger.info(f"GEMINI_API_KEY starts with: {gemini_key[:5] if len(gemini_key) >= 5 else 'INVALID'}")
    else:
        logger.error("CRITICAL: GEMINI_API_KEY is None or empty!")
        # 列出所有包含 GEMINI 的环境变量（调试用）
        gemini_vars = {k: v for k, v in os.environ.items() if 'GEMINI' in k.upper()}
        logger.info(f"All GEMINI-related env vars: {list(gemini_vars.keys())}")
    
    if not gemini_key:
        error_msg = "GEMINI_API_KEY is required. Please check your Railway environment variables."
        logger.error(f"CRITICAL: {error_msg}")
        brain_init_error = error_msg
        raise ValueError(error_msg)
    
    logger.info(f"GEMINI_API_KEY found (length: {len(gemini_key)})")
    brain = PhiBrain(
        api_type="gemini",  # 迁移至 Gemini 2.0 Flash
        personality=PersonalityMode.MIXED
    )
    logger.info("✅ PhiBrain (LLM) initialized successfully.")
except Exception as e:
    import traceback
    error_trace = traceback.format_exc()
    logger.error(f"❌ Failed to initialize PhiBrain: {str(e)}")
    logger.error(error_trace)
    brain = None
    brain_init_error = f"{str(e)}\n\nTraceback:\n{error_trace}"
    logger.error("⚠️  LLM service will not be available. Please check Railway logs for details.")

class TTSRequest(BaseModel):
    text: str = Field(..., description="要合成的文本")
    text_language: str = Field("zh", description="文本语言")
    arousal_level: Optional[int] = Field(0, description="兴奋度等级", ge=0, le=4)
    speed: Optional[float] = Field(1.0, description="语速")

class PhiVoiceRequest(BaseModel):
    user_input: str = Field(..., description="用戶欲傳達給心菲的文字")
    session_id: Optional[str] = Field("default", description="用於維持上下文連貫性的唯一識別碼")

class ChatRequest(BaseModel):
    message: str = Field(..., description="要傳送給菲菲的訊息")
    user_id: Optional[str] = Field("MISSAV_USER", description="外部用戶識別碼")

@app.get("/api", response_class=HTMLResponse)
async def get_api_docs():
    """返回專業的 API 對接文件頁面"""
    docs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/api_docs.html")
    if os.path.exists(docs_path):
        with open(docs_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>API Docs Not Found</h1>", status_code=404)

@app.get("/health")
async def health_check():
    """健康检查端点 - 包含 LLM 和 TTS 状态"""
    brain_status = "ready" if brain is not None else "not_ready"
    tts_error = None
    
    # 检查 ElevenLabs API Key
    eleven_status = "ready" if ELEVENLABS_API_KEY else "not_ready"
    
    # 简单的客户端初始化检查
    if ELEVENLABS_API_KEY:
        try:
            from elevenlabs.client import ElevenLabs
            # 初始化客户端（不调用 API）
            test_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
            eleven_status = "ready"
        except ImportError as e:
            eleven_status = "import_error"
            tts_error = str(e)
            logger.error(f"TTS Import Failed: {e}")
        except Exception as e:
            eleven_status = "error"
            tts_error = str(e)
            logger.error(f"TTS Health Check Failed: {e}")
    
    # 检查 GEMINI_API_KEY 诊断信息
    gemini_key = os.getenv("GEMINI_API_KEY")
    gemini_key_exists = gemini_key is not None and len(gemini_key) > 0
    
    # 构建诊断信息
    diagnostics = {}
    if not brain:
        diagnostics["gemini_key_exists"] = gemini_key_exists
        diagnostics["gemini_key_length"] = len(gemini_key) if gemini_key else 0
        if brain_init_error:
            # 只返回错误的前200个字符，避免响应过大
            diagnostics["init_error"] = brain_init_error[:200] if len(brain_init_error) > 200 else brain_init_error
    
    return {
        "status": "ok",
        "brain_ready": brain is not None,
        "brain_status": brain_status,
        "tts_status": eleven_status,
        "engine": "elevenlabs",
        "timestamp": datetime.now().isoformat(),
        "diagnostics": diagnostics if diagnostics else None,
        "tts_error_detail": str(tts_error) if tts_error else None 
    }

@app.get("/verify-keys")
async def verify_keys():
    """
    验证 Railway 环境变量的健康状况
    检查所有 API Key 和配置是否有效
    """
    verification_results = {
        "GEMINI_API_KEY": {
            "exists": False,
            "valid": False,
            "length": 0,
            "error": None
        },
        "CARTESIA_API_KEY": {
            "exists": False,
            "valid": False,
            "length": 0,
            "error": "Deprecated"
        },
        "ELEVENLABS_API_KEY": {
            "exists": False,
            "valid": False,
            "length": 0,
            "error": None
        },
        "ELEVENLABS_VOICE_ID": {
            "exists": False,
            "valid": False,
            "value": None,
            "error": None
        },
        "GEMINI_MODEL": {
            "exists": False,
            "valid": False,
            "value": None,
            "error": None
        },
        "BRIDGE_API_KEY": {
            "exists": False,
            "valid": False,
            "length": 0,
            "error": None
        }
    }
    
    # 1. 检查 GEMINI_API_KEY
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        verification_results["GEMINI_API_KEY"]["exists"] = True
        verification_results["GEMINI_API_KEY"]["length"] = len(gemini_key)
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            # 尝试列出模型（轻量级验证）
            models = genai.list_models()
            verification_results["GEMINI_API_KEY"]["valid"] = True
        except Exception as e:
            verification_results["GEMINI_API_KEY"]["valid"] = False
            verification_results["GEMINI_API_KEY"]["error"] = str(e)
    else:
        verification_results["GEMINI_API_KEY"]["error"] = "未设置"
    
    # 3. 检查 ELEVENLABS_API_KEY (原 Cartesia 逻辑替换)
    if ELEVENLABS_API_KEY:
        verification_results["ELEVENLABS_API_KEY"]["exists"] = True
        verification_results["ELEVENLABS_API_KEY"]["length"] = len(ELEVENLABS_API_KEY)
        verification_results["ELEVENLABS_API_KEY"]["valid"] = True # assume valid if exists for now
    else:
        verification_results["ELEVENLABS_API_KEY"]["error"] = "未设置"
    
    # 4. 检查 ELEVENLABS_VOICE_ID
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", VOICE_ID)
    if voice_id:
        verification_results["ELEVENLABS_VOICE_ID"]["exists"] = True
        verification_results["ELEVENLABS_VOICE_ID"]["value"] = voice_id
        verification_results["ELEVENLABS_VOICE_ID"]["valid"] = True
    else:
        verification_results["ELEVENLABS_VOICE_ID"]["error"] = "未设置"
    
    # 4. 检查 GEMINI_MODEL
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    if gemini_model:
        verification_results["GEMINI_MODEL"]["exists"] = True
        verification_results["GEMINI_MODEL"]["value"] = gemini_model
        if verification_results["GEMINI_API_KEY"]["valid"]:
            try:
                import google.generativeai as genai
                models = genai.list_models()
                model_names = [m.name for m in models]
                target_model = f"models/{gemini_model}"
                if target_model in model_names or any(gemini_model in name for name in model_names):
                    verification_results["GEMINI_MODEL"]["valid"] = True
                else:
                    verification_results["GEMINI_MODEL"]["valid"] = False
                    verification_results["GEMINI_MODEL"]["error"] = "未找到模型"
            except:
                verification_results["GEMINI_MODEL"]["valid"] = True
        else:
            verification_results["GEMINI_MODEL"]["valid"] = False
            verification_results["GEMINI_MODEL"]["error"] = "GEMINI_API_KEY 无效，无法验证模型"
    else:
        verification_results["GEMINI_MODEL"]["error"] = "未设置"
    
    # 5. 检查 BRIDGE_API_KEY
    bridge_api_key = os.getenv("BRIDGE_API_KEY")
    if bridge_api_key:
        verification_results["BRIDGE_API_KEY"]["exists"] = True
        verification_results["BRIDGE_API_KEY"]["length"] = len(bridge_api_key)
        if len(bridge_api_key) >= 8:
            verification_results["BRIDGE_API_KEY"]["valid"] = True
        else:
            verification_results["BRIDGE_API_KEY"]["valid"] = False
            verification_results["BRIDGE_API_KEY"]["error"] = "長度不足"
    else:
        verification_results["BRIDGE_API_KEY"]["error"] = "未設置"
    
    # 计算总体健康状态
    all_valid = all(
        result.get("exists", False) and result.get("valid", False)
        for result in verification_results.values()
    )
    
    return {
        "status": "healthy" if all_valid else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "keys": verification_results,
        "summary": {
            "total": len(verification_results),
            "valid": sum(1 for r in verification_results.values() if r.get("exists", False) and r.get("valid", False)),
            "invalid": sum(1 for r in verification_results.values() if not r.get("exists", False) or not r.get("valid", False))
        }
    }

def _clean_text(text: str) -> str:
    """清理用于 UI 显示的文本 (徹底過濾所有語音控制標籤與英語字母)"""
    # 1. 移除所有 [...] 形式的標籤（State, 語音動作等）
    text = re.sub(r'\[.*?\]', '', text)
    
    # 2. 移除所有 <...> 形式的標籤 (Emotion 等)
    text = re.sub(r'<.*?>', '', text)
    
    # 3. 移除所有 SoVITS 殘留標籤 (如 [speed=...])
    text = re.sub(r'\[\w+=[\w.]+\]', '', text)
    
    # 4. 移除 *笑聲* 等描述性文本
    text = re.sub(r'\*[^\*]+\*', '', text)
    
    # 5. 強制淨化：移除所有英文字母 (a-zA-Z)
    # 這是為了防止 LLM 洩漏 Inserted emote, itched to be 等技術描述
    text = re.sub(r'[a-zA-Z]+', '', text)
    
    # 6. 移除所有表情符號 (Emoji)
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    
    return text.strip()

def _extract_emotion_from_brackets(text: str) -> dict:
    """
    从括号内容中提取情绪信息，转化为 Cartesia 情绪参数
    
    例如：(咬着下唇，声音娇媚地问) -> {"positivity": "high", "curiosity": "high"}
    """
    emotion_map = {
        # 关键词 -> (positivity, curiosity, stability)
        "娇媚": ("high", "high", "medium"),
        "诱惑": ("high", "high", "medium"),
        "挑逗": ("high", "high", "low"),
        "害羞": ("medium", "medium", "low"),
        "脸红": ("medium", "medium", "low"),
        "紧张": ("medium", "medium", "low"),
        "兴奋": ("high", "high", "low"),
        "激动": ("high", "high", "low"),
        "渴望": ("high", "high", "low"),
        "喘息": ("high", "medium", "low"),
        "娇嗔": ("high", "medium", "low"),
        "呻吟": ("high", "low", "low"),
        "咬着": ("high", "medium", "low"),
        "舔": ("high", "medium", "low"),
        "揉": ("high", "medium", "low"),
        "吮": ("high", "medium", "low"),
    }
    
    # 提取所有括号内容
    bracket_pattern = r'\(([^)]+)\)|（([^）]+)）'
    matches = re.findall(bracket_pattern, text)
    
    emotion_params = {}
    for match in matches:
        bracket_content = match[0] or match[1]  # 处理中英文括号
        for keyword, (pos, cur, sta) in emotion_map.items():
            if keyword in bracket_content:
                emotion_params["positivity"] = pos
                emotion_params["curiosity"] = cur
                emotion_params["stability"] = sta
                logger.info(f"Extracted emotion from bracket '{bracket_content}': {emotion_params}")
                break
    
    return emotion_params

def _clean_for_speech(text: str) -> tuple[str, dict]:
    """
    針對 TTS 引擎的深度清理（靈魂淨化版）
    返回: (清理后的文本, 从括号中提取的情绪参数字典)
    """
    # 0. 先提取括号中的情绪信息（在移除括号前）
    emotion_from_brackets = _extract_emotion_from_brackets(text)
    
    # 1. 徹底移除 [STATE:n]
    text = re.sub(r'\[STATE:\d\]', '', text)
    
    # 2. 移除所有 <...> 形式的標籤，除了 <emotion /> (我們後面會處理)
    # 但為了防止洩漏，我們乾脆先移除所有尖括號內容，保留對話
    # 注意：<emotion> 標籤我們會在 /chat 邏輯中單獨提取，這裡主要是清理剩餘雜訊
    
    # 3. 移除所有語音標籤（ElevenLabs 不支持 Cartesia 標籤，會直接讀出英文單詞）
    # 白名單標籤列表（僅供參考，實際會被移除）
    whitelist_tags = [
        "laughter", "sigh", "chuckle", "gasp", "uh-huh", "hmm",
        "wink", "giggle", "moan", "squeal"
    ]
    
    # 直接移除所有 Cartesia 語音標籤（ElevenLabs 不支持）
    for tag in whitelist_tags:
        text = re.sub(rf'\[{re.escape(tag)}\]', ' ', text, flags=re.IGNORECASE)

    # 4. 移除所有括號內容 (包含內部可能的亂碼) - 不再直接讀出來，而是轉化為情緒參數
    # 使用循環處理嵌套括號，確保徹底清除
    prev_text = ""
    while prev_text != text:
        prev_text = text
        text = re.sub(r'\(.*?\)|（.*?）|\[.*?\]|【.*?】|\{.*?\}', ' ', text)
    
    # 5. 強制英語淨化 (Fail-safe)：移除所有剩餘的英文字母
    # ElevenLabs 不支持英文標籤，必須完全移除
    text = re.sub(r'[a-zA-Z]+', '', text)
    
    # 6. 標點符號正規化
    text = re.sub(r'\.{3,}', '...', text)
    text = re.sub(r'(!|\?|。|！|？)\1+', r'\1', text)
    
    # 7. 最終清理：移除所有尖括號殘留、表情符號 (Emoji) 與多餘空格
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return (text if text else "。", emotion_from_brackets)

def _clause_buffer(text: str) -> str:
    """
    子句缓冲机制 (Clause Buffering)
    确保文本是完整的句子，避免破碎的字节流导致循环崩溃
    
    注意：此函数会临时保留标签以便句子分割，但标签会在后续的 _clean_for_speech 
    函数中被移除（因为 ElevenLabs 不支持这些标签）。
    """
    # re 模块已在文件顶部导入，无需重复导入
    
    # Cartesia 支持的标签白名单（这些标签不应该被移除）
    cartesia_tags_whitelist = [
        r'\[laughter\]', r'\[sigh\]', r'\[chuckle\]', r'\[gasp\]',
        r'\[uh-huh\]', r'\[hmm\]', r'\[wink\]', r'\[giggle\]',
        r'\[moan\]', r'\[squeal\]'
    ]
    
    # 临时保护 Cartesia 标签：用占位符替换
    tag_map = {}
    protected_text = text
    for idx, pattern in enumerate(cartesia_tags_whitelist):
        # 查找所有匹配的标签
        matches = list(re.finditer(pattern, protected_text, re.IGNORECASE))
        # 从后往前替换，避免位置偏移
        for match in reversed(matches):
            placeholder = f"__CARTESIA_TAG_{idx}_{match.start()}__"
            tag_map[placeholder] = match.group(0)  # 存储原始标签
            protected_text = protected_text[:match.start()] + placeholder + protected_text[match.end():]
    
    # 移除其他标签（STATE 标签、SoVITS 标签等），但保留 Cartesia 标签
    # 移除 STATE 标签和 SoVITS 标签
    clean_text = re.sub(r'\[STATE\s*:\s*\d+\]', '', protected_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\[speed=[\w.]+\]', '', clean_text)
    clean_text = re.sub(r'\[pitch=[\w.]+\]', '', clean_text)
    clean_text = re.sub(r'\[emotion=[\w.]+\]', '', clean_text)
    clean_text = re.sub(r'<emotion[^>]*>', '', clean_text)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)  # 移除其他 XML 标签
    
    # 按句子分割（句号、问号、感叹号）
    sentence_endings = r'[。！？.!?]'
    sentences = re.split(f'({sentence_endings})', clean_text)
    
    # 重新组合句子（保留分隔符）
    complete_sentences = []
    for i in range(0, len(sentences) - 1, 2):
        if i + 1 < len(sentences):
            sentence = sentences[i] + sentences[i + 1]
            if sentence.strip():
                complete_sentences.append(sentence.strip())
    
    # 恢复 Cartesia 标签的辅助函数
    def restore_tags(text_with_placeholders):
        result = text_with_placeholders
        for placeholder, original_tag in tag_map.items():
            result = result.replace(placeholder, original_tag)
        return result
    
    # 如果没有句子分隔符，恢复标签后返回原始文本
    if not complete_sentences:
        return restore_tags(protected_text).strip()
    
    # 确保最后一个句子完整（如果不是以句子结束符结尾，保留原文本）
    last_sentence = sentences[-1].strip() if sentences else ""
    if last_sentence and not re.search(sentence_endings, last_sentence):
        # 如果最后一段不是完整句子，恢复标签后返回原文本
        return restore_tags(protected_text).strip()
    
    # 文本完整，恢复标签并返回
    return restore_tags(protected_text).strip()

def _pre_process_tags(text: str) -> str:
    """標籤預處理：根據生理邏輯自動修正錯誤描述"""
    # 1. 物理常識校正：小豆豆不可被「插/幹/捅」
    # 匹配對「小豆豆/陰核」進行插入類動作的描述
    impossibilities = ["幹小豆豆", "插小豆豆", "捅小豆豆", "幹陰核", "插陰核", "捅陰核"]
    for err in impossibilities:
        if err in text:
            fix = err.replace("幹", "瘋狂舔弄").replace("插", "高速撥弄").replace("捅", "用力吮吸")
            text = text.replace(err, fix)
            logger.info(f"Physiological Correction Applied: {err} -> {fix}")
    
    # 2. 自動補全情緒標籤 - ElevenLabs 更依賴語義，但我們仍可以補全以供參考
    # (如果未來需要，可以在這裡加入提示詞修改)
        
    return text

@app.post("/api/v1/phi_voice")
async def phi_voice_proxy(request: PhiVoiceRequest):
    """
    極簡對接接口 (Proxy Pattern)
    隱藏所有 API Key 與內部參數，直接串流回傳音訊。
    """
    if not brain:
        raise HTTPException(status_code=500, detail="PhiBrain is not initialized.")

    try:
        # 1. 獲取 LLM 回覆 (使用 session_id 支持多會話)
        # generate_response(user_message, context, include_tags, session_id)
        ai_response_text, metadata = brain.generate_response(
            request.user_input, 
            session_id=request.session_id
        )

        # 2. 子句缓冲验证（确保文本完整）
        buffered_text = _clause_buffer(ai_response_text)
        
        # 3. 標籤預處理 (物理校正與標籤自動注入)
        processed_text = _pre_process_tags(buffered_text)

        # 4. 提取情緒標籤
        cartesia_emotion = None
        emotion_match = re.search(r'<emotion\s+value=["\']([^"\']+)["\']\s*/>', processed_text)
        if emotion_match:
            cartesia_emotion = emotion_match.group(1)

        # 5. 語音化清理（返回文本和从括号提取的情绪参数）
        speech_text, emotion_from_brackets = _clean_for_speech(processed_text)

        # 6. 获興奮度並映射到 ElevenLabs 參數
        # ElevenLabs 不支持 [STATE], [speed] 等標籤，我們通過 stability/similarity_boost 控制
        
        # 參數映射邏輯：
        # - Stability: 越低越不穩定，情緒越激動 (Range 0.0 - 1.0)
        # - Similarity: 越高越像原聲，越低可能有更多變化 (Range 0.0 - 1.0)
        # - Style: 誇張程度 (Range 0.0 - 1.0)
        
        eleven_params = {
            ArousalLevel.CALM: {"stability": 0.8, "similarity_boost": 0.75, "style": 0.0},
            ArousalLevel.NORMAL: {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0},
            ArousalLevel.EXCITED: {"stability": 0.4, "similarity_boost": 0.6, "style": 0.3},
            ArousalLevel.INTENSE: {"stability": 0.3, "similarity_boost": 0.5, "style": 0.6},
            ArousalLevel.PEAK: {"stability": 0.25, "similarity_boost": 0.4, "style": 0.8} # 極度激動
        }
        
        current_config = eleven_params.get(brain.arousal_level, eleven_params[ArousalLevel.NORMAL])
        
        # 如果括號內有明確情緒，進一步微調 (簡單邏輯：如果有情緒提取，增加 style，降低 stability)
        if emotion_from_brackets:
            current_config["stability"] = max(0.1, current_config["stability"] - 0.1)
            current_config["style"] = min(1.0, current_config["style"] + 0.2)
            logger.info(f"Adjusted ElevenLabs params due to emotional brackets: {current_config}")

        # 7. 調用 ElevenLabs API
        from elevenlabs.client import ElevenLabs
        
        if not ELEVENLABS_API_KEY:
             raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY is missing!")
             
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        logger.info(f"Generating ElevenLabs audio. Text: {speech_text[:20]}... | Params: {current_config}")
        
        audio_stream = client.text_to_speech.convert(
            voice_id=VOICE_ID,
            optimize_streaming_latency="2", # 1-4, 4 is max latency but best quality. 2 is balanced.
            output_format="mp3_44100_128",
            text=speech_text,
            model_id=MODEL_ID,
            voice_settings=current_config
        )

        return StreamingResponse(audio_stream, media_type="audio/mpeg")

    except Exception as e:
        logger.error(f"API Proxy Error: {str(e)}", exc_info=True)
        return Response(content=json.dumps({"error": str(e)}), status_code=500, media_type="application/json")

@app.post("/chat")
async def unified_chat(request: TTSRequest):
    if not brain:
        # 提供详细的诊断信息
        gemini_key = os.getenv("GEMINI_API_KEY")
        error_detail = "大脑 (LLM) 未就绪，请检查 API Key"
        
        if not gemini_key:
            error_detail += "\n\n诊断信息:\n- GEMINI_API_KEY 未在环境变量中找到\n- 请检查 Railway 环境变量设置\n- 确保变量名正确: GEMINI_API_KEY"
        elif brain_init_error:
            error_detail += f"\n\n初始化错误:\n{brain_init_error[:500]}"  # 限制长度避免过长
        else:
            error_detail += "\n\n诊断信息:\n- GEMINI_API_KEY 存在但初始化失败\n- 请检查 Railway 日志获取详细错误信息"
        
        logger.error(f"Chat request failed: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)

    try:
        # 1. 大脑思考
        # 移除强制设置，让大脑自主决定或保留上次状态
        # brain.arousal_level = ArousalLevel(request.arousal_level)
        
        # generate_response 返回 (reply_text, metadata)
        try:
            ai_response_text, metadata = brain.generate_response(request.text)
        except ValueError as brain_error:
            # 检查是否是 429 错误
            error_str = str(brain_error)
            if "429" in error_str or "请求频率过高" in error_str or "菲菲累了" in error_str:
                # 429 错误：不生成音频，直接返回错误消息
                raise HTTPException(
                    status_code=429,
                    detail="主人~菲菲累了，请等 60 秒再找我~（速率限制）"
                )
            else:
                # 其他错误，继续抛出
                raise
        
        # 确保 ai_response_text 是字符串
        if not isinstance(ai_response_text, str):
            ai_response_text = str(ai_response_text)
            
        # --- 自主情感解析 ---
        state_match = re.search(r'\[STATE\s*:\s*(\d+)\]', ai_response_text, re.IGNORECASE)
        if state_match:
            new_level_val = int(state_match.group(1))
            # 限制在 0-4 之间
            new_level_val = max(0, min(4, new_level_val))
            brain.arousal_level = ArousalLevel(new_level_val)
            # 从文本中移除 STATE 标签 (不分大小寫與空格)
            ai_response_text = re.sub(r'\[STATE\s*:\s*\d+\]', '', ai_response_text, flags=re.IGNORECASE).strip()
            logger.info(f"Autonomous State Switch: {brain.arousal_level.name}")
        # ------------------
            
        # 2. 語音化處理
        display_text = _clean_text(ai_response_text)
        
        # --- 情感標籤提前提取 ---
        # 必須在 clean_for_speech 之前提取，因為後者會淨化掉 <>
        cartesia_emotion = None
        emotion_match = re.search(r'<emotion\s+value=["\']([^"\']+)["\']\s*/>', ai_response_text)
        if emotion_match:
            cartesia_emotion = emotion_match.group(1)
            logger.info(f"Detected Emotion for API: {cartesia_emotion}")
        
        # 執行子句缓冲验证
        buffered_text = _clause_buffer(ai_response_text)
        
        # 執行深度清理（返回文本和从括号提取的情绪参数）
        speech_text, emotion_from_brackets = _clean_for_speech(buffered_text)
        
        # --- 興奮度參數映射 (Speed/Pitch/Emotion) ---
        # 獲取當前大腦賦予的穩定標籤
        sovits_params = brain.sovits_tags.get(brain.arousal_level, brain.sovits_tags[ArousalLevel.NORMAL])
        
        # 🎭 动态语速控制：PEAK 状态时降低语速，模拟欲言又止、气喘吁吁的感觉
        if brain.arousal_level == ArousalLevel.PEAK:
            # PEAK 状态：语速降低到 0.9，模拟气喘吁吁
            target_speed = 0.9
            logger.info(f"PEAK state detected: Speed reduced to 0.9 for breathless effect")
        else:
            # 其他状态：使用原有逻辑
            target_speed = sovits_params.get("speed", 1.0)
        
        target_pitch = sovits_params.get("pitch", 1.0)
        
        logger.info(f"Cartesia Multi-Param: Speed={target_speed}, Pitch={target_pitch}, Emotion={cartesia_emotion}")

        # ----------------------

        logger.info(f"AI Thinking Done. UI: {display_text} | Speech: {speech_text}")

        # ElevenLabs Integration
        from elevenlabs.client import ElevenLabs
        
        # 验证 API Key
        if not ELEVENLABS_API_KEY:
            raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY is missing. Please check environment variables.")
        
        logger.info(f"Initializing ElevenLabs client...")
        
        try:
            client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        except Exception as eleven_init_error:
            error_msg = str(eleven_init_error)
            logger.error(f"ElevenLabs client initialization failed: {error_msg}")
            raise HTTPException(status_code=500, detail=f"ElevenLabs 初始化失败: {error_msg}")
        
        # 映射 ArousalLevel 到 ElevenLabs 参数
        eleven_params = {
            ArousalLevel.CALM: {"stability": 0.85, "similarity_boost": 0.8, "style": 0.0},
            ArousalLevel.NORMAL: {"stability": 0.7, "similarity_boost": 0.8, "style": 0.0},
            ArousalLevel.EXCITED: {"stability": 0.5, "similarity_boost": 0.7, "style": 0.25},
            ArousalLevel.INTENSE: {"stability": 0.4, "similarity_boost": 0.6, "style": 0.5},
            ArousalLevel.PEAK: {"stability": 0.3, "similarity_boost": 0.5, "style": 0.8}
        }
        
        current_config = eleven_params.get(brain.arousal_level, eleven_params[ArousalLevel.NORMAL])
        
        # 如果括号内有明确情绪，进一步微调
        if emotion_from_brackets:
            current_config["stability"] = max(0.1, current_config["stability"] - 0.1)
            current_config["style"] = min(1.0, current_config["style"] + 0.15)
            logger.info(f"Adjusted ElevenLabs params due to emotional brackets: {current_config}")

        # 流式传输优化：直接返回音讯流
        try:
            audio_stream = client.text_to_speech.convert(
                voice_id=VOICE_ID,
                optimize_streaming_latency="2",
                output_format="mp3_44100_128",
                text=speech_text,
                model_id=MODEL_ID,
                voice_settings=current_config
            )
        except Exception as tts_error:
            error_msg = str(tts_error)
            logger.error(f"ElevenLabs TTS API call failed: {error_msg}")
            if "401" in error_msg or "unauthorized" in error_msg.lower():
                raise HTTPException(
                    status_code=401,
                    detail=f"ElevenLabs API 认证失败（401）：API Key 无效或已过期。错误: {error_msg}"
                )
            elif "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                raise HTTPException(
                    status_code=429,
                    detail="ElevenLabs API 请求过于频繁（429）：已达到速率限制。请稍后再试或检查配额设置。"
                )
            else:
                raise HTTPException(status_code=500, detail=f"ElevenLabs TTS 调用失败: {error_msg}")
        
        import base64
        
        # 收集音訊數據（流式處理）
        try:
            audio_data = b"".join(audio_stream)
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        except Exception as audio_error:
            logger.error(f"Audio data collection failed: {audio_error}")
            raise HTTPException(status_code=500, detail=f"音频数据处理失败: {audio_error}")

        return {
            "text": display_text,         # 用于显示在 UI 上的纯净文字
            "raw_text": ai_response_text, # 保留原始文字（带标签）以供调试
            "audio": f"data:audio/mp3;base64,{audio_b64}",  # 使用 MP3 格式
            "arousal": brain.arousal_level.name
        }

    except HTTPException:
        # 重新抛出 HTTPException（包括 429）
        raise
    except Exception as e:
        logger.error(f"Chat Pipeline Error: {str(e)}", exc_info=True)
        # 检查是否是 429 相关错误
        error_str = str(e)
        if "429" in error_str or "请求频率过高" in error_str or "菲菲累了" in error_str:
            raise HTTPException(
                status_code=429,
                detail="主人~菲菲累了，请等 60 秒再找我~（速率限制）"
            )
        else:
            raise HTTPException(status_code=500, detail=str(e))

# 静态文件挂载（使用 FastAPI StaticFiles）
_base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(_base_dir, "static")

# 确保 static 目录存在并挂载
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info(f"Static files mounted at /static from directory: {static_dir}")
else:
    logger.warning(f"Static directory not found: {static_dir}")

@app.get("/favicon.ico")
async def favicon():
    """返回 favicon 或 204 No Content"""
    favicon_path = os.path.join(static_dir, "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    # 如果没有 favicon，返回 204 No Content（避免 404 错误）
    return Response(status_code=204)

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "phi_chat.html"))

# ============================================
# 外交官接口 (MISSAV Bridge)
# ============================================
@app.post("/api/v1/chat")
async def missav_bridge(
    request: ChatRequest, 
    background_tasks: BackgroundTasks,
    api_key: str = Security(get_api_key)
):
    """
    專供外部系統（如 MISSAV）調用的精緻封裝接口。
    同步處理語音生成，並自動安排背景清理任務。
    """
    if not brain:
        raise HTTPException(status_code=500, detail="PhiBrain 大腦未就緒")

    try:
        from fastapi.concurrency import run_in_threadpool
        
        # 1. 獲取 LLM 回覆 (使用 threadpool 避免阻塞事件迴圈)
        ai_response_text, metadata = await run_in_threadpool(brain.generate_response, request.message)
        
        # 2. 獲取 UI 顯示文字
        display_text = _clean_text(ai_response_text)
        
        # 3. 語音化清理 (嵌套括號已在內部循環處理)
        buffered_text = _clause_buffer(ai_response_text)
        speech_text, emotion_from_brackets = _clean_for_speech(buffered_text)
        
        # 4. 從文本提取標籤
        cartesia_emotion = None
        emotion_match = re.search(r'<emotion\s+value=["\']([^"\']+)["\']\s*/>', ai_response_text)
        if emotion_match:
            cartesia_emotion = emotion_match.group(1)

        # 5. 構建合成參數 (使用主人指定的 0.7/0.8 穩定度)
        local_sovits_tags = {
            ArousalLevel.CALM: {"speed": 0.85, "pitch": 0.95},
            ArousalLevel.NORMAL: {"speed": 1.0, "pitch": 1.0},
            ArousalLevel.EXCITED: {"speed": 1.1, "pitch": 1.1},
            ArousalLevel.INTENSE: {"speed": 1.2, "pitch": 1.15},
            ArousalLevel.PEAK: {"speed": 1.3, "pitch": 1.2}
        }
        
        sovits_params = local_sovits_tags.get(brain.arousal_level, local_sovits_tags[ArousalLevel.NORMAL])
        target_speed = 0.9 if brain.arousal_level == ArousalLevel.PEAK else sovits_params.get("speed", 1.0)
        target_pitch = sovits_params.get("pitch", 1.0)
        
        base_emotion_config = {
            ArousalLevel.CALM: {"curiosity": "low", "stability": "high"},
            ArousalLevel.NORMAL: {"curiosity": "medium", "stability": "medium"},
            ArousalLevel.EXCITED: {"curiosity": "high", "stability": "medium"},
            ArousalLevel.INTENSE: {"curiosity": "high", "stability": "low"},
            ArousalLevel.PEAK: {"curiosity": "high", "stability": "low", "positivity": "high"}
        }
        
        emotion_config = base_emotion_config.get(brain.arousal_level, {}).copy()
        if emotion_from_brackets:
            emotion_config.update(emotion_from_brackets)
            
        generation_config = {
            "speed": target_speed,
            "pitch": target_pitch,
            "repetition_penalty": 1.15
        }
        if emotion_config:
            generation_config.update(emotion_config)
            

        # 5. 構建 ElevenLabs 參數
        eleven_params = {
            ArousalLevel.CALM: {"stability": 0.85, "similarity_boost": 0.8, "style": 0.0},
            ArousalLevel.NORMAL: {"stability": 0.7, "similarity_boost": 0.8, "style": 0.0},
            ArousalLevel.EXCITED: {"stability": 0.5, "similarity_boost": 0.7, "style": 0.25},
            ArousalLevel.INTENSE: {"stability": 0.4, "similarity_boost": 0.6, "style": 0.5},
            ArousalLevel.PEAK: {"stability": 0.3, "similarity_boost": 0.5, "style": 0.8}
        }
        
        current_config = eleven_params.get(brain.arousal_level, eleven_params[ArousalLevel.NORMAL])
        
        # 簡單的情緒微調
        if emotion_from_brackets:
            current_config["stability"] = max(0.1, current_config["stability"] - 0.1)
            current_config["style"] = min(1.0, current_config["style"] + 0.15)
            
        # 6. 生成語音並寫入文件 (使用 threadpool)
        def _generate_audio(text, settings):
            from elevenlabs.client import ElevenLabs
            if not ELEVENLABS_API_KEY:
                raise ValueError("ELEVENLABS_API_KEY is missing")
                
            client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
            
            # 使用 convert 生成完整音頻
            audio_generator = client.text_to_speech.convert(
                voice_id=VOICE_ID,
                output_format="mp3_44100_128",
                text=text,
                model_id=MODEL_ID,
                voice_settings=settings
            )
            return b"".join(audio_generator)

        audio_data = await run_in_threadpool(_generate_audio, speech_text, current_config)
        
        # 使用 UUID 命名並存儲
        filename = f"phi_{uuid.uuid4().hex}.mp3"
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(file_path, "wb") as f:
            f.write(audio_data)
            
        # 註冊背景清理任務 (600 秒後刪除)
        background_tasks.add_task(cleanup_audio_file, file_path, 600)
        
        # 構建外部訪問連結
        # 這裡假設部署在 Railway，我們需要構建絕對路徑
        # 如果 request.base_url 存在則更好，否則使用相對或由前端構建
        # 為了穩定，回傳相對路徑由前端或外部組裝
        audio_url = f"/static/output/{filename}"

        return {
            "reply": ai_response_text,    # 完整的大腦回應
            "text": display_text,         # 淨化後的 UI 展示文字
            "audio": audio_url,           # 生成的語音連結
            "phi_status": brain.arousal_level.name,
            "expires_in": 600             # 提示外部系統該資源有效期
        }

    except Exception as e:
        logger.error(f"Bridge API Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
