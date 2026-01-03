# 解压 GPT-SoVITS 整合包指南

## 📦 整合包信息

- **文件路径**：`C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228.7z`
- **文件格式**：.7z（需要 7-Zip 解压）

## 🔧 解压方法

### 方法一：使用 7-Zip（推荐）

1. **安装 7-Zip**（如果未安装）
   - 下载：https://www.7-zip.org/download.html
   - 安装后重启终端

2. **解压文件**
   ```powershell
   # 使用 7-Zip 命令行解压
   7z x "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228.7z" -o"C:\Users\waiti\missfay\"
   ```
   
   或者：
   - 右键点击 `.7z` 文件
   - 选择 "7-Zip" → "提取到 GPT-SoVITS-v3lora-20250228\"
   - 或选择 "提取文件..." 指定解压位置

### 方法二：使用 WinRAR

如果已安装 WinRAR：
- 右键点击 `.7z` 文件
- 选择 "解压到 GPT-SoVITS-v3lora-20250228\"

### 方法三：使用其他解压工具

- **Bandizip**：https://www.bandisoft.com/bandizip/
- **PeaZip**：https://peazip.github.io/
- **Windows 11**：可能支持直接解压（右键 → 全部提取）

## 📁 解压后的目录结构

解压后应该会得到类似这样的目录：
```
GPT-SoVITS-v3lora-20250228/
├── runtime/          # Python 运行环境
├── GPT_SoVITS/      # 核心代码
├── tools/           # 工具脚本
├── go-webui.bat     # 启动脚本
├── go-webui.ps1     # PowerShell 启动脚本
└── ...
```

## 🚀 解压后的下一步

1. **进入解压后的目录**
   ```powershell
   cd "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228"
   ```

2. **启动 WebUI**
   - 双击 `go-webui.bat`
   - 或运行：`.\go-webui.ps1`

3. **浏览器会自动打开**
   - 通常是：http://127.0.0.1:9874
   - 如果没有自动打开，手动访问上述地址

4. **开始训练 FAY 音源**
   - 按照 `完整安装和训练指南.md` 中的步骤操作
   - 音频文件路径：`C:\Users\waiti\missfay\MISSFAY-2.mp3`

## ⚠️ 注意事项

- 解压需要足够的磁盘空间（约 5-10 GB）
- 解压后不要移动 `runtime` 目录
- 确保解压路径没有中文特殊字符（当前路径没问题）

## 🎯 快速开始

解压完成后，运行：
```powershell
cd "C:\Users\waiti\missfay\GPT-SoVITS-v3lora-20250228"
.\go-webui.bat
```

然后在 WebUI 中：
1. 切换到 "1-GPT-SoVITS-TTS/1A-数据集准备"
2. 填入音频路径：`C:\Users\waiti\missfay\MISSFAY-2.mp3`
3. 按照训练指南继续操作

