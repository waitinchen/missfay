import os
import sys

# ?瑕?摰?頝臬?
script_dir = os.path.dirname(os.path.abspath('voice_bridge.py'))
cwd = os.getcwd()
static_dir1 = os.path.join(script_dir, 'static')
static_dir2 = os.path.join(cwd, 'static')

print('Script directory:', script_dir)
print('Current working directory:', cwd)
print('Static dir (script):', static_dir1)
print('Static dir (cwd):', static_dir2)
print()
print('Script static exists:', os.path.exists(static_dir1))
print('CWD static exists:', os.path.exists(static_dir2))
print()

if os.path.exists(static_dir1):
    print('Files in script static:', os.listdir(static_dir1))
if os.path.exists(static_dir2):
    print('Files in cwd static:', os.listdir(static_dir2))
