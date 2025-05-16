
from flask import Flask, jsonify
import requests

app = Flask(__name__)

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

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Cryptocurrency Portfolio API",
        "endpoints": ["/portfolio", "/portfolio/value", "/prices/current"]
    })

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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
