"""
Model layer for Cryptocurrency Dashboard.
Handles data fetching, configuration, and logging.
"""

import json
import os
import logging
import pandas as pd
import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# CONFIGURATION & LOGGING

class CustomFormatter(logging.Formatter):
    """Custom logging formatter with milliseconds."""
    
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def configure_logging():
    """
    Configure application logging.
    """
    log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
    formatter = CustomFormatter(log_format)
    
    # File handler
    file_handler = logging.FileHandler("exchange.log", mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])

# Global variable for config warning
_config_loaded = False

def load_config():
    """
    Load configuration from JSON file or use defaults.
    """
    global _config_loaded
    config_file = "config/config.json"
    
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return json.load(file)
    
    # Show warning only once
    if not _config_loaded:
        logging.warning("Config file not found. Using defaults.")
        _config_loaded = True
    
    return {"base_url": "https://api.coingecko.com/api/v3/"}


# DATA FETCHING FUNCTIONS

# Valid OHLC time ranges supported by CoinGecko
VALID_OHLC_DAYS = [1, 7, 14, 30, 90, 180, 365, "max"]

def closest_valid_days(days):
    """
    Find the closest valid OHLC time range.
    
    Args:
        days (int): Requested number of days
        
    Returns:
        int: Closest valid day count
    """
    # Exclude "max" for rounding
    return min(VALID_OHLC_DAYS[:-1], key=lambda x: abs(x - days))

def requests_retry_session(retries=3, backoff_factor=0.3, 
                          status_forcelist=(500, 502, 503, 504)):
    """
    Create a retry session for API requests.
    
    Args:
        retries (int): Number of retries
        backoff_factor (float): Backoff factor
        status_forcelist (tuple): HTTP status codes to retry
        
    Returns:
        requests.Session: Configured session
    """
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
    """
    Fetch real-time cryptocurrency prices from CoinGecko.
    
    Args:
        currency (str): Currency code (usd, eur, gbp)
        
    Returns:
        pandas.DataFrame or None: Market data or None if error
    """
    config = load_config()
    base_url = config["base_url"]
    url = f"{base_url}coins/markets?vs_currency={currency}&order=market_cap_desc&per_page=10&page=1"
    
    try:
        session = requests_retry_session()
        response = session.get(url)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.RequestException as e:
        logging.error(f"Error fetching cryptocurrency data: {e}")
        return None

def fetch_candlestick_data(coin_id="bitcoin", currency="usd", days=30):
    """
    Fetch historical OHLC (Open, High, Low, Close) prices.
    
    Args:
        coin_id (str): Cryptocurrency ID
        currency (str): Currency code
        days (int): Number of days for historical data
        
    Returns:
        pandas.DataFrame or None: OHLC data or None if error
    """
    config = load_config()
    base_url = config["base_url"]
    
    # Adjust days to closest valid range
    valid_days = closest_valid_days(days)
    url = f"{base_url}coins/{coin_id}/ohlc?vs_currency={currency}&days={valid_days}"
    
    try:
        session = requests_retry_session()
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        
        logging.info(f"Fetched OHLC data for {coin_id}: {valid_days} days")
        return df
    except requests.RequestException as e:
        logging.error(f"Error fetching candlestick data for {coin_id}: {e}")
        return None


# UTILITY FUNCTIONS

def format_price(price, currency="USD"):
    """
    Format price with currency symbol.
    
    Args:
        price (float): Price value
        currency (str): Currency code
        
    Returns:
        str: Formatted price string
    """
    currency_symbols = {
        "usd": "$",
        "eur": "€", 
        "gbp": "£",
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }
    
    symbol = currency_symbols.get(currency, "$")
    return f"{symbol}{price:,.2f}"

def format_large_number(num):
    """
    Format large numbers with K, M, B suffixes.
    
    Args:
        num (float): Number to format
        
    Returns:
        str: Formatted number
    """
    if num >= 1e9:
        return f"{num/1e9:.2f}B"
    elif num >= 1e6:
        return f"{num/1e6:.2f}M"
    elif num >= 1e3:
        return f"{num/1e3:.2f}K"
    return f"{num:.2f}"