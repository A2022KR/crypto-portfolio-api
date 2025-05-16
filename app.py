from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Cryptocurrency mappings
coin_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "DOGE": "Dogecoin", 
    "BNB": "BNB"
}

# Homepage
@app.route("/")
def home():
    return render_template("crypto_api_homepage.html")

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Portfolio JSON
@app.route("/portfolio", methods=["GET"])
def get_portfolio():
    return jsonify({
        "BTC": 0.5,
        "ETH": 1.2,
        "USDT": 1000
    })

# Current Prices JSON
@app.route("/prices/current", methods=["GET"])
def get_prices():
    ids = ",".join(coin_map.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    return jsonify(response.json())

# Value of Portfolio
@app.route("/portfolio/value", methods=["GET"])
def get_portfolio_value():
    user_portfolio = {
        "BTC": 0.5,
        "ETH": 1.2,
        "USDT": 1000
    }

    ids = ",".join(coin_map.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    prices = requests.get(url).json()

    total_value = 0
    breakdown = {}

    for symbol, amount in user_portfolio.items():
        coin_id = coin_map[symbol]
        if coin_id in prices and "usd" in prices[coin_id]:
            price = prices[coin_id]["usd"]
            value = round(price * amount, 2)
            breakdown[symbol] = {
                "amount": amount,
                "usd_price": price,
                "value_usd": value
            }
            total_value += value

    return jsonify({
        "total_value_usd": round(total_value, 2),
        "breakdown": breakdown
    })

# Calculator Page
@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        crypto_symbol = request.form.get("crypto")
        amount = float(request.form.get("amount"))

        coin_id = coin_map.get(crypto_symbol)
        if not coin_id:
            return "Invalid cryptocurrency symbol selected.", 400

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url).json()

        usd_price = response[coin_id]["usd"]
        value = round(usd_price * amount, 2)

        return render_template("calculator_template.html", result=value, symbol=crypto_symbol, amount=amount)

    return render_template("calculator_template.html")

# 🟢 Final Line — Fix for Render.com: Listen on public IP and port 10000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
