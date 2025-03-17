import requests
import pandas as pd
import logging
from model.data_treatment import load_config
from model.crypto_data import fetch_candlestick_data

def get_live_data(currency="usd"):
    """Fetches real-time cryptocurrency market data from CoinGecko."""
    config = load_config()
    base_url = config["base_url"]
    url = f"{base_url}coins/markets?vs_currency={currency}&order=market_cap_desc&per_page=10&page=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        live_data = pd.DataFrame(response.json())

        # Fetch market dominance
        dominance_data = get_market_dominance()

        if dominance_data:
            # Convert dominance keys to lowercase to match `symbol` column
            dominance_data = {key.lower(): value for key, value in dominance_data.items()}

            # Check if `symbol` column exists
            if "symbol" in live_data.columns:
                # Map dominance data based on symbol instead of ID
                live_data["market_cap_percentage"] = live_data["symbol"].map(dominance_data)

        return live_data
    except requests.RequestException as e:
        logging.error(f"Error fetching live cryptocurrency data: {e}")
        return None

def get_market_dominance():
    """Fetches cryptocurrency market dominance from CoinGecko."""
    url = "https://api.coingecko.com/api/v3/global"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "market_cap_percentage" in data["data"]:
            dominance = data["data"]["market_cap_percentage"]
            logging.info(f"Retrieved market dominance data: {dominance}")
            return dominance  # Dictionary {symbol: dominance_percentage}

        logging.warning("Market dominance data missing in API response.")
        return None
    except requests.RequestException as e:
        logging.error(f"Error fetching market dominance: {e}")
        return None
    
def get_historical_data(coin, currency, days):
    """Fetch OHLC (candlestick) cryptocurrency data."""
    return fetch_candlestick_data(coin_id=coin, currency=currency, days=days)