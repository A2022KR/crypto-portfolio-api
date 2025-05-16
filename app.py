
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

@app.route("/")
def home():
    return render_template("crypto_api_homepage.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        amount = request.form.get("amount")

        try:
            amount = float(amount)
        except ValueError:
            return "Invalid amount. Please enter a numeric value."

        coin_id = coin_map.get(symbol)
        if not coin_id:
            return render_template("error.html", message="Invalid cryptocurrency symbol selected.")

        import requests
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url).json()

        try:
            usd_price = response[coin_id]["usd"]
        except KeyError:
            return render_template("error.html", message="Price not found. Please try again later.")

        value = round(amount * usd_price, 2)
        return f"{amount} {symbol} = ${value} USD"
    return render_template("calculator_template.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
