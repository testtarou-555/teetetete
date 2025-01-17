import os
import requests
from flask import Flask
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

app = Flask(__name__)

# 環境変数からLINE Notifyのアクセストークンとタイムゾーンを取得
LINE_NOTIFY_ACCESS_TOKEN = os.getenv('LINE_NOTIFY_ACCESS_TOKEN')
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Tokyo')  # デフォルトは東京時間

def send_line_notify():
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_ACCESS_TOKEN}"
    }
    data = {
        "message": "昼の12:50分です。"
    }
    try:
        response = requests.post(url, headers=headers, data=data)
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
    # 通知を昼の12:50に設定
    scheduler.add_job(send_line_notify, 'cron', hour=12, minute=50)
    scheduler.start()
    print("スケジューラーが開始されました。")

if __name__ == "__main__":
    schedule_job()
    # Flaskアプリを起動
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
