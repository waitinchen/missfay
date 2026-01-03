# 配置 OpenRouter API Key 脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  配置 OpenRouter API Key" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$envContent = @"
# Phi 系统环境变量配置
# OpenRouter 无过滤架构配置

# ============================================
# OpenRouter API 配置
# ============================================

# OpenRouter API 密钥
OPENROUTER_API_KEY=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

# OpenAI API 密钥（备用，如果使用 OpenAI）
OPENAI_API_KEY=

# Anthropic Claude API 密钥（备用，如果使用 Claude）
ANTHROPIC_API_KEY=

# ============================================
# GPT-SoVITS 服务配置
# ============================================

# GPT-SoVITS 服务地址
GPT_SOVITS_URL=http://127.0.0.1:9880

# GPT-SoVITS API 版本 (v1 或 v2)
GPT_SOVITS_API_VERSION=v2

# 默认参考音频路径（可选）
DEFAULT_REF_AUDIO_PATH=

# 默认参考音频文本（可选）
DEFAULT_REF_AUDIO_TEXT=

# 默认参考音频语言（可选）
DEFAULT_REF_AUDIO_LANG=zh

# ============================================
# Voice Bridge 服务配置
# ============================================

# Voice Bridge 服务端口
VOICE_BRIDGE_PORT=8000

# Voice Bridge 服务地址
VOICE_BRIDGE_HOST=0.0.0.0

# ============================================
# OpenRouter 模型配置
# ============================================

# 默认模型（无过滤模型）
OPENROUTER_MODEL=meta-llama/llama-3-70b-instruct

# 备用模型（可选）
# OPENROUTER_MODEL=gryphe/mythomax-l2-13b

# OpenRouter 请求头配置
OPENROUTER_REFERER=https://github.com/Project-Phi
OPENROUTER_TITLE=Project Phi
"@

# 检查 .env 文件是否存在
if (Test-Path ".env") {
    Write-Host "⚠ .env 文件已存在" -ForegroundColor Yellow
    $overwrite = Read-Host "是否覆盖? (Y/N)"
    if ($overwrite -ne "Y" -and $overwrite -ne "y") {
        Write-Host "取消操作" -ForegroundColor Yellow
        exit 0
    }
}

# 写入 .env 文件
$envContent | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "✅ .env 文件已创建/更新" -ForegroundColor Green
Write-Host ""
Write-Host "配置内容：" -ForegroundColor Cyan
Write-Host "  - OpenRouter API Key: 已配置" -ForegroundColor White
Write-Host "  - 默认模型: meta-llama/llama-3-70b-instruct" -ForegroundColor White
Write-Host "  - 备用模型: gryphe/mythomax-l2-13b" -ForegroundColor White
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "  运行 python phi_test_uncensored.py 进行测试" -ForegroundColor White

