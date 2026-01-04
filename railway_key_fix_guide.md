# Railway GEMINI_API_KEY 修复指南

## 问题发现

### Key 比较结果

**本地 Key (正确):**
```
AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo
长度: 39 字符
状态: ✅ 已验证有效
```

**生产环境 Key (从图片中，可能有误):**
```
AIzaSyBh19-bR6xKe4DW2525LXU6dxYJSxUuOo
长度: 38 字符
状态: ❌ 长度不匹配，可能有输入错误
```

**差异分析:**
- 位置 8: 本地='l', 生产='1' (字母 l vs 数字 1)
- 位置 22-30: 多处字符差异
- 生产环境 Key 长度少 1 个字符

### 生产环境实际状态

从 `/verify-keys` 端点检查：
- Key 存在: ✅
- Key 长度: 39 (与本地匹配)
- Key 有效性: ❌ (libstdc++ 错误导致无法验证)

## 解决方案

### 步骤 1: 更新 Railway 环境变量

1. 访问 Railway Dashboard:
   ```
   https://railway.com/project/fa1d9d77-9344-464e-88c8-b0546d4376b7/service/26c887d6-0a28-4034-849b-08ec0ec0b286/variables
   ```

2. 找到 `GEMINI_API_KEY` 变量

3. 更新为正确的值:
   ```
   AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo
   ```
   
   **注意**: 
   - 确保没有多余的空格
   - 确保没有引号
   - 确保是完整的 39 个字符

4. 保存更改

### 步骤 2: 验证其他环境变量

同时确认以下变量已正确设置:

- `GEMINI_API_KEY` = `AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo`
- `GEMINI_MODEL` = `gemini-2.0-flash-exp`
- `CARTESIA_API_KEY` = (您的 Cartesia Key)
- `CARTESIA_VOICE_ID` = `a5a8b420-9360-4145-9c1e-db4ede8e4b15`

### 步骤 3: 重新部署

1. Railway Dashboard → Service → Deployments
2. 点击 "Redeploy" 或等待自动部署
3. 等待部署完成（约 2-5 分钟）

### 步骤 4: 验证修复

部署完成后，运行诊断脚本:
```bash
python check_railway_env.py
```

或访问:
- `https://missfay.tonetown.ai/health`
- `https://missfay.tonetown.ai/verify-keys`

预期结果:
- `brain_ready: true`
- `GEMINI_API_KEY.valid: true`
- `/chat` 端点正常工作

## 正确的 Key (已验证)

```
AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo
```

这个 Key 已经在本地测试中验证有效，可以正常调用 Gemini API。

