import streamlit as st
import pandas as pd
import time
from controller.exchange_controller import get_live_data, fetch_candlestick_data
from view.visualization import plot_live_prices, plot_candlestick_chart
from model.crypto_data import VALID_OHLC_DAYS
from streamlit.runtime.caching import cache_data

def run_app():
    """Runs the Streamlit Cryptocurrency Market Dashboard."""

    st.title("📈 Cryptocurrency Market Dashboard")

    # Sidebar - User selection
    st.sidebar.header("Settings")
    selected_currency = st.sidebar.selectbox("Select Currency", ["usd", "eur", "gbp"])
    currency_symbol = {"usd": "USD", "eur": "EUR", "gbp": "GBP"}[selected_currency]  # Map currency codes to symbols

    # Fetch live data to populate cryptocurrency selection
    live_data = get_live_data(currency=selected_currency)
    available_coins = live_data['name'].tolist() if live_data is not None else ["bitcoin", "ethereum"]
    selected_coin = st.sidebar.selectbox("Select Cryptocurrency", available_coins).lower()

    # ✅ Candlestick Data Range Selection (Restricted to Valid OHLC Days)
    selected_days = st.sidebar.selectbox("Select Candlestick Data Range (days)", VALID_OHLC_DAYS[:-1])  # Exclude "max"

    st.write("*Note: Prices are refreshed every 10 minutes.*")

    if live_data is not None:
        # ✅ Format the "image" column to properly display images
        live_data["image"] = live_data["image"].astype(str)

        # ✅ Round numeric values for better readability
        numeric_columns = ["current_price", "market_cap", "total_volume", "high_24h", "low_24h", "price_change_24h", "price_change_percentage_24h"]
        for col in numeric_columns:
            if col in live_data.columns:
                live_data[col] = live_data[col].round(2)  # Round numbers

        # ✅ Display table with dynamically updated currency label
        st.subheader("Live Cryptocurrency Prices")
        st.dataframe(
            live_data,
            column_config={
                "image": st.column_config.ImageColumn("Logo", width="small"),
                f"current_price": st.column_config.NumberColumn(f"Price ({currency_symbol})", format="%.2f"),
                "market_cap": st.column_config.NumberColumn("Market Cap", format="%.2f"),
                "total_volume": st.column_config.NumberColumn("Total Volume", format="%.2f"),
                "high_24h": st.column_config.NumberColumn(f"24h High ({currency_symbol})", format="%.2f"),
                "low_24h": st.column_config.NumberColumn(f"24h Low ({currency_symbol})", format="%.2f"),
                "price_change_24h": st.column_config.NumberColumn(f"24h Change ({currency_symbol})", format="%.2f"),
                "price_change_percentage_24h": st.column_config.NumberColumn("24h Change (%)", format="%.2f"),
            },
            hide_index=True,
        )

        # ✅ Add space before the candlestick chart
        st.write("")

        # ✅ Fetch & Display Candlestick Chart
        st.subheader(f"{selected_coin.capitalize()} Candlestick Chart (Last {selected_days} Days)")

        candlestick_data = fetch_candlestick_data(selected_coin, selected_currency, selected_days)

        if candlestick_data is not None:
            candlestick_chart = plot_candlestick_chart(candlestick_data, selected_coin)
            st.plotly_chart(candlestick_chart)
        else:
            st.warning(f"No candlestick data found for {selected_coin}.")

    else:
        st.warning("Failed to fetch live cryptocurrency data.")

if __name__ == "__main__":
    run_app()