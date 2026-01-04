"""简单的 UI 路由测试"""
# 读取 HTML 文件内容
with open("static/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

print("HTML file read successfully")
print(f"Content length: {len(html_content)} characters")
print(f"First 100 chars: {html_content[:100]}")




