from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Data masuk:", data)

    open_price = data['open']
    close = data['close']

    if close > open_price:
        print("BUY signal")
    else:
        print("SELL signal")

    return jsonify({"status": "ok"})