import numpy as np
import pandas as pd
from scipy import stats

class StatisticalAnalyzer:
    def __init__(self, sentiment_data):
        self.data = pd.DataFrame(sentiment_data)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data.set_index('timestamp', inplace=True)

    def moving_average(self, window_size):
        """
        Calculate the moving average of the sentiment scores.

        Parameters:
        window_size : int
            The size of the window to use for calculating the moving average.

        Returns:
        moving_average : pandas Series
            The moving average of the sentiment scores.
        """
        return self.data['sentiment_score'].rolling(window_size, freq='H').mean()

    def z_scores(self):
        """
        Calculate the z-scores of the sentiment scores.

        Returns:
        z_scores : pandas Series
            The z-scores of the sentiment scores.
        """
        return pd.Series(stats.zscore(self.data['sentiment_score']), index=self.data.index)

    def standard_deviation(self, window_size):
        """
        Calculate the standard deviation of the sentiment scores over a window.

        Parameters:
        window_size : int
            The size of the window to use for calculating the standard deviation.

        Returns:
        standard_deviation : pandas Series
            The standard deviation of the sentiment scores over the window.
        """
        return self.data['sentiment_score'].rolling(window_size, freq='H').std()