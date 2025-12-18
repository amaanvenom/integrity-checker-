import requests
import os
from config.config import BOT_TOKEN, CHAT_ID

def send_telegram_alert(file_path, action):
    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_path)[1] or "Unknown"
    message = (
        "📁 <b>File Integrity Alert</b>\n\n"
        f"🔹 <b>Name:</b> {file_name}\n"
        f"🔹 <b>Type:</b> {file_type}\n"
        f"📍 <b>Location:</b> {file_path}\n"
        f"⚠️ <b>Action:</b> {action}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"[ERROR] Telegram failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Telegram exception: {e}")
