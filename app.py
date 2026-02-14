"""
Streamlit application for Cryptocurrency Dashboard.
Main view layer that coordinates with controller and model.
"""

import streamlit as st
import pandas as pd
from streamlit.runtime.caching import cache_data

from controller.controller import *
from view.view import *
from model.model import *

# ✅ Cache live data to reduce API calls
@cache_data
def get_cached_live_data(currency):
    return get_live_data(currency)

def run_app():
    """Main function to run the Streamlit Cryptocurrency Dashboard."""
    
    # Page configuration
    st.set_page_config(
        page_title="Crypto Dashboard",
        layout="wide",
        page_icon="📈",
        initial_sidebar_state="expanded"
        )
    st.title("📈 Cryptocurrency Market Dashboard")

    # Dashboard Description
    st.markdown("""
    Get **real-time cryptocurrency data** powered by **CoinGecko API**.

    Track **live prices**, analyze **historical trends** with **candlestick charts**, 
    and switch between **USD, EUR, and GBP**.

    ### How to use:
    1️⃣ **Choose a Currency** – Select **USD, EUR, or GBP** from the sidebar.  
    2️⃣ **Select a Cryptocurrency** – Pick from the available options.  
    3️⃣ **Adjust Time Range** – Choose a period for historical price analysis.
    """)

    # Sidebar - User selection
    with st.sidebar:
        st.header("Settings")
        selected_currency = st.selectbox("Select Currency", ["usd", "eur", "gbp"])
        currency_symbol = {"usd": "USD", "eur": "EUR", "gbp": "GBP"}[selected_currency]
        
        # Get cached data
        live_data = get_cached_live_data(selected_currency)
        
        if live_data is None:
            st.warning("⚠️ CoinGecko API rate limit reached. Try again in a few minutes.")
            st.stop()
        
        # Available coins for selection
        available_coins = live_data['name'].tolist()
        selected_coin = st.selectbox("Select Cryptocurrency", available_coins).lower()
        
        # Candlestick Data Range Selection
        st.subheader("Historical Data")
        selected_days = st.selectbox(
            "Select Time Range (days)", 
            VALID_OHLC_DAYS[:-1],  # Exclude "max"
            help="Choose the time period for historical price analysis"
        )
        

    # Process and display live data
    if live_data is not None:
        display_live_data(live_data, currency_symbol)
        
        # Fetch and display candlestick chart
        display_candlestick_chart(selected_coin, selected_currency, selected_days)

def display_live_data(live_data, currency_symbol):
    """Display formatted live cryptocurrency data."""
    
    st.subheader("Live Cryptocurrency Prices")
    
    # Prepare data for display
    display_df = prepare_live_data_table(live_data, currency_symbol)
    
    # Display table with formatted columns
    st.dataframe(
        display_df,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank"),
            "name": st.column_config.TextColumn("Name"),
            "image": st.column_config.ImageColumn("Logo", width="small"),
            "symbol": st.column_config.TextColumn("Symbol"),
            "current_price": st.column_config.NumberColumn(f"Price ({currency_symbol})"),
            "market_cap": st.column_config.NumberColumn("Market Cap"),
            "Dominance (%)": st.column_config.NumberColumn("Dominance (%)", format="%.2f%%"),
            "Circulating Supply": st.column_config.NumberColumn("Circulating Supply"),
            "total_volume": st.column_config.NumberColumn("Total Volume"),
            "All Time High": st.column_config.NumberColumn(f"All Time High ({currency_symbol})"),
            "All Time High Change %": st.column_config.NumberColumn("ATH Change (%)", format="%.2f%%"),
            "All Time High Date": st.column_config.DateColumn("ATH Date", format="YYYY-MM-DD"),
        },
        hide_index=True,
        use_container_width=True
    )
    
def prepare_live_data_table(data, currency_symbol):
    """Prepare and format live data for display."""
    
    # Create a copy to avoid modifying cached data
    df = data.copy()
    
    # Define columns to keep and their display names
    column_mapping = {
        'market_cap_rank': 'Rank',
        'name': 'name',
        'image': 'image',
        'symbol': 'symbol',
        'current_price': 'current_price',
        'market_cap': 'market_cap',
        'market_cap_percentage': 'Dominance (%)',
        'circulating_supply': 'Circulating Supply',
        'total_volume': 'total_volume',
        'ath': 'All Time High',
        'ath_change_percentage': 'All Time High Change %',
        'ath_date': 'All Time High Date'
    }
    
    # Select and rename columns
    display_columns = [col for col in column_mapping.keys() if col in df.columns]
    df = df[display_columns]
    df = df.rename(columns=column_mapping)
    
    # Format columns
    if 'All Time High Date' in df.columns:
        df['All Time High Date'] = pd.to_datetime(df['All Time High Date']).dt.date
    
    # Format percentages
    if 'All Time High Change %' in df.columns:
        df['All Time High Change %'] = df['All Time High Change %']
    
    if 'Dominance (%)' in df.columns:
        df['Dominance (%)'] = df['Dominance (%)'] * 100
    
    return df

def display_candlestick_chart(coin_id, currency, days):
    """Display candlestick chart for selected cryptocurrency."""
    
    if days == 1:
        st.subheader(f"{coin_id.capitalize()} Price Chart - Last 24 Hours")
    else:
        st.subheader(f"{coin_id.capitalize()} Price Chart - Last {days} Days")
    
    # Chart description
    st.markdown("""
    This candlestick chart visualizes historical price movements:
    - **Green candles**: Price increased during the period
    - **Red candles**: Price decreased during the period
    - Each candle shows: Open, High, Low, Close prices
    """)
    
    # Fetch candlestick data
    with st.spinner(f"Loading {days}-day data for {coin_id}..."):
        candlestick_data = get_candlestick_data(coin_id, currency, days)
    
    # Display chart or message
    if candlestick_data is not None and not candlestick_data.empty:
        chart = create_candlestick_chart(candlestick_data, coin_id)
        st.plotly_chart(chart, use_container_width=True)
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            latest_close = candlestick_data['close'].iloc[-1]
            st.metric("💰 Latest Price", format_price(latest_close, currency))
        
        with col2:
            price_change = candlestick_data['close'].iloc[-1] - candlestick_data['open'].iloc[0]
            change_pct = (price_change / candlestick_data['open'].iloc[0]) * 100
            sign = "+" if price_change >= 0 else "-"
            sign_change_pct = "+" if change_pct >= 0 else "-"
            st.metric("📈 Period Change", f"{sign}{format_price(abs(price_change), currency)}", delta=f"{sign_change_pct}{abs(change_pct):.2f}%", delta_color="normal")
        
        with col3:
            highest = candlestick_data['high'].max()
            st.metric("⬆️ Period High", format_price(highest, currency))
        
        with col4:
            lowest = candlestick_data['low'].min()
            st.metric("⬇️ Period Low", format_price(lowest, currency))
    else:
        st.warning(f"No historical data found for {coin_id}.")