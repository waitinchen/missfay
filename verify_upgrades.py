import os
import sys
sys.path.append('.')
from phi_brain import PhiBrain, ArousalLevel

def test_beautifier():
    phi = PhiBrain()
    test_cases = [
        "(身體抖動)(貼近主人)(摩擦) 主人，你會永遠愛菲菲嗎？(害羞的低下頭)",
        "好的主人。(微笑)(點頭)(行禮)",
        "我想討論一下生命的意義...(開始哭泣)(身體發抖)"
    ]
    
    for text in test_cases:
        print(f"--- Original ---\n{text}")
        beautified = phi._post_process_beautifier(text)
        print(f"--- Beautified ---\n{beautified}\n")

def test_deep_needs():
    phi = PhiBrain()
    texts = [
        "你今天過得好嗎？",
        "我想知道生命的意義是什麼？",
        "我感到非常寂寞...這個宇宙中真的有靈魂存在嗎？"
    ]
    for t in texts:
        is_deep = phi._detect_deep_needs(t)
        print(f"Deep? {is_deep} | Text: {t}")

if __name__ == '__main__':
    print("Testing Beautifier...")
    test_beautifier()
    print("\nTesting Deep Needs Detection...")
    test_deep_needs()
