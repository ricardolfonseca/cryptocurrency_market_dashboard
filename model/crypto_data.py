import requests
import pandas as pd
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from model.data_treatment import load_config

# ✅ CoinGecko's valid OHLC time ranges
VALID_OHLC_DAYS = [1, 7, 14, 30, 90, 180, 365, "max"]

def closest_valid_days(days):
    """Find the closest valid OHLC time range supported by CoinGecko."""
    return min(VALID_OHLC_DAYS[:-1], key=lambda x: abs(x - days))  # Exclude "max" for rounding

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
    """Creates a retry session for API requests."""
    session = requests.Session()
    retry = Retry(
        total=retries, 
        read=retries, 
        connect=retries, 
        backoff_factor=backoff_factor, 
        status_forcelist=status_forcelist
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

def fetch_crypto_data(currency="usd"):
    """Fetches real-time cryptocurrency prices from CoinGecko."""
    config = load_config()
    base_url = config["base_url"]
    url = f"{base_url}coins/markets?vs_currency={currency}&order=market_cap_desc&per_page=10&page=1"

    try:
        session = requests_retry_session()
        response = session.get(url)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.RequestException as e:
        logging.error(f"Error fetching live cryptocurrency data: {e}")
        return None

def fetch_candlestick_data(coin_id="bitcoin", currency="usd", days=30):
    """Fetches historical OHLC (Open, High, Low, Close) cryptocurrency prices from CoinGecko."""
    config = load_config()
    base_url = config["base_url"]

    # ✅ Automatically adjust days to the closest supported range
    valid_days = closest_valid_days(days)
    url = f"{base_url}coins/{coin_id}/ohlc?vs_currency={currency}&days={valid_days}"

    try:
        session = requests_retry_session()
        response = session.get(url)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        
        logging.info(f"Fetched OHLC data for {coin_id}: {valid_days} days (requested: {days} days)")
        return df
    except requests.RequestException as e:
        logging.error(f"Error fetching candlestick data for {coin_id}: {e}")
        return None