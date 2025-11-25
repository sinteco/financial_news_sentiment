import yfinance as yf
import pandas as pd
from typing import Optional, List

def fetch_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch stock data (Open, High, Low, Close, Volume) from Yahoo Finance.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL')
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        
    Returns:
        DataFrame with stock data
    """
    print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    if df.empty:
        print(f"Warning: No data found for {ticker}")
        return df
        
    # Ensure columns are flat if multi-index (yfinance sometimes returns multi-index)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    # Ensure we have the required columns
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"Warning: Missing columns {missing} for {ticker}")
        
    return df

def batch_fetch_stock_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch data for multiple tickers and combine them.
    """
    all_data = {}
    for t in tickers:
        df = fetch_stock_data(t, start_date, end_date)
        if not df.empty:
            all_data[t] = df
            
    return all_data

def load_stock_csv(path: str) -> pd.DataFrame:
    """
    Load stock data from a CSV file.
    Expects columns: Date, Open, High, Low, Close, Volume
    """
    print(f"Loading data from {path}...")
    try:
        df = pd.read_csv(path, parse_dates=['Date'], index_col='Date')
        
        # Ensure we have the required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        # Check if columns exist (case-insensitive check might be safer, but let's assume standard format first)
        
        return df
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return pd.DataFrame()
