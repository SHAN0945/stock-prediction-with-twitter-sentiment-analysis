import yfinance as yf
import pandas as pd

def create_stock_csv(stock_name, start_date, end_date, output_filename='stock_data.csv'):
    """
    Fetches stock data (including Adjusted Close) and saves it to a CSV file.
    
    Parameters:
    - stock_name (str): Stock ticker symbol (e.g., 'AAPL').
    - start_date (str): Start date in 'YYYY-MM-DD' format.
    - end_date (str): End date in 'YYYY-MM-DD' format.
    - output_filename (str): Output CSV filename. Default: 'stock_data.csv'.
    
    Returns:
    - None (saves data to CSV).
    """
    try:
        # Fetch data with yfinance
        stock_data = yf.download(stock_name, start=start_date, end=end_date)
        
        # Check if data is empty
        if stock_data.empty:
            raise ValueError(f"No data found for {stock_name} between {start_date} and {end_date}.")
        
        # Reset index to include 'Date' as a column
        stock_data.reset_index(inplace=True)
        
        # Check if 'Adj Close' exists (fallback to 'Close' if missing)
        if 'Adj Close' not in stock_data.columns:
            print("Warning: 'Adj Close' column not found. Using 'Close' as a fallback.")
            stock_data['Adj Close'] = stock_data['Close']
        
        # Add 'Stock Name' column
        stock_data['Stock Name'] = stock_name
        
        # Define and reorder columns
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Stock Name']
        stock_data = stock_data[columns]
        
        # Save to CSV
        stock_data.to_csv(output_filename, index=False)
        print(f"Data saved to {output_filename}")
        
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
create_stock_csv('tsla', '2025-02-01', '2025-4-16', 'stock_data.csv')