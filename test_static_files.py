"""测试静态文件路径"""
import os

# 获取当前脚本目录
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
index_path = os.path.join(static_dir, "index.html")

print("=" * 60)
print("Static File Path Test")
print("=" * 60)
print()
print(f"Current directory: {current_dir}")
print(f"Static directory: {static_dir}")
print(f"Index file path: {index_path}")
print()
print(f"Static dir exists: {os.path.exists(static_dir)}")
print(f"Index file exists: {os.path.exists(index_path)}")
print()

if os.path.exists(index_path):
    file_size = os.path.getsize(index_path)
    print(f"✅ File found! Size: {file_size} bytes")
    print()
    print("First 5 lines of file:")
    with open(index_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 5:
                print(f"  {i+1}: {line.strip()[:80]}")
else:
    print("❌ File not found!")
    print()
    print("Checking static directory contents:")
    if os.path.exists(static_dir):
        files = os.listdir(static_dir)
        print(f"  Files in static dir: {files}")
    else:
        print("  Static directory does not exist!")




