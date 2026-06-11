import requests
import os

class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TG_BOT_TOKEN")
        self.chat_id = os.getenv("TG_CHAT_ID")

    def send(self, msg):
        if not self.token or not self.chat_id:
            print("⚠️ Telegram未配置")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:
            requests.post(url, json={
                "chat_id": self.chat_id,
                "text": msg
            }, timeout=5)
        except Exception as e:
            print("Telegram error:", e)
