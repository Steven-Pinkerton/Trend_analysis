from lstm.lstm_trend_identification import LSTM
from time_series.trend_identification import decompose_time_series, apply_exponential_smoothing, apply_prophet

class TrendAnalyzer:
    def __init__(self, sentiment_data):
        self.data = sentiment_data

    def identify_trends(self, method='lstm'):
        """
        Identify trends in the sentiment data using the specified method.

        Parameters:
        method : str
            The method to use for trend identification. Options are 'lstm', 'decompose', 'exponential_smoothing', and 'prophet'.
        """
        if method == 'lstm':
            trend_identifier = LSTM(self.data)
            self.trends = trend_identifier.predict_trends()  # Assumes you add a predict_trends method to your LSTM class
        elif method == 'decompose':
            self.trends = decompose_time_series(self.data['sentiment_score'])
        elif method == 'exponential_smoothing':
            self.trends = apply_exponential_smoothing(self.data['sentiment_score'])
        elif method == 'prophet':
            df = self.data[['timestamp', 'sentiment_score']]
            df.columns = ['ds', 'y']
            forecast = apply_prophet(df)
            self.trends = forecast['yhat']  # The forecasted values
        else:
            raise ValueError(f"Invalid method: {method}. Options are 'lstm', 'decompose', 'exponential_smoothing', and 'prophet'.")

        return self.trends
    
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
        weighted_trends = None

        for method, weight in weights.items():
            trends = self.identify_trends(method)
            if weighted_trends is None:
                weighted_trends = trends * weight
            else:
                weighted_trends += trends * weight

        return weighted_trends
    
    
    