import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List

def analyze_sentiment(df: pd.DataFrame, text_column: str = 'headline') -> pd.DataFrame:
    """
    Analyze sentiment of the text column using VADER.
    Adds 'sentiment_score' column to the DataFrame.
    """
    analyzer = SentimentIntensityAnalyzer()
    
    # Ensure text column is string
    df[text_column] = df[text_column].astype(str)
    
    # Calculate sentiment
    # Compound score is usually best for a single metric (-1 to 1)
    df['sentiment_score'] = df[text_column].apply(lambda x: analyzer.polarity_scores(x)['compound'])
    
    return df

def aggregate_sentiment(df: pd.DataFrame, date_column: str = 'date', stock_column: str = 'stock') -> pd.DataFrame:
    """
    Aggregate sentiment scores by date and stock.
    Returns a DataFrame with Date index and columns for each stock's daily sentiment.
    """
    # Ensure date is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        # Try parsing with mixed format support or coerce errors
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce', utc=True).dt.date
    else:
        df[date_column] = df[date_column].dt.date
        
    # Drop rows with invalid dates
    df = df.dropna(subset=[date_column])
        
    # Group by date and stock, then mean
    daily_sentiment = df.groupby([date_column, stock_column])['sentiment_score'].mean().reset_index()
    
    # Pivot to have stocks as columns
    pivot_df = daily_sentiment.pivot(index=date_column, columns=stock_column, values='sentiment_score')
    
    return pivot_df
