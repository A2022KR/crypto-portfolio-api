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
    result = None
    error_message = None
    if request.method == "POST":
        symbol = request.form.get("symbol")
        amount = request.form.get("amount")

        try:
            amount = float(amount)
        except ValueError:
            error_message = "Invalid amount. Please enter a number."
            return render_template("calculator_template.html", coins=coin_map, error=error_message)

        coin_id = coin_map.get(symbol)
        if not coin_id:
            error_message = "Invalid cryptocurrency symbol selected."
            return render_template("calculator_template.html", coins=coin_map, error=error_message)

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url).json()

        try:
            usd_price = response[coin_id]["usd"]
        except KeyError:
            return render_template("error.html", message="Price not found. Please try again later.")

        result = f"{amount} {symbol} = ${round(amount * usd_price, 2)} USD"

    return render_template("calculator_template.html", coins=coin_map, result=result)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found."), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
