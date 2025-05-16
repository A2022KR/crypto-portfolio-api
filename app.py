from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Cryptocurrency mappings (display only, not used for API anymore)
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
    result = None
    selected = None
    amount = None

    if request.method == "POST":
        coin_id = request.form.get("symbol")
        amount = request.form.get("amount")
        selected = coin_id

        try:
            amount_float = float(amount)
        except ValueError:
            return render_template("error.html", message="Invalid amount. Please enter a numeric value.")

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url).json()

        try:
            usd_price = response[coin_id]["usd"]
        except KeyError:
            return render_template("error.html", message="Price not found. Please try again later.")

        value = round(amount_float * usd_price, 2)
        result = f"{amount} {coin_id.upper()} = ${value} USD"

    return render_template("calculator_template.html", result=result, selected=selected, amount=amount)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found."), 404

# ✅ Required for Render.com deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use PORT from Render if available
    app.run(host="0.0.0.0", port=port)
