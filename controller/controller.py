"""
Controller layer for the Cryptocurrency Dashboard.
Coordinates between model and view, providing simplified access to data and services.
"""

import logging
from model.CryptoDataProvider import CryptoDataProvider, VALID_OHLC_DAYS
from model.GeminiChat import GeminiChat

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Instância única do chatbot Gemini (usa as secrets do Streamlit)
_gemini_chat = GeminiChat()

def get_live_data(currency="usd"):
    """
    Fetch real-time cryptocurrency market data.
    Args:
        currency (str): 'usd' or 'eur'
    Returns:
        pandas.DataFrame or None
    """
    try:
        return CryptoDataProvider.fetch_crypto_data(currency)
    except Exception as e:
        logger.error(f"Error in get_live_data: {e}")
        return None

def get_candlestick_data(coin_id, currency, days):
    """
    Fetch historical OHLC data for a cryptocurrency.
    Args:
        coin_id (str): e.g., 'bitcoin'
        currency (str): 'usd' or 'eur'
        days (int): number of days
    Returns:
        pandas.DataFrame or None
    """
    try:
        return CryptoDataProvider.fetch_candlestick_data(coin_id, currency, days)
    except Exception as e:
        logger.error(f"Error in get_candlestick_data: {e}")
        return None

def ask_chatbot(question, live_data=None, currency="USD"):
    """
    Send a question to the Gemini chatbot with market context.
    Args:
        question (str): user's question
        live_data (DataFrame): current market data (optional)
        currency (str): currency code (USD, EUR)
    Returns:
        str: chatbot's response
    """
    try:
        return _gemini_chat.get_response(question, live_data, currency)
    except Exception as e:
        logger.error(f"Error in ask_chatbot: {e}")
        return f"Sorry, an error occurred: {str(e)}"