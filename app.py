from flask import Flask
import threading
import time
from datetime import datetime
import pytz

app = Flask(__name__)

# =========================
# CONFIG
# =========================
START_HOUR = 6
END_HOUR = 12

# timezone New York
ny_tz = pytz.timezone("America/New_York")


# =========================
# CEK WAKTU TRADING
# =========================
def is_trading_time():
    now = datetime.now(ny_tz)
    hour = now.hour
    return START_HOUR <= hour < END_HOUR


# =========================
# LOGIC TRADING (EDIT DISINI)
# =========================
def trading_logic():
    print("🔍 Checking market...")

    # contoh dummy logic
    # nanti bisa diganti ambil data API / strategi kamu
    import random
    signal = random.choice(["BUY", "SELL", "NONE"])

    if signal == "BUY":
        print("🟢 BUY SIGNAL")
    elif signal == "SELL":
        print("🔴 SELL SIGNAL")
    else:
        print("⚪ NO TRADE")


# =========================
# LOOP BOT
# =========================
def bot_loop():
    while True:
        try:
            if is_trading_time():
                print("⏰ Trading session ON")
                trading_logic()
            else:
                print("💤 Outside trading hours")

            time.sleep(60)  # cek tiap 1 menit

        except Exception as e:
            print("❌ ERROR:", e)
            time.sleep(10)


# =========================
# WEB SERVER (BIAR REPLIT GA SLEEP)
# =========================
@app.route('/')
def home():
    return "Bot is running!"


def run_flask():
    app.run(host="0.0.0.0", port=8080)


# =========================
# RUN THREAD
# =========================
threading.Thread(target=bot_loop).start()
threading.Thread(target=run_flask).start()
