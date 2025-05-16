from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Sample user data
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
    return render_template("crypto_api_homepage.html")

@app.route("/portfolio", methods=["GET"])
def get_portfolio():
    return jsonify(user_portfolio)

@app.route("/prices/current", methods=["GET"])
def get_current_prices():
    ids = ",".join(coin_map.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    return jsonify(response.json())

@app.route("/portfolio/value", methods=["GET"])
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
        else:
            breakdown[symbol] = {
                "amount": amount,
                "usd_price": "N/A",
                "value_usd": "N/A"
            }

    return jsonify({
        "total_value_usd": round(total_value, 2),
        "breakdown": breakdown
    })

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = ""
    if request.method == "POST":
        try:
            symbol = request.form["symbol"]
            amount = float(request.form["amount"])

            coin_id = coin_map.get(symbol)
            if not coin_id:
                result = f"⚠️ Invalid cryptocurrency symbol: {symbol}"
            else:
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
                response = requests.get(url).json()
                print("🔍 CoinGecko response:", response)

                if coin_id in response and "usd" in response[coin_id]:
                    usd_price = response[coin_id]["usd"]
                    total_value = round(usd_price * amount, 2)
                    result = f"You own {amount} {symbol}<br>Current price: ${usd_price:.2f}<br>Total value: ${total_value:,.2f}"
                else:
                    result = f"❌ Price data not found for {symbol}."
        except Exception as e:
            result = f"⚠️ Error: {str(e)}"

    return render_template("calculator_template.html", result=result)

@app.route("/about")
def about():
    return render_template("about.html")
