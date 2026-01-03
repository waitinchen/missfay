import os
import struct

def get_wav_duration(file_path):
    try:
        with open(file_path, 'rb') as f:
            riff = f.read(4)
            if riff != b'RIFF': return None
            f.seek(22)
            channels = struct.unpack('<H', f.read(2))[0]
            sample_rate = struct.unpack('<I', f.read(4))[0]
            f.seek(34)
            bits_per_sample = struct.unpack('<H', f.read(2))[0]
            f.seek(40)
            data_size = struct.unpack('<I', f.read(4))[0]
            duration = data_size / (sample_rate * channels * (bits_per_sample / 8))
            return duration
    except:
        return None

search_dir = r"C:\Users\waiti\missfay"
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.lower().endswith('.wav'):
            path = os.path.join(root, file)
            duration = get_wav_duration(path)
            if duration and 3 <= duration <= 10:
                print(f"FOUND: {path} ({duration:.2f}s)")
