import plotly.graph_objects as go
import plotly.express as px
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

def plot_live_prices(df):
    """Creates a bar chart for live cryptocurrency prices."""
    if df is None or df.empty:
        logging.error("No data available for plotting live prices.")
        return None
    
    fig = px.bar(df, x='name', y='current_price', text='current_price', 
                 title='Live Cryptocurrency Prices', labels={'current_price': 'Price (USD)'}, 
                 color='market_cap', hover_data=['market_cap', 'total_volume'])
    
    fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
    fig.update_layout(xaxis_title='Cryptocurrency', yaxis_title='Price (USD)')
    return fig

def plot_historical_trend(df, coin_name='Bitcoin', fast_render=False):
    """Creates a line chart for historical cryptocurrency prices with an optimized rendering option."""
    if df is None or df.empty:
        logging.error(f"No historical data available for {coin_name}.")
        return None

    fig = go.Figure()

    # Use scattergl for faster rendering when fast_render=True
    mode_type = "lines" if not fast_render else "lines+markers"
    fig.add_trace(go.Scattergl(x=df['timestamp'], y=df['price'], mode=mode_type, name=f'{coin_name} Price'))

    fig.update_layout(title=f'{coin_name} Price Trend',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      hovermode='x unified')
    return fig

# Example usage
if __name__ == "__main__":
    # Simulated historical data
    historical_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=30, freq='D'),
        'price': [40000 + i * 500 for i in range(30)]
    })
    chart = plot_historical_trend(historical_data, 'Bitcoin', fast_render=True)
    chart.show()