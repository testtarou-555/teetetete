import os
import requests
from flask import Flask
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

app = Flask(__name__)

# 環境変数からLINE Notifyのアクセストークンとタイムゾーンを取得
LINE_NOTIFY_ACCESS_TOKEN = 'TVb5EFJlsvu12xS78vkLwYbqCPjYrCYhtLKeQGwfAWt'
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Tokyo')  # デフォルトは東京時間

def send_line_notify():
    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 3分ごとの通知です。"
    print(message)  # コンソールにプリント
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_ACCESS_TOKEN}"
    }
    data = {
        "message": message
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        print("LINE Notify にメッセージを送信しました。")
    except requests.exceptions.HTTPError as err:
        print(f"HTTPエラー: {err}")
    except Exception as err:
        print(f"エラー: {err}")

@app.route('/')
def home():
    return "このページはUptimeRobotによって定期的にアクセスされ、RenderのWebサービスをスリープさせないため
