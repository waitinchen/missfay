import sys
sys.path.insert(0, '.')
from phi_brain import PhiBrain, ArousalLevel

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
