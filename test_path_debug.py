import os
import sys

# 璅⊥? voice_bridge.py ?楝敺圾??current_file = 'voice_bridge.py'
static_dir = os.path.join(os.path.dirname(os.path.abspath(current_file)), 'static')
chat_path = os.path.join(static_dir, 'phi_chat.html')

print(f'Current file: {current_file}')
print(f'Static dir: {static_dir}')
print(f'Chat path: {chat_path}')
print(f'Static dir exists: {os.path.exists(static_dir)}')
print(f'Chat file exists: {os.path.exists(chat_path)}')

# 摰?頝臬?
actual_static = os.path.join(os.getcwd(), 'static')
actual_chat = os.path.join(actual_static, 'phi_chat.html')
print(f'')
print(f'Actual static dir: {actual_static}')
print(f'Actual chat path: {actual_chat}')
print(f'Actual static exists: {os.path.exists(actual_static)}')
print(f'Actual chat exists: {os.path.exists(actual_chat)}')
