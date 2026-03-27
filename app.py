import requests
import time
from datetime import datetime
import pytz

# ===== CONFIG =====
SYMBOL = "EURUSD"
API_KEY = "demo"  # nanti bisa diganti

# ===== CEK SESSION =====
def is_ny_session():
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    ny_time = now_utc.astimezone(pytz.timezone("America/New_York"))
    return 6 <= ny_time.hour < 12

# ===== AMBIL DATA =====
def get_price():
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey={API_KEY}"
    res = requests.get(url)
    data = res.json()

    try:
        latest = list(data["Time Series FX (5min)"].values())[0]
        return {
            "open": float(latest["1. open"]),
            "high": float(latest["2. high"]),
            "low": float(latest["3. low"]),
            "close": float(latest["4. close"])
        }
    except:
        print("Gagal ambil data")
        return None

# ===== LOGIC =====
def strategy(candle):
    if candle["close"] > candle["open"]:
        print("BUY SIGNAL")
    else:
        print("SELL SIGNAL")

# ===== MAIN LOOP =====
while True:
    if is_ny_session():
        print("Session NY aktif")

        candle = get_price()
        if candle:
            print(candle)
            strategy(candle)

    else:
        print("Di luar session, tidur...")

    time.sleep(300)  # tiap 5 menit