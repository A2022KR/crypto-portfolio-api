from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Cryptocurrency mappings
coin_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "XRP": "ripple",
    "BNB": "binancecoin",
    "SOL": "solana",
    "USDC": "usd-coin",
    "DOGE": "dogecoin",
    "ADA": "cardano",
    "TRX": "tron"
}

@app.route("/")
def home():
    return render_template("crypto_api_homepage.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        coin_id = request.form.get("symbol")
        amount = request.form.get("amount")

        try:
            amount_float = float(amount)
        except ValueError:
            return render_template("error.html", message="Invalid amount. Please enter a numeric value.")

        import requests
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url).json()

        try:
            usd_price = response[coin_id]["usd"]
        except KeyError:
            return render_template("error.html", message="Price not found. Please try again later.")

        value = round(amount_float * usd_price, 2)
        result = f"{amount} {coin_id.upper()} = ${value} USD"
        return render_template("calculator_template.html", result=result, selected=coin_id, amount=amount)

    return render_template("calculator_template.html", result=None, selected=None, amount=None)
