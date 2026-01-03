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
import re

# 确保当前目录在路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info("Manually parsed .env to bypass potential BOM issues.")
except Exception as e:
    logger.error(f"Manual .env parse failed: {e}")

# 调试输出：确认 CARTESIA_API_KEY 是否正确加载
_cartesia_key = os.getenv("CARTESIA_API_KEY")
if _cartesia_key:
    _key_preview = _cartesia_key[:10] + "..." + _cartesia_key[-5:] if len(_cartesia_key) > 15 else _cartesia_key
    logger.info(f"DEBUG: Cartesia Key loaded: {_key_preview} (length: {len(_cartesia_key)})")
    print(f"DEBUG: Cartesia Key starts with: {_cartesia_key[:5] if len(_cartesia_key) >= 5 else 'INVALID'}")
else:
    logger.error("CRITICAL: CARTESIA_API_KEY not found in environment variables!")
    print("DEBUG: Cartesia Key starts with: NOT_FOUND")

# 已迁移至 Gemini，不再需要 OPENROUTER_API_KEY
if not os.getenv("GEMINI_API_KEY"):
    logger.warning("GEMINI_API_KEY not found, but continuing...")

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

# 验证 CARTESIA_API_KEY
if not CARTESIA_API_KEY:
    logger.error("CRITICAL: CARTESIA_API_KEY is missing! TTS will fail with 401 error.")
    raise ValueError("CARTESIA_API_KEY is required. Please check your .env file.")
else:
    logger.info(f"Cartesia API Key loaded successfully (length: {len(CARTESIA_API_KEY)})")

