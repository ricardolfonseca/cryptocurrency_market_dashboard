from model.crypto_data import fetch_crypto_data, fetch_candlestick_data

def get_live_data(currency):
    """Fetch live cryptocurrency data."""
    return fetch_crypto_data(currency=currency)

def get_historical_data(coin, currency, days):
    """Fetch OHLC (candlestick) cryptocurrency data."""
    return fetch_candlestick_data(coin_id=coin, currency=currency, days=days)