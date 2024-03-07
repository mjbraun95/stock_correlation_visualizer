import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def fetch_data(tickers):
    """
    Fetches historical stock prices for the given tickers.
    """
    data = yf.download(tickers, start="2023-01-01", end="2024-01-01")['Adj Close']
    return data

def compute_returns(data):
    """
    Computes daily returns for the stock prices.
    """
    daily_returns = data.pct_change()
    return daily_returns

def plot_correlation_matrix(daily_returns):
    """
    Plots the correlation matrix of the daily returns.
    """
    correlation_matrix = daily_returns.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Matrix of Stock Returns')
    plt.show()

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]  # Example tickers
    data = fetch_data(tickers)
    daily_returns = compute_returns(data)
    plot_correlation_matrix(daily_returns)
