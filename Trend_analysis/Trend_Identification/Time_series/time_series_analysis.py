import pandas as pd
import numpy as np

def convert_to_time_series(df, date_format=None):
    """
    Convert a DataFrame into a time series format.

    Parameters:
    df (pandas.DataFrame): The DataFrame to convert.
    date_format (str): The date format to use for conversion.

    Returns:
    pandas.DataFrame: The converted DataFrame.
    """
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format=date_format)
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
    except Exception as e:
        print("Error during conversion to time series:", e)
        return None
    
    return df

def resample_data(data, column, freq):
    resampled_data = data[column].resample(freq).mean()
    return resampled_data

def handle_missing_values(data, method='ffill'):
    data.fillna(method=method, inplace=True)
    return data

def handle_outliers(data, method='median', threshold=3):
    """
    Detect and handle outliers in the data.

    Parameters:
    data (pandas.DataFrame or pandas.Series): The data to process.
    method (str): The method to use for outlier handling - 'mean', 'median', or 'remove'.
    threshold (float): The modified z-score threshold to use for detecting outliers.

    Returns:
    pandas.DataFrame or pandas.Series: The processed data.
    """
    if method not in ['mean', 'median', 'remove']:
        raise ValueError("Invalid method. Expected 'mean', 'median', or 'remove'.")

    median = data.median()
    median_absolute_deviation = np.median(np.abs(data - median))
    modified_z_scores = 0.6745 * (data - median) / median_absolute_deviation

    if method == 'mean':
        data[modified_z_scores > threshold] = data.mean()
    elif method == 'median':
        data[modified_z_scores > threshold] = data.median()
    elif method == 'remove':
        data = data[modified_z_scores <= threshold]

    return data