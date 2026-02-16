class MarketDataFormatter:
    """Utility class for formatting market data for display."""

    @staticmethod
    def format_price(price, currency="USD"):
        """Format price with currency symbol."""
        symbols = {"usd": "$", "eur": "€", "gbp": "£", "USD": "$", "EUR": "€", "GBP": "£"}
        symbol = symbols.get(currency, "$")
        return f"{symbol}{price:,.2f}"

    @staticmethod
    def format_large_number(num):
        """Format large numbers with K, M, B suffixes."""
        if num >= 1e9:
            return f"{num/1e9:.2f}B"
        elif num >= 1e6:
            return f"{num/1e6:.2f}M"
        elif num >= 1e3:
            return f"{num/1e3:.2f}K"
        return f"{num:.2f}"