from model.crypto_data import fetch_crypto_data, fetch_historical_data

def get_live_data(currency):
    """Fetch live cryptocurrency data."""
    return fetch_crypto_data(currency=currency)

def get_historical_data(coin, currency, days):
    """Fetch historical cryptocurrency data."""
    return fetch_historical_data(coin_id=coin, currency=currency, days=days)