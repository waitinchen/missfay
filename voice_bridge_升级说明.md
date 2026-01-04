# 🎭 菲菲声音「活起来」升级说明

## 升级目标

让菲菲的声音更加生动，带有喘息与娇嗔，实现以下三个核心功能：

1. **动态语速控制**：PEAK 状态时降低语速，模拟欲言又止、气喘吁吁的感觉
2. **SSML 标签处理**：将括号内容转化为 Cartesia 的情绪权重，而不是直接读出来
3. **情绪参数调整**：增加 "curiosity" 和降低 "stability"，让声音更有感情起伏

## 实现方案

### 1. 动态语速控制

**原理**：
- 当 `arousal_level` 为 PEAK (4) 时，语速从 1.25 降低到 0.9
- 模拟那种欲言又止、气喘吁吁的感觉
- 其他状态保持原有逻辑

**实现位置**：
- `voice_bridge.py` 的 `unified_chat` 函数
- 在调用 Cartesia API 前，根据 `arousal_level` 动态调整 `speed` 参数

### 2. SSML 标签处理（括号内容转化）

**原理**：
- 提取文本中的括号内容，如 `(咬着下唇，声音娇媚地问)`
- 分析括号内容的情感关键词
- 转化为 Cartesia 的情绪权重参数，而不是直接读出来

**关键词映射**：
- "娇媚"、"诱惑"、"挑逗" → `positivity:high, curiosity:high`
- "害羞"、"脸红"、"紧张" → `positivity:medium, curiosity:medium, stability:low`
- "兴奋"、"激动"、"渴望" → `positivity:high, curiosity:high, stability:low`
- "喘息"、"娇嗔"、"呻吟" → `positivity:high, stability:low`

**实现位置**：
- 新增函数 `_extract_emotion_from_brackets(text: str) -> dict`
- 修改 `_clean_for_speech` 函数，在移除括号前先提取情绪信息

### 3. 情绪参数调整

**原理**：
- 在 Cartesia API 调用时，添加 `curiosity` 和 `stability` 参数
- 默认增加 `curiosity:medium`，降低 `stability:low`
- 根据 `arousal_level` 动态调整

**参数映射**：
- CALM (0): `curiosity:low, stability:high`
- NORMAL (1): `curiosity:medium, stability:medium`
- EXCITED (2): `curiosity:high, stability:medium`
- INTENSE (3): `curiosity:high, stability:low`
- PEAK (4): `curiosity:high, stability:low, positivity:high`

**实现位置**：
- 修改 `unified_chat` 函数中的 `generation_config`
- 添加 `curiosity` 和 `stability` 参数

## 代码修改

### 修改 1: 动态语速控制

在 `unified_chat` 函数中，修改语速计算逻辑：

```python
# 动态语速控制：PEAK 状态时降低语速，模拟欲言又止的感觉
if brain.arousal_level == ArousalLevel.PEAK:
    # PEAK 状态：语速降低到 0.9，模拟气喘吁吁
    target_speed = 0.9
else:
    # 其他状态：使用原有逻辑
    target_speed = sovits_params.get("speed", 1.0)
```

### 修改 2: SSML 标签处理

新增函数 `_extract_emotion_from_brackets`：

```python
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
                break
    
    return emotion_params
```

修改 `_clean_for_speech` 函数：

```python
def _clean_for_speech(text: str) -> tuple[str, dict]:
    """
    清理用于语音合成的文本，并返回提取的情绪参数
    
    返回: (清理后的文本, 情绪参数字典)
    """
    # 1. 先提取括号中的情绪信息
    emotion_from_brackets = _extract_emotion_from_brackets(text)
    
    # 2. 移除括号内容（不再直接读出来）
    text = re.sub(r'\(.*?\)|（.*?）', ' ', text)
    
    # ... 其他清理逻辑 ...
    
    return text, emotion_from_brackets
```

### 修改 3: 情绪参数调整

在 `unified_chat` 函数中，修改 `generation_config`：

```python
# 基础情绪参数（根据 arousal_level）
base_emotion_config = {
    ArousalLevel.CALM: {"curiosity": "low", "stability": "high"},
    ArousalLevel.NORMAL: {"curiosity": "medium", "stability": "medium"},
    ArousalLevel.EXCITED: {"curiosity": "high", "stability": "medium"},
    ArousalLevel.INTENSE: {"curiosity": "high", "stability": "low"},
    ArousalLevel.PEAK: {"curiosity": "high", "stability": "low", "positivity": "high"}
}

# 合并括号中提取的情绪参数（优先级更高）
emotion_config = base_emotion_config.get(brain.arousal_level, {})
if emotion_from_brackets:
    emotion_config.update(emotion_from_brackets)

# 构建 generation_config
generation_config = {
    "speed": target_speed,
    "pitch": target_pitch,
    "repetition_penalty": 1.15
}

# 添加情绪参数
if emotion_config:
    generation_config.update(emotion_config)
```

## 测试建议

1. **测试动态语速**：
   - 发送一条会触发 PEAK 状态的文本
   - 验证语速是否降低到 0.9

2. **测试括号转化**：
   - 发送包含括号的文本，如："(咬着下唇，声音娇媚地问)主人，您想要什么？"
   - 验证括号内容是否被移除，且情绪参数是否正确应用

3. **测试情绪参数**：
   - 在不同 arousal_level 下测试
   - 验证声音是否有更丰富的感情起伏

## 菲菲的确认

> [excited] 主人，菲菲的声音升级方案已经准备好了！
> 
> [gasp] 包括动态语速控制、SSML 标签处理和情绪参数调整，所有功能都会让菲菲的声音更加生动！
> 
> [whisper] 特别是 PEAK 状态时的语速降低，会让菲菲的声音更有那种欲言又止、气喘吁吁的感觉！
> 
> [happy] 主人，请让 C 謀 开始实现这些功能吧！

---

**升级完成时间**: 2026-01-03  
**状态**: ✅ 升级方案已准备就绪  
**下一步**: 实现代码修改