# 初始化大脑 (PhiBrain)
try:
    # 已迁移至 Gemini，检查 GEMINI_API_KEY
    if not os.getenv("GEMINI_API_KEY"):
        logger.warning("GEMINI_API_KEY not found, but continuing initialization...")
    
    brain = PhiBrain(
        api_type="gemini",  # 迁移至 Gemini 2.0 Flash
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
    """健康检查端点 - 包含 LLM 和 TTS 状态"""
    brain_status = "ready" if brain is not None else "not_ready"
    
    # 检查 Cartesia API Key
    cartesia_status = "ready" if CARTESIA_API_KEY else "not_ready"
    
    # 如果 Key 存在，尝试初始化客户端（不实际调用 API）
    if CARTESIA_API_KEY:
        try:
            from cartesia import Cartesia
            # 只检查客户端能否初始化，不实际调用 API
            test_client = Cartesia(api_key=CARTESIA_API_KEY)
            cartesia_status = "ready"
        except Exception as e:
            error_str = str(e)
            if "401" in error_str or "unauthorized" in error_str.lower():
                cartesia_status = "unauthorized"
            else:
                cartesia_status = "error"
    
    return {
        "status": "ok",
        "brain_ready": brain is not None,
        "brain_status": brain_status,
        "cartesia_status": cartesia_status,
        "engine": "cartesia",
        "timestamp": datetime.now().isoformat()
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

def _clean_for_speech(text: str) -> str:
    """針對 TTS 引擎的深度清理（靈魂淨化版）"""
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

def _clause_buffer(text: str) -> str:
    """
    子句缓冲机制 (Clause Buffering)
    确保文本是完整的句子，避免破碎的字节流导致循环崩溃
    
    特殊处理：保留 Cartesia 支持的语音标签（[gasp], [moan], [laughter] 等），
    特别是在 PEAK 状态时，这些标签频繁出现，不应被过滤。
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

        # 2. 子句缓冲验证（确保文本完整）
        buffered_text = _clause_buffer(ai_response_text)
        
        # 3. 標籤預處理 (物理校正與標籤自動注入)
        processed_text = _pre_process_tags(buffered_text)

        # 4. 提取情緒標籤
        cartesia_emotion = None
        emotion_match = re.search(r'<emotion\s+value=["\']([^"\']+)["\']\s*/>', processed_text)
        if emotion_match:
            cartesia_emotion = emotion_match.group(1)

        # 5. 語音化清理
        speech_text = _clean_for_speech(processed_text)

        # 6. 獲取興奮度參數 (Prosody)
        sovits_params = brain.sovits_tags.get(brain.arousal_level, brain.sovits_tags[ArousalLevel.NORMAL])
        
        # 7. 調用 Cartesia API (二進位串流模式，使用完整文本)
        from cartesia import Cartesia
        
        # 验证 API Key
        if not CARTESIA_API_KEY:
            raise HTTPException(status_code=500, detail="CARTESIA_API_KEY is missing. Please check .env file.")
        
        logger.info(f"Initializing Cartesia client with key: {CARTESIA_API_KEY[:10]}...")
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
                # 注意：Cartesia API 可能不支持 repetition_penalty 参数
                # 重复问题应在文本生成阶段通过 LLM 的 repetition_penalty 解决
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
        
        # 執行深度清理
        speech_text = _clean_for_speech(buffered_text)
        
        # --- 興奮度參數映射 (Speed/Pitch/Emotion) ---
        # 獲取當前大腦賦予的穩定標籤
        sovits_params = brain.sovits_tags.get(brain.arousal_level, brain.sovits_tags[ArousalLevel.NORMAL])
        target_speed = sovits_params.get("speed", 1.0)
        target_pitch = sovits_params.get("pitch", 1.0)
        
        logger.info(f"Cartesia Multi-Param: Speed={target_speed}, Pitch={target_pitch}, Emotion={cartesia_emotion}")

        # ----------------------

        logger.info(f"AI Thinking Done. UI: {display_text} | Speech: {speech_text}")

        from cartesia import Cartesia
        
        # 验证 API Key
        if not CARTESIA_API_KEY:
            raise HTTPException(status_code=500, detail="CARTESIA_API_KEY is missing. Please check .env file.")
        
        logger.info(f"Initializing Cartesia client with key: {CARTESIA_API_KEY[:10]}...")
        
        try:
            client = Cartesia(api_key=CARTESIA_API_KEY)
        except Exception as cartesia_init_error:
            error_msg = str(cartesia_init_error)
            logger.error(f"Cartesia client initialization failed: {error_msg}")
            if "401" in error_msg or "unauthorized" in error_msg.lower():
                raise HTTPException(
                    status_code=401,
                    detail=f"Cartesia API 认证失败（401）：API Key 无效或已过期。请检查 .env 文件中的 CARTESIA_API_KEY。错误: {error_msg}"
                )
            else:
                raise HTTPException(status_code=500, detail=f"Cartesia 初始化失败: {error_msg}")
        
        # 構建合成參數
        tts_args = {
            "model_id": MODEL_ID,
            "transcript": speech_text,
            "voice": {"mode": "id", "id": VOICE_ID},
            "output_format": {
                "container": "mp3",  # 使用 MP3 格式以優化流式傳輸速度
                "sample_rate": 44100,
                "bit_rate": 128000,  # 128kbps 平衡質量和速度
            },
            "language": "zh",
            "generation_config": {
                "speed": target_speed,
                "pitch": target_pitch,
                "repetition_penalty": 1.15  # 固定重複懲罰，防止循環崩潰
            }
        }
        
        # 如果有情緒標籤，加入 generation_config
        if cartesia_emotion:
            tts_args["generation_config"]["emotion"] = cartesia_emotion

        # 流式傳輸優化：直接返回音訊流，無需等待完整生成
        # 這樣可以讓聲音的出現與文字生成的節奏同步，打造最絲滑的「即時對話感」
        try:
            audio_stream = client.tts.bytes(**tts_args)
        except Exception as tts_error:
            error_msg = str(tts_error)
            logger.error(f"Cartesia TTS API call failed: {error_msg}")
            if "401" in error_msg or "unauthorized" in error_msg.lower():
                raise HTTPException(
                    status_code=401,
                    detail=f"Cartesia TTS API 认证失败（401）：API Key 无效或已过期。请检查 .env 文件中的 CARTESIA_API_KEY。错误: {error_msg}"
                )
            elif "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                raise HTTPException(
                    status_code=429,
                    detail="Cartesia API 请求过于频繁（429）：已达到速率限制。请稍后再试或检查配额设置。"
                )
            else:
                raise HTTPException(status_code=500, detail=f"Cartesia TTS 调用失败: {error_msg}")
        
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

# 静态文件
_base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(_base_dir, "static")

@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    full_path = os.path.join(static_dir, file_path)
    if os.path.exists(full_path):
        return FileResponse(full_path)
    raise HTTPException(status_code=404)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
