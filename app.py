import streamlit as st
import pandas as pd
import time
from controller.exchange_controller import get_live_data, get_historical_data
from view.visualization import plot_live_prices, plot_historical_trend
from streamlit.runtime.caching import cache_data

def run_app():
    """Runs the Streamlit Cryptocurrency Market Dashboard."""

    st.title("📈 Cryptocurrency Market Dashboard")

    # Sidebar - User selection
    st.sidebar.header("Settings")
    selected_currency = st.sidebar.selectbox("Select Currency", ["usd", "eur", "gbp"])

    # Fetch live data to populate cryptocurrency selection
    live_data = get_live_data(currency=selected_currency)
    available_coins = live_data['name'].tolist() if live_data is not None else ["bitcoin", "ethereum"]
    selected_coin = st.sidebar.selectbox("Select Cryptocurrency", available_coins).lower()

    # Historical data range filter
    selected_days = st.sidebar.slider("Select Historical Data Range (days)", 1, 90, 30)

    st.write("*Note: Prices are refreshed every 10 minutes.*")

    if live_data is not None:
        # ✅ Format the "image" column to properly display images
        live_data["image"] = live_data["image"].astype(str)

        # ✅ Round numeric values for better readability
        numeric_columns = ["current_price", "market_cap", "total_volume", "high_24h", "low_24h", "price_change_24h", "price_change_percentage_24h"]
        for col in numeric_columns:
            if col in live_data.columns:
                live_data[col] = live_data[col].round(2)  # Round numbers

        # ✅ Display table with images and formatted numbers
        st.subheader("Live Cryptocurrency Prices")
        st.dataframe(
            live_data,
            column_config={
                "image": st.column_config.ImageColumn("Logo", width="small"),
                "current_price": st.column_config.NumberColumn("Price (USD)", format="%.2f"),
                "market_cap": st.column_config.NumberColumn("Market Cap", format="%.2f"),
                "total_volume": st.column_config.NumberColumn("Total Volume", format="%.2f"),
                "high_24h": st.column_config.NumberColumn("24h High", format="%.2f"),
                "low_24h": st.column_config.NumberColumn("24h Low", format="%.2f"),
                "price_change_24h": st.column_config.NumberColumn("24h Change", format="%.2f"),
                "price_change_percentage_24h": st.column_config.NumberColumn("24h Change (%)", format="%.2f"),
            },
            hide_index=True,  # ✅ Hide the default index column
        )

        # ✅ Add one paragraph space before the graph
        st.write("")  

        # ✅ Fetch & Display Historical Price Trend
        st.subheader(f"{selected_coin.capitalize()} Price Trend (Last {selected_days} Days)")
        historical_data = get_historical_data(selected_coin, selected_currency, selected_days)

        if historical_data is not None:
            historical_chart = plot_historical_trend(historical_data, selected_coin)
            st.plotly_chart(historical_chart)
        else:
            st.warning(f"No historical data found for {selected_coin}.")

    else:
        st.warning("Failed to fetch live cryptocurrency data.")

if __name__ == "__main__":
    run_app()