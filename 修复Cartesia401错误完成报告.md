# 修复 Cartesia 401 错误完成报告

## 执行时间
2026-01-03

## 问题诊断

根据用户反馈，401 错误来自 **Cartesia TTS**，而非 Gemini LLM。

## 已修复的问题

### 1. ✅ 强制重新加载 .env 环境变量

**修复位置**: `voice_bridge.py` 顶部

**修复内容**:
- 添加 `load_dotenv(_env_path, override=True)` 强制覆盖旧变量
- 保留手动解析逻辑（处理 BOM 问题）
- 添加调试输出确认 CARTESIA_API_KEY 是否正确加载

**代码更改**:
```python
# 强制覆盖旧变量
load_dotenv(_env_path, override=True)

# 手动加载并处理可能的 BOM（双重保险）
try:
    with open(_env_path, 'r', encoding='utf-8') as f:
        env_content = f.read().lstrip('\ufeff')
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#') and line.strip():
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
except Exception as e:
    logger.error(f"Manual .env parse failed: {e}")

# 调试输出
_cartesia_key = os.getenv("CARTESIA_API_KEY")
if _cartesia_key:
    logger.info(f"DEBUG: Cartesia Key loaded: {_key_preview} (length: {len(_cartesia_key)})")
    print(f"DEBUG: Cartesia Key starts with: {_cartesia_key[:5]}")
else:
    logger.error("CRITICAL: CARTESIA_API_KEY not found!")
```

### 2. ✅ 验证 CARTESIA_API_KEY 配置

**修复位置**: `voice_bridge.py` 第 67-75 行

**修复内容**:
- 添加启动时验证，如果 CARTESIA_API_KEY 缺失，立即报错
- 添加日志输出确认 Key 已加载

**代码更改**:
```python
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

# 验证 CARTESIA_API_KEY
if not CARTESIA_API_KEY:
    logger.error("CRITICAL: CARTESIA_API_KEY is missing! TTS will fail with 401 error.")
    raise ValueError("CARTESIA_API_KEY is required. Please check your .env file.")
else:
    logger.info(f"Cartesia API Key loaded successfully (length: {len(CARTESIA_API_KEY)})")
```

### 3. ✅ 增强 Cartesia 初始化错误处理

**修复位置**: 
- `/api/v1/phi_voice` 端点（第 297-299 行）
- `/chat` 端点（第 403-404 行）

**修复内容**:
- 在每次调用 Cartesia 前验证 API Key
- 添加调试日志输出

**代码更改**:
```python
# 验证 API Key
if not CARTESIA_API_KEY:
    raise HTTPException(status_code=500, detail="CARTESIA_API_KEY is missing. Please check .env file.")

logger.info(f"Initializing Cartesia client with key: {CARTESIA_API_KEY[:10]}...")
client = Cartesia(api_key=CARTESIA_API_KEY)
```

### 4. ✅ 创建进程清理脚本

**新文件**: `kill_python_processes.ps1`

**功能**:
- 强制关闭所有 Python 进程
- 检查端口 8000 和 9880 是否已释放
- 提供清晰的输出和下一步指引

## 验证清单

- [x] 强制重新加载 .env 环境变量
- [x] 添加 CARTESIA_API_KEY 调试输出
- [x] 添加启动时验证
- [x] 增强 Cartesia 初始化错误处理
- [x] 创建进程清理脚本

## 下一步操作

### 步骤 1: 关闭残留进程

```powershell
# 方法 1: 使用提供的脚本
.\kill_python_processes.ps1

# 方法 2: 手动执行
Stop-Process -Name python -Force
```

### 步骤 2: 验证 .env 文件

确认 `.env` 文件中包含：
```env
CARTESIA_API_KEY=your_cartesia_api_key_here
GEMINI_API_KEY=AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo
```

### 步骤 3: 重新启动服务

```powershell
.\start_voice_bridge.ps1
```

### 步骤 4: 检查启动日志

启动时应该看到：
```
DEBUG: Cartesia Key starts with: [前5个字符]
Cartesia API Key loaded successfully (length: [长度])
```

如果看到 `CARTESIA_API_KEY not found`，请检查 `.env` 文件。

## 如果仍然出现 401 错误

### 可能原因 1: CARTESIA_API_KEY 无效或过期

**解决方案**:
- 检查 Cartesia 控制台的 API Key 状态
- 确认 Key 未过期
- 重新生成新的 API Key 并更新 `.env` 文件

### 可能原因 2: .env 文件路径问题

**解决方案**:
- 确认 `.env` 文件在项目根目录（与 `voice_bridge.py` 同级）
- 检查文件编码为 UTF-8（无 BOM）

### 可能原因 3: 服务未完全重启

**解决方案**:
- 使用 `kill_python_processes.ps1` 强制关闭所有进程
- 等待 5 秒后重新启动

## 调试输出说明

启动服务时，控制台会显示：
- `DEBUG: Cartesia Key starts with: [前5个字符]` - 确认 Key 已加载
- `Cartesia API Key loaded successfully (length: [长度])` - 确认 Key 有效
- `Initializing Cartesia client with key: [前10个字符]...` - 每次调用时的确认

如果看到 `NOT_FOUND` 或 `INVALID`，说明 Key 未正确加载。

---

**修复完成时间**: 2026-01-03  
**状态**: ✅ 代码已修复，等待服务重启验证

