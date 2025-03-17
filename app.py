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

    # ✅ Dashboard Description
    st.markdown(
        """
        Get **real-time cryptocurrency data** powered by **CoinGecko API**.

        Track **live prices**, analyze **historical trends** with **candlestick charts**, and switch between **USD, EUR, and GBP**.

        ### How to use:
        1️⃣ **Choose a Currency** – Select **USD, EUR, or GBP** from the sidebar.  
        2️⃣ **Select a Cryptocurrency** – Pick from the available options.  
        3️⃣ **Adjust Time Range** – Choose a period for historical price analysis.
        """
    )

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

    if live_data is not None:
        # ✅ Remove unnecessary columns
        columns_to_remove = [
            "id", "high_24h", "low_24h", "price_change_24h", 
            "price_change_percentage_24h", "market_cap_change_24h", 
            "market_cap_change_percentage_24h", "max_supply", "roi", "last_updated"
        ]
        live_data = live_data.drop(columns=[col for col in columns_to_remove if col in live_data.columns])

        # ✅ Rename columns
        column_rename = {
            "market_cap_rank": "Rank",
            "circulating_supply": "Circulating Supply",
            "ath": "All Time High",
            "ath_change_percentage": "All Time High Change Percentage",
            "ath_date": "All Time High Date",
            "market_cap_percentage": "Dominance (%)"
        }
        live_data = live_data.rename(columns=column_rename)

        # ✅ Convert `ath_date` to readable format
        if "All Time High Date" in live_data.columns:
            live_data["All Time High Date"] = pd.to_datetime(live_data["All Time High Date"]).dt.strftime('%Y-%m-%d')

        # ✅ Reorder columns (placing "Dominance (%)" next to Market Cap)
        column_order = [
            "Rank", "name", "image", "symbol", "current_price", 
            "market_cap", "Dominance (%)", "Circulating Supply", "total_volume", 
            "All Time High", "All Time High Change Percentage", "All Time High Date"
        ]
        live_data = live_data[[col for col in column_order if col in live_data.columns]]

        # ✅ Format the "image" column to properly display images
        live_data["image"] = live_data["image"].astype(str)

        # ✅ Round numeric values for better readability
        numeric_columns = ["current_price", "market_cap", "Circulating Supply", "total_volume", "All Time High", "All Time High Change Percentage", "Dominance (%)"]
        for col in numeric_columns:
            if col in live_data.columns:
                live_data[col] = live_data[col].round(2)  # Round numbers

        # ✅ Display table with dynamically updated currency label
        st.subheader("Live Cryptocurrency Prices")
        st.dataframe(
            live_data,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank"),
                "name": st.column_config.TextColumn("Name"),
                "image": st.column_config.ImageColumn("Logo", width="small"),
                "symbol": st.column_config.TextColumn("Symbol"),
                "current_price": st.column_config.NumberColumn(f"Price ({currency_symbol})", format="%.2f"),
                "market_cap": st.column_config.NumberColumn("Market Cap", format="%.2f"),
                "Dominance (%)": st.column_config.NumberColumn("Dominance (%)", format="%.2f"),
                "Circulating Supply": st.column_config.NumberColumn("Circulating Supply", format="%.2f"),
                "total_volume": st.column_config.NumberColumn("Total Volume", format="%.2f"),
                "All Time High": st.column_config.NumberColumn(f"All Time High ({currency_symbol})", format="%.2f"),
                "All Time High Change Percentage": st.column_config.NumberColumn("All Time High Change (%)", format="%.2f"),
                "All Time High Date": st.column_config.TextColumn("All Time High Date"),
            },
            hide_index=True,
        )
    
        # Fetch & Display Candlestick Chart
        if selected_days == 1:
            st.subheader(f"{selected_coin.capitalize()} Price Chart for the last 24 hours")
        else:
            st.subheader(f"{selected_coin.capitalize()} Price Chart for {selected_days} Days")

        # Add Chart Description Below the Title
        st.markdown(
            """
            This candlestick chart visualizes the historical price movements of the selected cryptocurrency.
            Each candlestick represents a time period, showing **opening, highest, lowest, and closing prices**.
            Green candles indicate price increases, while red candles show declines.
            """)

        candlestick_data = fetch_candlestick_data(selected_coin, selected_currency, selected_days)

        if candlestick_data is not None and not candlestick_data.empty:
            candlestick_chart = plot_candlestick_chart(candlestick_data, selected_coin)
            st.plotly_chart(candlestick_chart)
        else:
            st.warning(f"No candlestick data found for {selected_coin}.")

if __name__ == "__main__":
    run_app()