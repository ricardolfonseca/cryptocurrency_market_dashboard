"""
View layer for Cryptocurrency Dashboard.
Handles all data visualization components and formatting utilities.
"""

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# FORMATTING UTILITIES

class MarketDataFormatter:
    """Utility class for formatting market data for display."""

    @staticmethod
    def format_price(price, currency="USD"):
        """Format price with currency symbol."""
        symbols = {"usd": "$", "eur": "€", "USD": "$", "EUR": "€"}
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


# CHART CREATION FUNCTIONS

def create_candlestick_chart(data, coin_name, currency="USD"):
    """
    Create a candlestick chart for cryptocurrency OHLC data.

    Args:
        data (DataFrame): OHLC data with columns: timestamp, open, high, low, close
        coin_name (str): Name of the cryptocurrency
        currency (str): Currency code (USD, EUR) for axis label and prefix

    Returns:
        plotly.graph_objects.Figure: Candlestick chart
    """
    if data is None or data.empty:
        return create_empty_chart("No data available")

    # Determine currency symbol
    symbols = {"USD": "$", "EUR": "€"}
    symbol = symbols.get(currency.upper(), "$")

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
        yaxis_title=f"Price ({currency.upper()})",
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
        tickprefix=symbol,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )

    return fig


def create_price_line_chart(data, title="Cryptocurrency Prices", currency="USD"):
    """
    Create a line chart for cryptocurrency prices.

    Args:
        data (DataFrame): Data with timestamp and price columns
        title (str): Chart title
        currency (str): Currency code for axis label and prefix

    Returns:
        plotly.graph_objects.Figure: Line chart
    """
    if data is None or data.empty:
        return create_empty_chart("No data available")

    symbols = {"USD": "$", "EUR": "€"}
    symbol = symbols.get(currency.upper(), "$")

    fig = px.line(
        data,
        x="timestamp",
        y="close",
        title=title,
        labels={
            "timestamp": "Date",
            "close": f"Price ({currency.upper()})"
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

    # Update y-axis tick prefix
    fig.update_yaxes(tickprefix=symbol)

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