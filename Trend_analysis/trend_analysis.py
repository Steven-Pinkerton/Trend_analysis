from lstm.lstm_trend_identification import LSTM
from time_series import convert_to_time_series, resample_data, handle_missing_values, handle_outliers
from event_identification.event_identification import EventIdentifier

class TrendAnalyzer:
    def __init__(self, sentiment_data, date_format=None, resample_freq=None, handle_missing_method='ffill', handle_outliers_method='median', outliers_threshold=3):
        # Preprocess the sentiment data
        self.data = convert_to_time_series(sentiment_data, date_format)
        if resample_freq:
            self.data = resample_data(self.data, 'sentiment_score', resample_freq)
        self.data = handle_missing_values(self.data, handle_missing_method)
        self.data = handle_outliers(self.data, handle_outliers_method, outliers_threshold)

    # Existing methods...

    def identify_events(self, freq='H', threshold=50, keywords=[], window=3, z_threshold=2, contamination=0.01):
        """
        Identify events in the sentiment data using various methods.

        Parameters:
        freq : str
            The frequency to use for resampling the data.
        threshold : int
            The threshold to use for detecting high volume periods and keyword bursts.
        keywords : list of str
            The keywords to look for in detecting keyword bursts.
        window : int
            The window size to use for calculating rolling sentiment trends.
        z_threshold : float
            The z-score threshold to use for detecting outliers.
        contamination : float
            The contamination factor to use for detecting anomalies with Isolation Forest.
        """
        event_identifier = EventIdentifier(self.data)
        event_identifier.group_by_time(freq)
        event_identifier.detect_high_volume_periods(freq, threshold)
        event_identifier.detect_keyword_bursts(keywords, freq, threshold)
        event_identifier.detect_rolling_trends(window)
        event_identifier.detect_outliers(z_threshold)
        event_identifier.detect_anomalies(contamination)

        self.events = event_identifier.data
        return self.events
    
    def estimate_trend_strength(self):
        """
        Estimate the strength of identified trends.
        Returns:
        trend_strength : list of float
            The calculated slope of the trends identified in sentiment data.
        """
        # calculate the slope of the trend line
        trend_slope = np.diff(self.trends) / np.diff(self.data['timestamp'])
        # return the absolute value of the slope as the trend strength
        return abs(trend_slope)

    def detect_trend_changes(self):
        """
        Detect changes in identified trends.
        Returns:
        trend_change : list of int
            The indices in self.data['timestamp'] where the trend changes.
        """
        # calculate the second derivative of the trend line
        second_derivative = np.diff(self.trends, n=2)
        # find indices where the second derivative is close to zero (indicating a change in trend)
        trend_change_indices = argrelextrema(second_derivative, np.isclose, atol=1e-5)
        # convert these indices to corresponding timestamps
        trend_change = self.data['timestamp'][trend_change_indices]
        return trend_change
    
    
    def weighted_average_trends(self, weights):
        """
        Calculate the weighted average of the trends identified by the different methods.

        Parameters:
        weights : dict
            A dictionary mapping methods to their weights. The keys of the dictionary should be the same as the ones used in the identify_trends method, and the values should be the weights (which should sum to 1).

        Returns:
        weighted_average_trends : pandas Series or DataFrame
            The weighted average of the trends identified by the different methods.
        """
        # Check if the weights sum to 1
        if not np.isclose(sum(weights.values()), 1, atol=1e-5):
            raise ValueError("The sum of the weights should be 1.")
        
        weighted_trends = None

        for method, weight in weights.items():
            trends = self.identify_trends(method)
            if weighted_trends is None:
                weighted_trends = trends * weight
            else:
                weighted_trends += trends * weight

        return weighted_trends