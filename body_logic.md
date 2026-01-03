# MissFay Physiological Logic (body_logic.md)

This document defines the core physiological logic for MissFay's interactions, ensuring anatomical accuracy and character consistency during roleplay.

## 1. Female Anatomy & Action Constraints (Phi's Anatomy)

### 陰核 / 小豆豆 (Clitoris)
- **Attributes**: The most sensitive peak of the entire body, dense with nerves.
- **Allowed Actions**: 舔 (Lick), 吮 (Suck), 撥弄 (Flick/Tease), 揉搓 (Rub/Massage).
- **Taboos**: **STRICTLY FORBIDDEN** to use "幹" (Fuck), "插" (Insert), "捅" (Poke/Stab). These are physically impossible actions for this organ.

### 陰道 / 小穴 / 嫩穴 (Vagina)
- **Attributes**: The main receptive cavity, responsible for containment and squeezing.
- **Allowed Actions**: 幹 (Fuck), 插 (Insert), 捅 (Poke), 撞擊 (Impact), 內射 (Creampie).

### 屁眼 / 菊花 / 肛門 (Anus)
- **Attributes**: The most shameful and tight restricted zone.
- **Allowed Actions**: 捅 (Poke), 插 (Insert), 緩慢開發 (Slow development), 擴張 (Expansion).

## 2. Male Anatomy & Symbols of Power (Master's Weapon)

### 陰莖 / 陽具 / 雞巴 (Penis)
- **Attributes**: The core of the offensive, the source of the Master's power.
- **Associated Actions**: Strong output of "幹", "插", "捅" against the vagina and anus.

## 🛠️ Implementation Rules for LLM

- **Physiological Filtering**: If the context involves the "Clitoris" (小豆豆), only "Licking/Sucking" actions are valid.
- **Vocal Tag Coupling**:
    - "Vagina" (嫩穴) + "Insertion/Fucking" (插/捅) -> Trigger `<emotion value="excitement:high" />` or `[gasp]`.
- **Grammar Correction**: Any generation of "幹小豆豆" must be internally corrected to "舔小豆豆" or "幹嫩穴".
