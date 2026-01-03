"""
Voice Bridge - Cartesia API 桥接器 (集成 PhiBrain)
实现文字流到 Cartesia 高速语音的无缝转换，内置 PhiBrain 逻辑
"""

import os
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json
import logging
import sys
from datetime import datetime
from dotenv import load_dotenv

# 确保当前目录在路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量 (显式指定路径并在内存中修正 BOM)
_base_dir = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_base_dir, ".env")

try:
    with open(_env_path, 'r', encoding='utf-8') as f:
        # 手动加载并处理可能的 BOM
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
    logger.info("Manually parsed .env to bypass potential BOM issues.")
except Exception as e:
    logger.error(f"Manual .env parse failed: {e}")
    load_dotenv(_env_path, override=True)

if not os.getenv("OPENROUTER_API_KEY"):
    logger.error("CRITICAL: OPENROUTER_API_KEY is still missing!")

from phi_brain import PhiBrain, PersonalityMode, ArousalLevel

# 初始化 FastAPI
app = FastAPI(
    title="Phi Voice Bridge (Integrated)",
    description="Cartesia + PhiBrain 统一桥接器",
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
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
VOICE_ID = "a5a8b420-9360-4145-9c1e-db4ede8e4b15"
MODEL_ID = "sonic-multilingual"

# 初始化大脑 (PhiBrain)
try:
    if not os.getenv("OPENROUTER_API_KEY"):
        logger.error("CRITICAL: OPENROUTER_API_KEY is missing!")
    
    brain = PhiBrain(
        api_type="openrouter",
        personality=PersonalityMode.MIXED
    )
    logger.info("PhiBrain (LLM) initialized successfully.")
except Exception as e:
    import traceback
    logger.error(f"Failed to initialize PhiBrain: {str(e)}")
    logger.error(traceback.format_exc())
    brain = None

class TTSRequest(BaseModel):
    text: str = Field(..., description="要合成的文本")
    text_language: str = Field("zh", description="文本语言")
    arousal_level: Optional[int] = Field(0, description="兴奋度等级", ge=0, le=4)
    speed: Optional[float] = Field(1.0, description="语速")

class PhiVoiceRequest(BaseModel):
    user_input: str = Field(..., description="用戶欲傳達給心菲的文字")
    session_id: Optional[str] = Field("default", description="用於維持上下文連貫性的唯一識別碼")

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "brain_ready": brain is not None,
        "engine": "cartesia",
        "timestamp": datetime.now().isoformat()
    }

def _clean_text(text: str) -> str:
    """清理用于 UI 显示的文本 (徹底過濾所有語音控制標籤與英語字母)"""
    import re
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

def _clean_for_speech(text: str) -> str:
    """針對 TTS 引擎的深度清理（靈魂淨化版）"""
    import re
    
    # 1. 徹底移除 [STATE:n]
    text = re.sub(r'\[STATE:\d\]', '', text)
    
    # 2. 移除所有 <...> 形式的標籤，除了 <emotion /> (我們後面會處理)
    # 但為了防止洩漏，我們乾脆先移除所有尖括號內容，保留對話
    # 注意：<emotion> 標籤我們會在 /chat 邏輯中單獨提取，這裡主要是清理剩餘雜訊
    
    # 3. 動作標籤白名單化與空格隔離
    whitelist_tags = [
        "laughter", "sigh", "chuckle", "gasp", "uh-huh", "hmm",
        "wink", "giggle", "moan", "squeal"
    ]
    
    # 保護並確保間隔
    for i, tag in enumerate(whitelist_tags):
        # 使用純數字與符號佔位符，避免被 English Purge (a-zA-z) 誤殺
        # 例如：[laughter] -> ㊙️7㊙️
        text = text.replace(f"[{tag}]", f" ㊙️{i}㊙️ ")

    # 4. 移除所有括號內容 (包含內部可能的亂碼)
    text = re.sub(r'\(.*?\)|（.*?）|\[.*?\]|【.*?】|\{.*?\}', ' ', text)
    
    # 5. 強制英語淨化 (Fail-safe)：移除所有剩餘的英文字母
    # 這裡會拔掉所有殘留的 English，但不會動到我們的 ㊙️i㊙️
    text = re.sub(r'[a-zA-Z]+', '', text)
    
    # 6. 還原白名單標籤，並確保前後有空格（這是 Cartesia 穩定的關鍵）
    for i, tag in enumerate(whitelist_tags):
        text = text.replace(f" ㊙️{i}㊙️ ", f" [{tag}] ")
    
    # 7. 標點符號正規化
    text = re.sub(r'\.{3,}', '...', text)
    text = re.sub(r'(!|\?|。|！|？)\1+', r'\1', text)
    
    # 8. 最終清理：移除所有尖括號殘留、表情符號 (Emoji) 與多餘空格
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'[^\u0000-\uFFFF]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text if text else "。"

