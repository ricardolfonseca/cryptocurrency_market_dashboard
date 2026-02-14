"""
Controller layer for the Cryptocurrency Dashboard.
Handles business logic and coordinates between model and view.
"""

import logging
from model.model import *

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_live_data(currency="usd"):
    """
    Fetch real-time cryptocurrency market data.
    
    Args:
        currency (str): Currency code (usd, eur, gbp)
        
    Returns:
        pandas.DataFrame or None: Market data or None if error
    """
    try:
        return fetch_crypto_data(currency)
    except Exception as e:
        logger.error(f"Error in get_live_data: {e}")
        return None

def get_candlestick_data(coin_id, currency, days):
    """
    Fetch historical OHLC data for a cryptocurrency.
    
    Args:
        coin_id (str): Cryptocurrency ID (e.g., 'bitcoin')
        currency (str): Currency code
        days (int): Number of days for historical data
        
    Returns:
        pandas.DataFrame or None: OHLC data or None if error
    """
    try:
        return fetch_candlestick_data(coin_id, currency, days)
    except Exception as e:
        logger.error(f"Error in get_candlestick_data: {e}")
        return None

def get_config():
    """
    Get application configuration.
    
    Returns:
        dict: Configuration dictionary
    """
    return load_config()