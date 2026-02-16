import pandas as pd
import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Global constants
VALID_OHLC_DAYS = [1, 7, 14, 30, 90, 180, 365, "max"]

class CryptoDataProvider:
    """Handles all interactions with the CoinGecko API."""

    BASE_URL = "https://api.coingecko.com/api/v3/"

    @staticmethod
    def closest_valid_days(days):
        """Find the closest valid OHLC time range."""
        return min(VALID_OHLC_DAYS[:-1], key=lambda x: abs(x - days))

    @staticmethod
    def requests_retry_session(retries=3, backoff_factor=0.3,
                               status_forcelist=(500, 502, 503, 504)):
        """Create a requests session with retry strategy."""
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

    @classmethod
    def fetch_crypto_data(cls, currency="usd"):
        """Fetch real-time cryptocurrency prices."""
        url = f"{cls.BASE_URL}coins/markets?vs_currency={currency}&order=market_cap_desc&per_page=10&page=1"
        try:
            session = cls.requests_retry_session()
            response = session.get(url)
            response.raise_for_status()
            return pd.DataFrame(response.json())
        except requests.RequestException as e:
            logging.error(f"Error fetching cryptocurrency data: {e}")
            return None

    @classmethod
    def fetch_candlestick_data(cls, coin_id="bitcoin", currency="usd", days=30):
        """Fetch historical OHLC prices."""
        valid_days = cls.closest_valid_days(days)
        url = f"{cls.BASE_URL}coins/{coin_id}/ohlc?vs_currency={currency}&days={valid_days}"
        try:
            session = cls.requests_retry_session()
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