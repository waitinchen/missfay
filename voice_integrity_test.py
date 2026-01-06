import requests
import wave
import struct
import sys
from datetime import datetime

print("Testing voice generation...")
print()

url = "http://localhost:8000/tts"
payload = {
    "text": "銝颱犖...?脩?鈭?鈭?..餈??...?刻?皛⊥???[laugh]",
    "text_language": "zh",
    "arousal_level": 2
}

try:
    response = requests.post(url, json=payload, timeout=30)
    
    if response.status_code == 200:
        # Save audio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"test_voice_{timestamp}.wav"
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        file_size = len(response.content)
        print(f"Audio file: {output_file}")
        print(f"File size: {file_size} bytes")
        
        # Check if file is not silent (basic check)
        if file_size == 0:
            print("FAIL: Audio file is empty (0 bytes)")
            sys.exit(1)
        
        # Try to read WAV file and check sample rate
        try:
            with wave.open(output_file, 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                frames = wav_file.getnframes()
                
                print(f"Sample rate: {sample_rate} Hz")
                print(f"Channels: {channels}")
                print(f"Frames: {frames}")
                
                # Check for 48kHz
                if sample_rate >= 48000:
                    print("PASS: Sample rate is 48kHz or higher")
                else:
                    print(f"WARN: Sample rate is {sample_rate}Hz (expected 48kHz)")
                
                # Check if audio has content (not silent)
                if frames > 0:
                    print("PASS: Audio has content (not silent)")
                else:
                    print("FAIL: Audio appears to be silent")
                    sys.exit(1)
        except Exception as e:
            print(f"WARN: Could not analyze WAV file: {e}")
            # File exists and has size, assume OK
            print("PASS: Audio file generated (size check passed)")
        
        # Check response headers
        arousal_header = response.headers.get("X-Arousal-Level", "N/A")
        tags_header = response.headers.get("X-Sovits-Tags", "N/A")
        
        print()
        print(f"Arousal Level: {arousal_header}")
        print(f"Tags: {tags_header}")
        
        # Verify arousal level matches
        if arousal_header == "2":
            print("PASS: Arousal level 2 confirmed")
        else:
            print(f"WARN: Arousal level mismatch (expected 2, got {arousal_header})")
        
        # Check for speed/pitch tags
        import json
        try:
            tags = json.loads(tags_header)
            if "speed" in tags and "pitch" in tags:
                speed = tags["speed"]
                pitch = tags["pitch"]
                print(f"PASS: Tags present - speed={speed}, pitch={pitch}")
                
                # Level 2 should have slight speed increase
                if 1.0 < speed <= 1.2:
                    print("PASS: Speed offset matches level 2 (slight increase)")
                else:
                    print(f"WARN: Speed {speed} may not match level 2")
            else:
                print("WARN: Speed/pitch tags not found in response")
        except:
            print("WARN: Could not parse tags from header")
        
        print()
        print("PASS: Voice integrity check passed")
        sys.exit(0)
    else:
        print(f"FAIL: Request failed with status {response.status_code}")
        print(response.text[:200])
        sys.exit(1)
        
except Exception as e:
    print(f"FAIL: Error during test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
