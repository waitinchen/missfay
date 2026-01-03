import torch
import sys

print(f"Python Version: {sys.version}")
print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA Version (torch): {torch.version.cuda}")
    print(f"Device Name: {torch.cuda.get_device_name(0)}")
    print(f"Capability: {torch.cuda.get_device_capability(0)}")
else:
    print("CUDA is NOT available.")
    # Check if NVIDIA driver exists
    import os
    try:
        nvidia_smi = os.popen('nvidia-smi').read()
        if 'NVIDIA-SMI' in nvidia_smi:
            print("NVIDIA-SMI detected, driver is likely installed.")
            print(nvidia_smi.split('\n')[0])
        else:
            print("NVIDIA-SMI not found.")
    except Exception as e:
        print(f"Error checking nvidia-smi: {e}")
