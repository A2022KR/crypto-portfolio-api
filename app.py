
from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

user_portfolio = {
    "BTC": 0.5,
    "ETH": 1.2,
    "USDT": 1000
}

coin_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "DOGE": "dogecoin",
    "BNB": "binancecoin"
}

@app.route("/")
def home():
    return render_template("crypto_api_homepage.html")

@app.route("/portfolio")
def get_portfolio():
    return jsonify(user_portfolio)

@app.route("/prices/current")
def get_current_prices():
    ids = ",".join(coin_map.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    prices = response.json()
    return jsonify({"prices_usd": {k: prices.get(coin_map[k], {}).get("usd", 0) for k in user_portfolio}})

@app.route("/portfolio/value")
def get_portfolio_value():
    ids = ",".join(coin_map.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    prices = requests.get(url).json()
    total = 0
    for symbol, amount in user_portfolio.items():
        coin_id = coin_map.get(symbol)
        if coin_id and coin_id in prices:
            total += prices[coin_id]["usd"] * amount
    return jsonify({"total_portfolio_value_usd": round(total, 2)})

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = ""
    if request.method == "POST":
        symbol = request.form.get("symbol", "").upper()
        amount_input = request.form.get("amount", "")
        try:
            amount = float(amount_input)
            coin_id = coin_map.get(symbol)
            if coin_id:
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
                response = requests.get(url).json()
                usd_price = response[coin_id]["usd"]
                total_value = round(usd_price * amount, 2)
                result = f"You own {amount} {symbol}<br>Current price: ${usd_price:.2f}<br>Total value: ${total_value:,.2f}"
            else:
                result = f"❌ Unknown symbol: {symbol}"
        except ValueError:
            result = "❌ Please enter a valid number for amount."
    return render_template("calculator_template.html", result=result)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
