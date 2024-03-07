import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# New function to save tickers to a file
def save_tickers_to_file(tickers, filename="tickers.txt"):
    with open(filename, "w") as f:
        for ticker in tickers:
            f.write(ticker + "\n")

# New function to load tickers from a file
def load_tickers_from_file(filename="tickers.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def fetch_data(tickers, start_date, end_date="2024-01-01"):
    """
    Fetches historical stock prices for the given tickers within the specified date range.
    """
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def validate_and_clean_tickers(tickers):
    """
    Validates tickers by checking if they are accessible via yfinance. 
    Removes invalid tickers and returns a list of valid tickers.
    """
    valid_tickers = []
    for ticker in tickers:
        data = yf.Ticker(ticker)
        if data.history(period="1d").empty:
            print(f"Ticker {ticker} is not accessible or does not exist. Removing from the list.")
        else:
            valid_tickers.append(ticker)
    return valid_tickers

def validate_tickers(tickers):
    """
    Validates each ticker by attempting to fetch data for it.
    Returns a list of valid tickers.
    """
    valid_tickers = []
    for ticker in tickers:
        data = yf.Ticker(ticker)
        if data.history(period="1d").empty:
            print(f"Ticker {ticker} is not accessible or does not exist.")
        else:
            valid_tickers.append(ticker)
    return valid_tickers

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

def get_timeframe():
    """
    Asks the user for a timeframe and returns the start date for data fetching.
    """
    timeframe_map = {
        "1y": "1y",
        "6m": "6m",
        "3m": "3m",
        "1m": "1m",
        "": "max"
    }
    while True:
        timeframe = input("Enter the timeframe (1y, 6m, 3m, 1m) or press Enter for all time: ").lower()
        if timeframe in timeframe_map:
            return timeframe_map[timeframe]
        else:
            print("Invalid timeframe. Please try again.")

if __name__ == "__main__":
    continue_analysis = True
    
    # Ask user if they want to load previous tickers
    load_previous = input("Do you want to load previous tickers? (yes/no): ").strip().lower() == "yes"
    tickers = load_tickers_from_file() if load_previous else []

    while continue_analysis:
        if tickers:
            print("Previously entered tickers: ", tickers)
        print("Enter stock tickers, one per line. Enter a blank line to finish.")
        
        # Enter new tickers
        while True:
            ticker = input()
            if ticker == "":
                break
            if ticker.strip() not in tickers:
                tickers.append(ticker.strip())
        
        # Validate tickers
        tickers = validate_and_clean_tickers(tickers)
        
        # Ensure there are at least two valid tickers
        if len(tickers) < 2:
            print("At least two valid tickers are required for correlation analysis.")
            continue  # Skip the rest of the loop and start over
        
        # Save updated list of tickers
        save_tickers_to_file(tickers)

        # Proceed with analysis
        timeframe = get_timeframe()
        end_date = datetime.now()
        if timeframe != "max":
            if timeframe == "1y":
                start_date = end_date - timedelta(weeks=52)
            elif timeframe == "6m":
                start_date = end_date - timedelta(weeks=26)
            elif timeframe == "3m":
                start_date = end_date - timedelta(weeks=13)
            elif timeframe == "1m":
                start_date = end_date - timedelta(weeks=4)
            start_date = start_date.strftime("%Y-%m-%d")  # Format here if not "max"
        else:
            start_date = "1900-01-01"

        data = fetch_data(tickers, start_date=start_date, end_date=end_date.strftime("%Y-%m-%d"))
        daily_returns = compute_returns(data)
        plot_correlation_matrix(daily_returns)
        
        # Ask user if they want to continue after closing the plot
        continue_analysis = input("Do you want to modify tickers and re-analyze? (yes/no): ").strip().lower() == "yes"