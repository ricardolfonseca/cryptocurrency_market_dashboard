"""
Streamlit application for Cryptocurrency Dashboard.
Main view layer that coordinates with controller and view.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from controller.controller import (
    get_live_data,
    get_candlestick_data,
    ask_chatbot,
    VALID_OHLC_DAYS
)
from view.view import create_candlestick_chart, MarketDataFormatter as fmt

# Cache live data for 60 seconds
@st.cache_data(ttl=60)
def get_cached_live_data(currency):
    st.session_state.last_refresh_time = datetime.now()
    return get_live_data(currency)

def run_app():
    st.set_page_config(
        page_title="Crypto Dashboard",
        layout="wide",
        page_icon="📈",
        initial_sidebar_state="auto"
    )
    if "last_refresh_time" not in st.session_state:
        st.session_state.last_refresh_time = datetime.now()

    # ---- Top bar with title and chat button ----
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        st.title("📈 Cryptocurrency Market Dashboard")
    with col3:
        # Chat popover button
        with st.popover("💬 Chat", width="stretch"):
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            if prompt := st.chat_input("Ask about cryptocurrencies..."):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        live_data = st.session_state.get("live_data", None)
                        currency = st.session_state.get("selected_currency", "usd")
                        response = ask_chatbot(prompt, live_data, currency.upper())
                        st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

    # ---- Main dashboard description ----
    st.markdown("""
    Get **real-time cryptocurrency data** powered by **CoinGecko API**.

    Track **live prices**, analyze **historical trends** with **candlestick charts**, 
    and switch between **USD and EUR**.

    ### How to use:
    1️⃣ **Choose a Currency** - Select **USD or EUR** from the sidebar.  
    2️⃣ **Select a Cryptocurrency** - Pick from the available options.  
    3️⃣ **Adjust Time Range** - Choose a period for historical price analysis.
    """)

    # ---- Sidebar ----
    with st.sidebar:
        st.header("Settings")
        selected_currency = st.selectbox("Select Currency", ["usd", "eur"])
        st.session_state.selected_currency = selected_currency
        currency_symbol = {"usd": "USD", "eur": "EUR"}[selected_currency]

        live_data = get_cached_live_data(selected_currency)
        if live_data is None:
            st.warning("⚠️ CoinGecko API rate limit reached. Try again in a few minutes.")
            st.stop()

        st.session_state.live_data = live_data

        available_coins = live_data['name'].tolist()
        selected_coin = st.selectbox("Select Cryptocurrency", available_coins).lower()

        st.subheader("Historical Data")
        selected_days = st.selectbox(
            "Select Time Range (days)",
            VALID_OHLC_DAYS[:-1],  # Exclude "max"
            help="Choose the time period for historical price analysis"
        )

    # ---- Main content ----
    if live_data is not None:
        display_live_data(live_data, currency_symbol)
        display_candlestick_chart(selected_coin, selected_currency, selected_days)

def display_live_data(live_data, currency_symbol):
    st.subheader("Live Cryptocurrency Prices")
    last_refresh = st.session_state.last_refresh_time
    st.caption(f'Last refreshed: {last_refresh.strftime("%Y-%m-%d %H:%M:%S")}')

    display_df = prepare_live_data_table(live_data, currency_symbol)

    symbol = "$" if currency_symbol == "USD" else "€"

    st.dataframe(
        display_df,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
            "name": st.column_config.TextColumn("Name"),
            "image": st.column_config.ImageColumn("Logo", width="small"),
            "symbol": st.column_config.TextColumn("Symbol"),
            "current_price": st.column_config.TextColumn(f"Price ({currency_symbol})"),
            "market_cap": st.column_config.TextColumn("Market Cap"),
            "total_volume": st.column_config.TextColumn("Total Volume"),
            "Circulating Supply": st.column_config.TextColumn("Circulating Supply"),
            "All Time High": st.column_config.TextColumn(f"All Time High ({currency_symbol})"),
            "All Time High Date": st.column_config.DateColumn("ATH Date", format="YYYY-MM-DD"),
        },
        hide_index=True,
        use_container_width=True
    )

def prepare_live_data_table(data, currency_symbol):
    df = data.copy()

    column_mapping = {
        'market_cap_rank': 'Rank',
        'name': 'name',
        'image': 'image',
        'symbol': 'symbol',
        'current_price': 'current_price',
        'market_cap': 'market_cap',
        'circulating_supply': 'Circulating Supply',
        'total_volume': 'total_volume',
        'ath': 'All Time High',
        'ath_date': 'All Time High Date'
    }

    display_columns = [col for col in column_mapping.keys() if col in df.columns]
    df = df[display_columns]
    df = df.rename(columns=column_mapping)

    # Format dates
    if 'All Time High Date' in df.columns:
        df['All Time High Date'] = pd.to_datetime(df['All Time High Date']).dt.date

    # --- Formatting numerical columns ---
    symbol = "$" if currency_symbol == "USD" else "€"

    # Columns with 2 decimals and symbol
    for col in ['current_price', 'All Time High']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{symbol}{x:,.2f}")

    # Columns with 0 decimals and symbol
    for col in ['market_cap', 'total_volume']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:,.0f}")

    # Circulating Supply: without symbol, two decimal places
    if 'Circulating Supply' in df.columns:
        df['Circulating Supply'] = df['Circulating Supply'].apply(lambda x: f"{x:,.2f}")

    return df

def display_candlestick_chart(coin_id, currency, days):
    if days == 1:
        st.subheader(f"{coin_id.capitalize()} Price Chart - Last 24 Hours")
    else:
        st.subheader(f"{coin_id.capitalize()} Price Chart - Last {days} Days")

    st.markdown("""
    This candlestick chart visualizes historical price movements:
    - **Green candles**: Price increased during the period
    - **Red candles**: Price decreased during the period
    - Each candle shows: Open, High, Low, Close prices
    """)

    st.caption(
        "Note: The chart shows historical data. The latest candle's close may differ from "
        "the current live price in the table above, as that updates more frequently."
    )

    with st.spinner(f"Loading {days}-day data for {coin_id}..."):
        candlestick_data = get_candlestick_data(coin_id, currency, days)

    if candlestick_data is not None and not candlestick_data.empty:
        chart = create_candlestick_chart(candlestick_data, coin_id, currency.upper())
        st.plotly_chart(chart, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            latest_close = candlestick_data['close'].iloc[-1]
            st.metric("💰 Latest Close (Period End)", fmt.format_price(latest_close, currency))
        with col2:
            price_change = candlestick_data['close'].iloc[-1] - candlestick_data['open'].iloc[0]
            change_pct = (price_change / candlestick_data['open'].iloc[0]) * 100
            sign = "+" if price_change >= 0 else "-"
            period_label = "📈 Period Change (last 24 Hours)" if days == 1 else f"📈 Period Change (last {days} Days)"
            st.metric(period_label,
                      f"{sign}{fmt.format_price(abs(price_change), currency)}",
                      delta=f"{sign}{abs(change_pct):.2f}%",
                      delta_color="normal")
        with col3:
            highest = candlestick_data['high'].max()
            st.metric("⬆️ Period High", fmt.format_price(highest, currency))
        with col4:
            lowest = candlestick_data['low'].min()
            st.metric("⬇️ Period Low", fmt.format_price(lowest, currency))
    else:
        st.warning(f"No historical data found for {coin_id}.")