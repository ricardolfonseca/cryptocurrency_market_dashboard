import requests
import pandas as pd
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from model.data_treatment import load_config

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
    """Creates a retry session for API requests."""
    session = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
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

def fetch_historical_data(coin_id="bitcoin", currency="usd", days=30):
    """Fetches historical cryptocurrency prices from CoinGecko."""
    config = load_config()
    base_url = config["base_url"]
    url = f"{base_url}coins/{coin_id}/market_chart?vs_currency={currency}&days={days}&interval=daily"

    try:
        session = requests_retry_session()
        response = session.get(url)
        response.raise_for_status()
        data = response.json()["prices"]
        df = pd.DataFrame(data, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except requests.RequestException as e:
        logging.error(f"Error fetching historical data for {coin_id}: {e}")
        return None