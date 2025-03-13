import plotly.express as px
import plotly.graph_objects as go

def plot_live_prices(data):
    """Generates a live price line chart for cryptocurrencies."""
    fig = px.line(
        data,
        x=data.index,
        y="current_price",
        title="Live Cryptocurrency Prices",
        labels={"current_price": "Price (USD)", "index": "Cryptocurrency"},
        markers=True
    )

    return fig

def plot_candlestick_chart(data, coin_name):
    """Generates a candlestick chart for cryptocurrency OHLC prices."""
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data["timestamp"],
                open=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["close"],
                name=coin_name,
            )
        ]
    )

    # Customize chart layout
    fig.update_layout(
        title=f"{coin_name.capitalize()} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )

    return fig