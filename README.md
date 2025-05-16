
# Cryptocurrency Portfolio API

A simple Flask API that simulates a user's crypto portfolio, fetches live prices from CoinGecko, and returns the total value in USD.

## Endpoints

- `/` – Welcome message and endpoint list
- `/portfolio` – Shows hardcoded crypto balances
- `/prices/current` – Fetches current market prices (USD)
- `/portfolio/value` – Calculates total value using live prices

## Deployment

This project includes a `render.yaml` to deploy easily on [Render.com](https://render.com).
