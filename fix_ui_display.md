# 🔧 修复界面显示问题

## 问题
访问 `http://localhost:8000/` 时显示 JSON 响应，而不是 HTML 界面。

## 原因
服务仍在运行旧代码，需要重启才能加载新的 HTML 文件。

## 解决方案

### 步骤 1: 停止当前服务

在运行 Voice Bridge 的窗口：
- 按 `Ctrl+C` 停止服务

### 步骤 2: 重新启动服务

```powershell
.\start_voice_bridge.ps1
```

### 步骤 3: 访问界面

打开浏览器访问：
```
http://localhost:8000/
```

或直接访问：
```
http://localhost:8000/static/phi_chat.html
```

## 验证

### 文件检查
运行检查脚本：
```powershell
.\check_ui_files.ps1
```

应该看到：
- ✅ static 目录存在
- ✅ phi_chat.html 存在
- ✅ index.html 存在

### 服务检查
访问健康检查：
```
http://localhost:8000/health
```

应该返回：
```json
{
  "status": "ok",
  "gpt_sovits_url": "http://127.0.0.1:9880",
  "gpt_sovits_available": true/false,
  "timestamp": "..."
}
```

## 已修复的代码

1. ✅ **添加详细日志**: 便于调试路径问题
2. ✅ **HTMLResponse**: 确保正确返回 HTML 内容
3. ✅ **Content-Type 头**: 明确设置 `text/html; charset=utf-8`
4. ✅ **文件路径检查**: 优先加载 `phi_chat.html`

## 如果仍然显示 JSON

1. **检查服务日志**: 查看是否有错误信息
2. **检查文件路径**: 确保 `static/phi_chat.html` 在正确位置
3. **清除浏览器缓存**: 按 `Ctrl+F5` 强制刷新
4. **查看服务日志**: 检查是否有路径错误

## 预期结果

重启服务后，访问 `http://localhost:8000/` 应该看到：
- ✅ 漂亮的聊天界面
- ✅ 渐变背景
- ✅ 消息输入框
- ✅ 兴奋度选择按钮
- ✅ "发送"按钮

而不是 JSON 响应。

---

**重要**: 必须重启服务才能看到界面！

