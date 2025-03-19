import requests
import pandas as pd
import logging
from model.data_treatment import load_config
from model.crypto_data import fetch_candlestick_data

import requests
import pandas as pd
import logging
import time
from model.data_treatment import load_config

def get_live_data(currency="usd", max_retries=5):
    """Fetches real-time cryptocurrency market data from CoinGecko with retry logic."""
    config = load_config()
    base_url = config["base_url"]
    url = f"{base_url}coins/markets?vs_currency={currency}&order=market_cap_desc&per_page=10&page=1"

    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            
            # ✅ Handle API Rate Limiting (429)
            if response.status_code == 429:
                wait_time = 2 ** retries  # Exponential backoff: 2, 4, 8, 16 seconds
                logging.warning(f"API rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
                continue  # Retry the request

            response.raise_for_status()  # Raise error for other HTTP issues
            live_data = pd.DataFrame(response.json())
            return live_data

        except requests.RequestException as e:
            logging.error(f"Error fetching live cryptocurrency data: {e}")
            retries += 1
            time.sleep(2 ** retries)  # Wait before retrying

    logging.error("Max retries reached. Failed to fetch cryptocurrency data.")
    return None  # Return None if all retries fail


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