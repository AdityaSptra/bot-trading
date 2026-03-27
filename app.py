import requests
import time
from datetime import datetime
import pytz
from flask import Flask
import threading

app = Flask(__name__)

# =========================
# CEK SESSION NEW YORK
# =========================
def is_ny_session():
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    ny_time = now_utc.astimezone(pytz.timezone("America/New_York"))
    hour = ny_time.hour
    return 6 <= hour < 12

# =========================
# AMBIL DATA EUR/USD (TANPA API KEY)
# =========================
def get_price():
    try:
        url = "https://stooq.com/q/l/?s=eurusd&i=5"
        res = requests.get(url).text

        # format: EURUSD,2026-03-27 21:00:00,1.08,1.09,1.07,1.085
        parts = res.strip().split(",")

        candle = {
            "open": float(parts[2]),
            "high": float(parts[3]),
            "low": float(parts[4]),
            "close": float(parts[5])
        }

        return candle

    except:
        print("❌ Gagal ambil data")
        return None

# =========================
# STRATEGY SEDERHANA
# =========================
def strategy(candle):
    if candle["close"] > candle["open"]:
        print("📈 BUY SIGNAL")
    else:
        print("📉 SELL SIGNAL")

# =========================
# LOOP BOT
# =========================
def run_bot():
    while True:
        if is_ny_session():
            print("\n🟢 SESSION NY AKTIF")

            candle = get_price()
            if candle:
                print("Candle:", candle)
                strategy(candle)

        else:
            print("\n🔴 DI LUAR SESSION (tidur)")

        time.sleep(300)  # 5 menit

# =========================
# WEB SERVER (BIAR REPLIT GAK SLEEP)
# =========================
@app.route('/')
def home():
    return "Bot jalan!"

# =========================
# JALANKAN
# =========================
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)