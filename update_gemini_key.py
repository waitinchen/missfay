"""
Update GEMINI_API_KEY in .env file
"""

import os
import re
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

env_file = ".env"
new_key = "AIzaSyBhl9-bR6xKe4DW25J25LXU6dxYJsxUuOo"

print("=" * 60)
print("Update GEMINI_API_KEY")
print("=" * 60)
print()

if os.path.exists(env_file):
    # Read existing content
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if GEMINI_API_KEY already exists
    if re.search(r'GEMINI_API_KEY\s*=', content):
        # Replace existing Key
        content = re.sub(r'GEMINI_API_KEY\s*=.*', f'GEMINI_API_KEY={new_key}', content)
        print("[OK] Updated existing GEMINI_API_KEY")
    else:
        # Add new Key
        content += f'\nGEMINI_API_KEY={new_key}\n'
        print("[OK] Added GEMINI_API_KEY")
    
    # Ensure GEMINI_MODEL exists
    if not re.search(r'GEMINI_MODEL\s*=', content):
        content += 'GEMINI_MODEL=gemini-2.0-flash-exp\n'
        print("[OK] Added GEMINI_MODEL")
    
    # Write file
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] .env file updated")
else:
    # Create new file
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(f'GEMINI_API_KEY={new_key}\n')
        f.write('GEMINI_MODEL=gemini-2.0-flash-exp\n')
    print("[OK] Created .env file")

print()
print(f"GEMINI_API_KEY set to: {new_key[:10]}...{new_key[-5:]}")
print()
print("You can now start the service:")
print("  .\\start_voice_bridge.ps1")
print()

