import yaml
import os

config_path = r"C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\GPT_SoVITS\configs\tts_infer.yaml"

if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 强制所有部分的 device 为 cpu
    if 'custom' in config:
        config['custom']['device'] = 'cpu'
        config['custom']['is_half'] = False
    
    if 'default' in config:
        config['default']['device'] = 'cpu'
        config['default']['is_half'] = False
        
    if 'default_v2' in config:
        config['default_v2']['device'] = 'cpu'
        config['default_v2']['is_half'] = False

    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)
    print("Forced CPU mode in config.")
else:
    print("Config file not found.")
