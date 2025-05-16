from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Cryptocurrency mappings
coin_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "DOGE": "dogecoin",
    "BNB": "binancecoin"
}

# Homepage
@app.route("/")
def home():
    return render_template("crypto_api_homepage.html")

# About page
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

# Calculator page
@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        amount = request.form.get("amount")

        if symbol not in coin_map:
            return render_template("error.html", message="Invalid cryptocurrency symbol selected.")

        try:
            amount = float(amount)
        except ValueError:
            return render_template("error.html", message="Amount must be a number.")

        coin_id = coin_map[symbol]
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url).json()

        usd_price = response.get(coin_id, {}).get("usd")
        if usd_price is None:
            return render_template("error.html", message="Failed to retrieve price data.")

        total = round(amount * usd_price, 2)
        return render_template("calculator_template.html", result=total, symbol=symbol)

    return render_template("calculator_template.html")
