import sys
import os
sys.path.insert(0, '.')

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from phi_brain import PhiBrain, ArousalLevel

# Set API key if not in env
if not os.getenv("OPENROUTER_API_KEY"):
    os.environ["OPENROUTER_API_KEY"] = "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"

phi = PhiBrain(api_type="openrouter")
phi.set_arousal_level(ArousalLevel.EXCITED)  # Level 2

test_text = "瘚??"
tagged = phi._generate_sovits_tags(test_text)

print(f"Original: {test_text}")
print(f"Tagged: {tagged}")

# Check for tags
has_speed = "[speed=" in tagged
has_pitch = "[pitch=" in tagged

if has_speed and has_pitch:
    print("PASS: Both speed and pitch tags present")
    sys.exit(0)
else:
    print(f"FAIL: speed={has_speed}, pitch={has_pitch}")
    sys.exit(1)
