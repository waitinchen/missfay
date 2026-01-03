import os
static_dir = os.path.join(os.path.dirname(os.path.abspath('voice_bridge.py')), 'static')
chat_path = os.path.join(static_dir, 'phi_chat.html')
print(f'Static dir: {static_dir}')
print(f'Chat path: {chat_path}')
print(f'Exists: {os.path.exists(chat_path)}')
