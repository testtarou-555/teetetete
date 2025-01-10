import os
import requests
from flask import Flask
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

app = Flask(__name__)

LINE_NOTIFY_ACCESS_TOKEN = os.getenv('LINE_NOTIFY_ACCESS_TOKEN')
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Tokyo')

def send_line_notify():
    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 3分ごとの通知です。"
    print(message, flush=True)  # Render のログに即時出力
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
        print("LINE Notify にメッセージを送信しました。", flush=True)
    except requests.exceptions.HTTPError as err:
        print(f"HTTPエラー: {err}", flush=True)
    except Exception as err:
        print(f"エラー: {err}", flush=True)

@app.route('/')
def home():
    return "このページはUptimeRobotによって定期的にアクセスされ、RenderのWebサービスをスリープさせないために存在します。"

def schedule_job():
    scheduler = BackgroundScheduler(timezone=TIMEZONE)
    scheduler.add_job(send_line_notify, 'interval', minutes=3)
    scheduler.start()
    print("スケジューラーが開始されました。（3分ごとの通知）", flush=True)

if __name__ == "__main__":
    schedule_job()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
