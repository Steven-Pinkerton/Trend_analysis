import pandas as pd

def aggregate_sentiments(df, freq='H'):
    """
    Aggregate sentiment scores over a specific frequency.

    Parameters:
    df : pandas DataFrame
        The input data with columns including 'timestamp' and 'sentiment_score'.
    freq : str
        The frequency at which to aggregate the sentiment scores. Default is 'D' for daily.

    Returns:
    df_aggregated : pandas DataFrame
        The input data aggregated over the specified frequency.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Aggregate the sentiment scores
    df_aggregated = df.resample(freq).mean()

    # Count positive and negative sentiments in each period
    df_pos = df[df['sentiment'] == 'positive'].resample(freq).count()
    df_neg = df[df['sentiment'] == 'negative'].resample(freq).count()

    df_aggregated['positive_sentiment_count'] = df_pos['sentiment']
    df_aggregated['negative_sentiment_count'] = df_neg['sentiment']

    return df_aggregated