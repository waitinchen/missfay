# CPU-Only Deployment Walkthrough (ASUS Zenbook 14)

The system has been refactored to run exclusively on the CPU to avoid CUDA-related crashes on this hardware.

## Key Changes Made

### 1. Hardware Fallback (CPU Mode)
- **GPT-SoVITS**: Forced `device: cpu` in `tts_infer.yaml`.
- **Torch Compatibility**: Patched `TTS.py` to use `map_location=torch.device('cpu')` for all model loading.
- **Voice Bridge**: Configured to use the integrated Python runtime which is pre-optimized for CPU inference.

### 2. Persona Hardening (Anti-Filter)
- **MissFay Identity**: Updated `phi_brain.py` with a new `SYSTEM_PROMPT` that strictly enforces the "MissFay" persona.
- **Forbidden Terms**: Explicitly blocked the model from identifying as an AI or Large Language Model.
- **OpenRouter Default**: Locked the generation engine to OpenRouter's uncensored models.

### 3. Environment Stability
- **English Renaming**: All startup and utility scripts have been renamed to English to prevent PowerShell encoding errors.
- **Unified Startup**: Provided a consolidated `launch_all.ps1` script that launches services in the correct sequence.

## How to Start
1. Run `launch_all.ps1` available in the root directory.
2. Wait for the two new PowerShell windows to show "Uvicorn running".
3. Access the UI at `http://localhost:8000/static/index.html`.
