import pandas as pd
import talib
import pynance as pn
from typing import Dict

def apply_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply TA-Lib indicators to the stock dataframe.
    Adds: SMA_20, RSI_14, MACD, MACD_signal, MACD_hist
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Ensure Close is float
    close_prices = df['Close'].values.astype(float)
    
    # Simple Moving Average (SMA)
    df['SMA_20'] = talib.SMA(close_prices, timeperiod=20)
    
    # Relative Strength Index (RSI)
    df['RSI_14'] = talib.RSI(close_prices, timeperiod=14)
    
    # MACD
    macd, macd_signal, macd_hist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = macd
    df['MACD_signal'] = macd_signal
    df['MACD_hist'] = macd_hist
    
    return df

def calculate_financial_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate financial metrics using PyNance (or manual calculation if PyNance is limited).
    Note: PyNance is quite old, so we might rely on pandas for some metrics if pynance fails.
    """
    metrics = {}
    
    if df.empty:
        return metrics
        
    # Daily Returns
    # pynance has data.return_relative but simple pandas pct_change is robust
    returns = df['Close'].pct_change().dropna()
    
    metrics['volatility'] = returns.std() * (252 ** 0.5) # Annualized volatility
    metrics['cumulative_return'] = (1 + returns).prod() - 1
    metrics['max_drawdown'] = (df['Close'] / df['Close'].cummax() - 1).min()
    
    # Try using pynance for something specific if possible, 
    # but standard metrics are often better done directly in pandas for control.
    # Example: pynance.tech.sma is redundant with talib.
    
    return metrics
