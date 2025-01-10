import os
import requests
from flask import Flask
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# 環境変数からWebhook URLとタイムゾーンを取得
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Tokyo')  # デフォルトは東京時間

def send_discord_message():
    data = {
        "content": "これは9:40に送信されたメッセージです。"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print(f"{datetime.now()} - メッセージを送信しました。")
    except requests.exceptions.HTTPError as err:
        print(f"HTTPエラー: {err}")
    except Exception as err:
        print(f"エラー: {err}")

@app.route('/')
def home():
    return "このページはUptimeRobotによって定期的にアクセスされ、RenderのWebサービスをスリープさせないために存在します。"

def schedule_job():
    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    scheduler.add_job(send_discord_message, 'cron', hour=9, minute=40)
    scheduler.start()
    print("スケジューラーが開始されました。")

if __name__ == "__main__":
    schedule_job()
    # Flaskアプリを起動
    app.run()
