# Full Flask app with homepage, portfolio API, CoinGecko price fetch, and interactive calculator

from pathlib import Path

enhanced_flask_app = '''
from flask import Flask, jsonify, request, render_template_string
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    with open("crypto_api_homepage.html", "r") as f:
        html = f.read()
    return render_template_string(html)

user_portfolio = {
    "BTC": 0.5,
    "ETH": 1.2,
    "USDT": 1000
}

coin_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether"
}

@app.route("/portfolio")
def get_portfolio():
    return jsonify(user_portfolio)

@app.route("/prices/current")
def get_current_prices():
    ids = ",".join(coin_map.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    return jsonify(response.json())

@app.route("/portfolio/value")
def get_portfolio_value():
    ids = ",".join(coin_map.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    prices = requests.get(url).json()

    total_value = 0
    breakdown = {}

    for symbol, amount in user_portfolio.items():
        coin_id = coin_map[symbol]
        if coin_id in prices and "usd" in prices[coin_id]:
            usd_price = prices[coin_id]["usd"]
            value = round(amount * usd_price, 2)
            breakdown[symbol] = {
                "amount": amount,
                "usd_price": usd_price,
                "value_usd": value
            }
            total_value += value

    return jsonify({
        "total_value_usd": round(total_value, 2),
        "breakdown": breakdown
    })

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = ""
    if request.method == "POST":
        symbol = request.form.get("symbol", "").upper()
        amount = float(request.form.get("amount", "0"))
        coin_id = coin_map.get(symbol)
        if coin_id:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
            response = requests.get(url).json()
            usd_price = response[coin_id]["usd"]
            total_value = round(usd_price * amount, 2)
            result = f"You own {amount} {symbol}<br>Current price: ${usd_price:.2f}<br>Total value: ${total_value:,.2f}"
        else:
            result = f"Unknown symbol: {symbol}"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crypto Value Calculator</title>
        <style>
            body {{ font-family: Arial; background: #0b0c10; color: #fff; padding: 40px; }}
            input, button {{ padding: 10px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>Cryptocurrency Value Calculator</h1>
        <form method="POST">
            <label>Cryptocurrency Symbol (e.g. BTC):</label><br>
            <input name="symbol" required><br>
            <label>Amount you own:</label><br>
            <input name="amount" type="number" step="any" required><br>
            <button type="submit">Calculate</button>
        </form>
        <div style="margin-top: 30px;">
            <strong>{result}</strong>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
'''

# Save updated app.py
new_app_path = Path("/mnt/data/app.py")
new_app_path.write_text(enhanced_flask_app)

new_app_path.name
