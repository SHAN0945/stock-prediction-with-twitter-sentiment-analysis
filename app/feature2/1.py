import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_stock_data(tickers, years=5):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=years * 365)
    adj_close_df = pd.DataFrame()
    
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        adj_close_df[ticker] = data['Close']
    
    return adj_close_df.dropna()

def analyze_portfolio(tickers):
    stock_data = get_stock_data(tickers)
    log_returns = np.log(stock_data / stock_data.shift(1)).dropna()
    correlation_matrix = log_returns.corr()
    
    avg_correlation = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)).mean().mean()
    
    print("Portfolio Analysis Report:")
    print("--------------------------------------------------")
    print("Correlation Matrix:")
    print(correlation_matrix)
    print("--------------------------------------------------")
    print(f"Average Correlation: {avg_correlation:.4f}")
    
    threshold = 0.7  # Define a threshold for correlationG
    if avg_correlation > threshold:
        print("Your portfolio is highly correlated. Consider diversifying into other sectors or asset classes.")
    else:
        print("Your portfolio is well-diversified!")
    
# User Input
tickers = input("Enter stock tickers separated by commas: ").upper().split(',')
analyze_portfolio([ticker.strip() for ticker in tickers])
