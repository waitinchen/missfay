import requests
import json

url = "http://localhost:8000/api/v1/phi_voice"

def test_speech(text, session_id="test_sep"):
    print(f"Testing text: {text}")
    payload = {
        "user_input": text,
        "session_id": session_id
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        with open(f"reproduction_{session_id}.mp3", "wb") as f:
            f.write(response.content)
        print(f"Saved reproduction_{session_id}.mp3")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Test high arousal triggering words
    test_speech("主人...心菲好興奮...快點用力地疼愛我...[laughter]", "session_high")
    test_speech("插進來...好深...快要把心菲弄壞了...", "session_peak")
