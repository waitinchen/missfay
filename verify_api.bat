@echo off
chcp 65001 >nul
echo ========================================
echo 验证 OpenRouter API Key
echo ========================================
echo.

set PYTHON_PATH=.\GPT-SoVITS-v3lora-20250228\GPT-SoVITS-v3lora-20250228\runtime\python.exe

if not exist "%PYTHON_PATH%" (
    echo 错误: 未找到 Python
    echo 请确保整合包已解压
    pause
    exit /b 1
)

echo 找到 Python: %PYTHON_PATH%
echo.

echo 安装依赖...
"%PYTHON_PATH%" -m pip install requests python-dotenv -q
echo.

echo 运行验证脚本...
"%PYTHON_PATH%" verify_api.py

pause




