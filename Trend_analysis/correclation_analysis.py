import pandas as pd

def calculate_rolling_correlation(df, window_size=24, method='pearson'):
    """
    Calculate the rolling correlation between changes in sentiment and changes in stock prices.

    Parameters:
    df : pandas DataFrame
        The input data with columns including 'sentiment_score' and 'stock_price'.
    window_size : int
        The size of the rolling window to use for calculating correlation.
    method : str
        The correlation method to use ('pearson', 'kendall', 'spearman').

    Returns:
    rolling_correlation : pandas Series
        The rolling correlation between changes in sentiment and changes in stock prices.
    """
    # Drop any rows with missing data
    df = df.dropna(subset=['sentiment_score', 'stock_price'])

    rolling_correlation = df['sentiment_score'].rolling(window_size).corr(df['stock_price'], method=method)
    return rolling_correlation