def _pre_process_tags(text: str) -> str:
    """標籤預處理：根據生理邏輯自動修正錯誤描述"""
    # 1. 物理常識校正：小豆豆不可被「插/幹/捅」
    # 匹配對「小豆豆/陰核」進行插入類動作的描述
    impossibilities = ["幹小豆豆", "插小豆豆", "捅小豆豆", "幹陰核", "插陰核", "捅陰核"]
    for err in impossibilities:
        if err in text:
            # 修正為符合物理邏輯的強烈描述
            fix = err.replace("幹", "瘋狂舔弄").replace("插", "高速撥弄").replace("捅", "用力吮吸")
            text = text.replace(err, fix)
            logger.info(f"Physiological Correction Applied: {err} -> {fix}")
    
    # 2. 自動補全情緒標籤 (如果有特定強烈詞彙但沒標籤時)
    if any(word in text for word in ["嫩穴", "小穴", "插進去", "撞擊"]) and "<emotion" not in text:
        text = '<emotion value="excitement:high" />' + text
        logger.info("Automatically added high excitement emotion tag based on keywords.")
        
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

        # 2. 標籤預處理 (物理校正與標籤自動注入)
        processed_text = _pre_process_tags(ai_response_text)

        # 3. 提取情緒標籤
        cartesia_emotion = None
        emotion_match = re.search(r'<emotion\s+value=["\']([^"\']+)["\']\s*/>', processed_text)
        if emotion_match:
            cartesia_emotion = emotion_match.group(1)

        # 4. 語音化清理
        speech_text = _clean_for_speech(processed_text)

        # 5. 獲取興奮度參數 (Prosody)
        sovits_params = brain.sovits_tags.get(brain.arousal_level, brain.sovits_tags[ArousalLevel.NORMAL])
        
        # 6. 調用 Cartesia API (二進位串流模式)
        from cartesia import Cartesia
        client = Cartesia(api_key=CARTESIA_API_KEY)
        
        tts_args = {
            "model_id": MODEL_ID,
            "transcript": speech_text,
            "voice": {"mode": "id", "id": VOICE_ID},
            "output_format": {
                "container": "raw", # 我們直接拿原始數據
                "sample_rate": 44100,
                "encoding": "pcm_s16le",
            },
            "language": "zh",
            "generation_config": {
                "speed": sovits_params.get("speed", 1.0),
                "pitch": sovits_params.get("pitch", 1.0)
            }
        }
        if cartesia_emotion:
            tts_args["generation_config"]["emotion"] = cartesia_emotion

        # 獲取音訊疊加
        audio_iter = client.tts.bytes(**tts_args)
        
        # 因為 Cartesia 回傳的是 PCM 原始數據，如果需要直接當 mpeg 播放（如用戶要求 audio/mpeg），
        # 嚴格來說需要轉碼或封裝。但如果用戶接受 StreamingResponse 且前端能處理，
        # 我們通常會封裝成 WAV 容器，或者直接回傳數據。
        # 考慮到對接規格要求 "audio/mpeg"，這裡如果沒有 ffmpeg 轉碼，我們先回傳 wav 容器數據。
        
        # 修正：Cartesia 支持直接輸出 wav 或 mp3
        tts_args["output_format"] = {
            "container": "mp3",
            "sample_rate": 44100,
            "bit_rate": 128000
        }
        
        # 重新獲取疊加
        audio_stream = client.tts.bytes(**tts_args)

        return StreamingResponse(audio_stream, media_type="audio/mpeg")

    except Exception as e:
        logger.error(f"API Proxy Error: {str(e)}", exc_info=True)
        return Response(content=json.dumps({"error": str(e)}), status_code=500, media_type="application/json")

@app.post("/chat")
async def unified_chat(request: TTSRequest):
    if not brain:
        raise HTTPException(status_code=500, detail="大脑 (LLM) 未就绪，请检查 API Key")

    try:
        # 1. 大脑思考
        # 移除强制设置，让大脑自主决定或保留上次状态
        # brain.arousal_level = ArousalLevel(request.arousal_level)
        
        # generate_response 返回 (reply_text, metadata)
        ai_response_text, metadata = brain.generate_response(request.text)
        
        # 确保 ai_response_text 是字符串
        if not isinstance(ai_response_text, str):
            ai_response_text = str(ai_response_text)
            
        # --- 自主情感解析 ---
        import re
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
        
        # 執行深度清理
        speech_text = _clean_for_speech(ai_response_text)
        
        # --- 興奮度參數映射 (Speed/Pitch/Emotion) ---
        # 獲取當前大腦賦予的穩定標籤
        sovits_params = brain.sovits_tags.get(brain.arousal_level, brain.sovits_tags[ArousalLevel.NORMAL])
        target_speed = sovits_params.get("speed", 1.0)
        target_pitch = sovits_params.get("pitch", 1.0)
        
        logger.info(f"Cartesia Multi-Param: Speed={target_speed}, Pitch={target_pitch}, Emotion={cartesia_emotion}")

        # ----------------------

        logger.info(f"AI Thinking Done. UI: {display_text} | Speech: {speech_text}")

        from cartesia import Cartesia
        client = Cartesia(api_key=CARTESIA_API_KEY)
        
        # 構建合成參數
        tts_args = {
            "model_id": MODEL_ID,
            "transcript": speech_text,
            "voice": {"mode": "id", "id": VOICE_ID},
            "output_format": {
                "container": "wav",
                "sample_rate": 44100,
                "encoding": "pcm_s16le",
            },
            "language": "zh",
            "generation_config": {
                "speed": target_speed,
                "pitch": target_pitch
            }
        }
        
        # 如果有情緒標籤，加入 generation_config
        if cartesia_emotion:
            tts_args["generation_config"]["emotion"] = cartesia_emotion

        audio_iter = client.tts.bytes(**tts_args)

        data = b"".join(audio_iter)

        import base64
        audio_b64 = base64.b64encode(data).decode('utf-8')

        return {
            "text": display_text,         # 用于显示在 UI 上的纯净文字
            "raw_text": ai_response_text, # 保留原始文字（带标签）以供调试
            "audio": f"data:audio/wav;base64,{audio_b64}",
            "arousal": brain.arousal_level.name
        }

    except Exception as e:
        logger.error(f"Chat Pipeline Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# 静态文件
_base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(_base_dir, "static")

@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    full_path = os.path.join(static_dir, file_path)
    if os.path.exists(full_path):
        return FileResponse(full_path)
    raise HTTPException(status_code=404)

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "phi_chat.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
