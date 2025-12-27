import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import json

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
    
    avg_correlation = correlation_matrix.where(
        np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
    ).mean().mean()

    # Convert to JSON-friendly format
    result = {
        "correlation_matrix": correlation_matrix.values.tolist(),
        "average_correlation": avg_correlation.item()
    }

    print(json.dumps(result))
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compute.py <ticker1> <ticker2> ... <tickerN>")
        sys.exit(1)
    
    tickers = []
    for arg in sys.argv[1:]:
        tickers.extend(arg.strip().upper().split(","))
    
    analyze_portfolio(tickers)