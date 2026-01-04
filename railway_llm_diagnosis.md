# Railway 生产环境 LLM 初始化问题诊断指南

## 问题描述
生产环境（Railway）出现错误：`500 - 大脑 (LLM) 未就绪，请检查 API Key`，但本地 LLM 正常工作。

## 可能原因

### 1. Railway 环境变量未正确设置
- **检查项**: 确认 Railway 后台已设置 `GEMINI_API_KEY`
- **验证方法**: 访问 Railway 环境变量页面，确认变量存在且值正确

### 2. 环境变量名称错误
- **检查项**: 确保变量名完全匹配 `GEMINI_API_KEY`（区分大小写）
- **常见错误**: `GEMINI_API_KEY` vs `Gemini_Api_Key` vs `gemini_api_key`

### 3. 环境变量值格式问题
- **检查项**: 确保 API Key 值没有多余的空格、引号或换行符
- **验证方法**: 复制完整的 Key 值，确保前后没有空格

### 4. Railway 部署后环境变量未生效
- **解决方法**: 重新部署服务（Redeploy）
- **步骤**: Railway Dashboard → Service → Deployments → Redeploy

## 诊断步骤

### 步骤 1: 检查 Railway 环境变量
1. 访问 Railway Dashboard
2. 进入 Service → Variables
3. 确认以下变量存在：
   - `GEMINI_API_KEY` = `AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo`
   - `CARTESIA_API_KEY` = (您的 Cartesia Key)
   - `CARTESIA_VOICE_ID` = `a5a8b420-9360-4145-9c1e-db4ede8e4b15`
   - `GEMINI_MODEL` = `gemini-2.0-flash-exp`

### 步骤 2: 检查服务日志
1. 访问 Railway Dashboard → Service → Logs
2. 查找以下关键日志：
   - `=== Environment Variables Check ===`
   - `GEMINI_API_KEY exists: True/False`
   - `Failed to initialize PhiBrain`
3. 如果看到 `GEMINI_API_KEY is None or empty!`，说明环境变量未正确加载

### 步骤 3: 使用诊断端点
访问生产环境的健康检查端点：
```
https://missfay.tonetown.ai/health
```

查看返回的 `diagnostics` 字段：
- `gemini_key_exists`: 是否找到 GEMINI_API_KEY
- `gemini_key_length`: Key 的长度（应该是 39）
- `init_error`: 初始化错误详情（如果有）

### 步骤 4: 使用验证端点
访问验证端点：
```
https://missfay.tonetown.ai/verify-keys
```

检查 `GEMINI_API_KEY` 的状态：
- `exists`: 是否存在于环境变量中
- `valid`: 是否有效（可以成功调用 API）

## 解决方案

### 方案 1: 重新设置环境变量
1. 在 Railway Dashboard 中删除 `GEMINI_API_KEY`
2. 重新添加 `GEMINI_API_KEY`，值为：`AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo`
3. 保存后触发重新部署

### 方案 2: 强制重新部署
1. Railway Dashboard → Service → Settings
2. 点击 "Redeploy" 或 "Deploy Latest"
3. 等待部署完成
4. 检查日志确认环境变量已加载

### 方案 3: 检查代码版本
确保最新代码已部署：
1. 检查 GitHub 仓库是否有最新提交
2. Railway 应该自动检测到新提交并部署
3. 如果没有，手动触发部署

## 验证修复

部署完成后，访问：
1. `/health` 端点：确认 `brain_ready: true`
2. `/verify-keys` 端点：确认 `GEMINI_API_KEY` 的 `valid: true`
3. 聊天界面：发送测试消息，确认不再出现 500 错误

## 常见错误信息

### "GEMINI_API_KEY is None or empty!"
- **原因**: 环境变量未设置或未正确加载
- **解决**: 检查 Railway 环境变量设置

### "Failed to initialize PhiBrain"
- **原因**: API Key 无效或网络问题
- **解决**: 验证 API Key 有效性，检查网络连接

### "google-generativeai 未安装"
- **原因**: 依赖包未安装
- **解决**: 检查 `requirements_phi.txt` 是否包含 `google-generativeai>=0.3.0`

## 联系支持

如果以上步骤都无法解决问题，请提供：
1. Railway 日志（最近的错误日志）
2. `/health` 端点的完整响应
3. `/verify-keys` 端点的完整响应

