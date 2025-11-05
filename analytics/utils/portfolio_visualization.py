import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


from .quotes_api import get_historic_data
from .portfolio_metrics import get_portfolio

from ..models import Portfolio

# ==========================================================================
# Display Individual Stock Prices
# ==========================================================================
def display_stocks(db, strategy_id, start_date, end_date, freq):
    portfolio = get_portfolio(db, strategy_id)

    portfolio_data = {}
    for ticker in portfolio.keys():
        portfolio_data[ticker] = get_historic_data(ticker, start_date, end_date, freq)["Close"]

    # Plotting stocks (ignore index) 
    plt.figure(figsize=(10, 5))
    for ticker, data in portfolio_data.items():
        plt.plot(data.index, data, label=ticker)
    
    # Formatting
    plt.title("Portfolio Stocks Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(False)
    plt.tight_layout()

    # plt.savefig("data/portfolio_plot.png")
    return portfolio_data

# ==========================================================================
# Display Portfolio Performance vs Index
# ==========================================================================
def display_portfolio(db, strategy_id, index, start_date, end_date, freq):
    portfolio = get_portfolio(db, strategy_id)
    index_data = get_historic_data(index, start_date, end_date, freq)["Close"]

    portfolio_df = pd.DataFrame(index=index_data.index)
    total_value_series = pd.Series(0, index=index_data.index)

    length = {}
    for ticker in portfolio.keys():
        stock_data = get_historic_data(ticker, start_date, end_date, freq)["Close"]
        stock_value = stock_data * portfolio[ticker]
        total_value_series += stock_value
        portfolio_df[ticker] = stock_value
        length[ticker] = len(stock_data)
        if length[ticker] < len(index_data):
            index_data = index_data[len(index_data) - length[ticker]:]

    # Check for data length mismatch
    if len(index_data) < len(total_value_series):
        new_date = index_data.index[0].strftime("%Y-%m-%d")
        culprit = [ticker for ticker in portfolio.keys() if length[ticker] < len(total_value_series)]
        raise ValueError(f"Data length mismatch for {culprit}. Hint: input start date later than {new_date}.")

    # Normalizing data
    portfolio_norm = total_value_series / total_value_series.iloc[0] * 100
    index_norm = index_data / index_data.iloc[0] * 100
    portfolio_df["total"] = total_value_series

    # Plotting index and portfolio average
    plt.figure(figsize=(10, 5))
    plt.plot(index_data.index, index_norm, label=index, color='black')
    plt.plot(index_data.index, portfolio_norm, label="Portfolio Average", color='blue')

    # Formatting
    plt.title("Portfolio Average vs Index Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(False)
    plt.tight_layout()

    # plt.savefig("data/portfolio_average_plot.png")
    return portfolio_df

# ==========================================================================
# Display Individual Stock Prices
# ==========================================================================
def display_stocks_plotly(db, strategy_id, start_date, end_date, freq):
    portfolio = get_portfolio(db, strategy_id)

    portfolio_data = {}
    for ticker in portfolio.keys():
        portfolio_data[ticker] = get_historic_data(ticker, start_date, end_date, freq)["Close"]

    # Create Plotly figure
    fig = go.Figure()
    for ticker, data in portfolio_data.items():
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data.values,
            mode="lines",
            name=ticker
        ))

    # Layout styling
    fig.update_layout(
        title="Portfolio Stocks Over Time",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        height=500,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Return HTML string to embed in Django
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html

# ==========================================================================
# Display Portfolio Performance vs Index
# ==========================================================================
def display_portfolio_plotly(db, strategy_id, index, start_date, end_date, freq):
    portfolio = get_portfolio(db, strategy_id)
    index_data = get_historic_data(index, start_date, end_date, freq)["Close"]

    portfolio_df = pd.DataFrame(index=index_data.index)
    total_value_series = pd.Series(0, index=index_data.index)

    length = {}
    for ticker in portfolio.keys():
        stock_data = get_historic_data(ticker, start_date, end_date, freq)["Close"]
        stock_value = stock_data * portfolio[ticker]
        total_value_series += stock_value
        portfolio_df[ticker] = stock_value
        length[ticker] = len(stock_data)
        if length[ticker] < len(index_data):
            index_data = index_data[len(index_data) - length[ticker]:]

    # Normalize data
    portfolio_norm = total_value_series / total_value_series.iloc[0] * 100
    index_norm = index_data / index_data.iloc[0] * 100

    # Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=index_data.index, y=index_norm, name=index, line=dict(color="gray")))
    fig.add_trace(go.Scatter(x=index_data.index, y=portfolio_norm, name="Portfolio", line=dict(color="blue")))

    fig.update_layout(
        title="Portfolio vs Index Over Time",
        xaxis_title="Date",
        yaxis_title="Normalized Value",
        template="plotly_dark",
        height=500,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    graph_html = pio.to_html(fig, full_html=False)
    return graph_html


# ========== Test ==========
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    db = get_db()
    strategy_id = 1
    start_date = "2020-09-30"
    end_date = "2023-01-01"
    index = "^GSPC"
    freq = "1d"
    display_stocks(db, strategy_id, start_date, end_date, freq)
    display_portfolio(db, strategy_id, index, start_date, end_date, freq)
    close_db(db)
