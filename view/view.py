"""
View layer for Cryptocurrency Dashboard.
Handles all data visualization components.
"""

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def create_candlestick_chart(data, coin_name):
    """
    Create a candlestick chart for cryptocurrency OHLC data.
    
    Args:
        data (DataFrame): OHLC data with columns: timestamp, open, high, low, close
        coin_name (str): Name of the cryptocurrency
        
    Returns:
        plotly.graph_objects.Figure: Candlestick chart
    """
    if data is None or data.empty:
        return create_empty_chart("No data available")
    
    # Create candlestick trace
    candlestick = go.Candlestick(
        x=data["timestamp"],
        open=data["open"],
        high=data["high"],
        low=data["low"],
        close=data["close"],
        name=coin_name,
        increasing_line_color='#2E8B57',  # Sea green for up
        decreasing_line_color='#DC143C',  # Crimson for down
    )
    
    # Create line trace for closing prices
    line_trace = go.Scatter(
        x=data["timestamp"],
        y=data["close"],
        mode='lines',
        name='Close Price',
        line=dict(color='#4169E1', width=1),  # Royal blue
        opacity=0.5
    )
    
    # Create figure
    fig = go.Figure(data=[candlestick, line_trace])
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'{coin_name.capitalize()} - Candlestick Chart',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        hovermode="x unified",
        height=600,
        margin=dict(t=80, b=50, l=50, r=50),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Update axis properties
    fig.update_xaxes(
        tickformat="%b %d\n%H:%M",
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    
    fig.update_yaxes(
        tickprefix="$",
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    
    return fig

def create_price_line_chart(data, title="Cryptocurrency Prices"):
    """
    Create a line chart for cryptocurrency prices.
    
    Args:
        data (DataFrame): Data with timestamp and price columns
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Line chart
    """
    if data is None or data.empty:
        return create_empty_chart("No data available")
    
    fig = px.line(
        data,
        x="timestamp",
        y="close",
        title=title,
        labels={
            "timestamp": "Date",
            "close": "Price (USD)"
        },
        color_discrete_sequence=['#4169E1']  # Royal blue
    )
    
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    fig.update_traces(
        mode='lines+markers',
        marker=dict(size=4),
        line=dict(width=2)
    )
    
    return fig

def create_empty_chart(message="No data available"):
    """
    Create an empty chart with a message.
    
    Args:
        message (str): Message to display
        
    Returns:
        plotly.graph_objects.Figure: Empty chart with message
    """
    fig = go.Figure()
    
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[{
            'text': message,
            'xref': "paper",
            'yref': "paper",
            'showarrow': False,
            'font': {'size': 20}
        }],
        template="plotly_white",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

'''def display_metric_card(title, value, delta=None, delta_prefix="", icon="📊"):
    """
    Display a metric card in Streamlit.
    
    Args:
        title (str): Metric title
        value (str): Main value
        delta (str, optional): Delta value
        delta_prefix (str): Prefix for delta (+, -, etc.)
        icon (str): Emoji icon
    """
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<h1 style='font-size: 2.5rem;'>{icon}</h1>", unsafe_allow_html=True)
    with col2:
        if delta:
            st.metric(title, value, f"{delta_prefix}{delta}")
        else:
            st.metric(title, value)
'''

def format_currency(value, currency="USD"):
    """
    Format currency values for display.
    
    Args:
        value (float): Currency value
        currency (str): Currency code
        
    Returns:
        str: Formatted currency string
    """
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }
    
    symbol = currency_symbols.get(currency.upper(), "$")
    
    if abs(value) >= 1_000_000_000:
        return f"{symbol}{value/1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"{symbol}{value/1_000_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"{symbol}{value/1_000:.2f}K"
    else:
        return f"{symbol}{value:.2f}"