import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(df, text_column='headline'):
    """
    Analyzes the sentiment of the text in the specified column using VADER.
    Adds a 'sentiment_score' column to the DataFrame.
    """
    analyzer = SentimentIntensityAnalyzer()
    
    # Ensure the text column is string type
    df[text_column] = df[text_column].astype(str)
    
    # Apply VADER analyzer
    df['sentiment_score'] = df[text_column].apply(
        lambda x: analyzer.polarity_scores(x)['compound']
    )
    
    return df

def aggregate_sentiment(df, date_column='date', stock_column='stock'):
    """
    Aggregates sentiment scores by date and stock.
    Returns a DataFrame with dates as index and stocks as columns.
    """
    # Work on a copy to avoid chained assignment warnings downstream
    df = df.copy()
    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce', utc=True)
    
    # Drop rows with invalid dates and clone to avoid chained assignment warnings
    df = df.dropna(subset=[date_column]).copy()
    
    # Normalize to daily frequency in naive (timezone-free) datetime for consistent alignment
    df.loc[:, 'normalized_date'] = df[date_column].dt.tz_convert(None).dt.normalize()
    
    # Group by date and stock, calculating the mean sentiment
    daily_sentiment = df.groupby(['normalized_date', stock_column])['sentiment_score'].mean().reset_index()
    
    # Pivot the table: Index=Date, Columns=Stock, Values=Sentiment
    sentiment_pivot = daily_sentiment.pivot(index='normalized_date', columns=stock_column, values='sentiment_score')
    
    # Fill missing values with 0 (neutral) or forward fill? 
    # For correlation, maybe keep NaN or fill 0. Let's keep NaN for now to be safe, 
    # but usually 0 is a safe neutral assumption for missing news.
    # Let's fill with 0 for now as "no news is good news" or rather "neutral".
    sentiment_pivot = sentiment_pivot.fillna(0)
    
    return sentiment_pivot
