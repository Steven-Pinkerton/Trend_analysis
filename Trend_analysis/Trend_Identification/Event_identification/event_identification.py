class EventIdentifier:
    def __init__(self, sentiment_data, neg_weight=1.5):
        self.data = pd.DataFrame(sentiment_data)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data.set_index('timestamp', inplace=True)
        # Apply weighting to negative sentiment scores
        self.data['weighted_sentiment'] = np.where(self.data['sentiment_score'] < 0, self.data['sentiment_score'] * neg_weight, self.data['sentiment_score'])

    def group_by_time(self, freq='H'):
        # Group by time periods and compute the mean sentiment score for each period
        self.data = self.data.resample(freq)['weighted_sentiment'].mean().reset_index()
        return self.data

    def detect_high_volume_periods(self, threshold=50):
        # Group by time periods and count the number of posts in each period
        post_counts = self.data.resample('H').size()
        # Identify high volume periods
        self.data['high_volume'] = post_counts > threshold
        return self.data

    def detect_keyword_bursts(self, keywords, threshold=5):
        # Compute the number of keyword occurrences in each time period
        keyword_counts = self.data[self.data['keywords'].apply(lambda x: any(keyword in x for keyword in keywords))].resample('H').size()
        # Identify periods with high keyword occurrences
        self.data['keyword_burst'] = keyword_counts > threshold
        return self.data

    def detect_rolling_trends(self, window=3):
        # Compute the rolling average sentiment score
        self.data['rolling_sentiment'] = self.data['sentiment_score'].rolling(window=window).mean()
        return self.data

    def detect_outliers(self, z_threshold=2):
        # Compute z-scores of the sentiment scores
        z_scores = np.abs(stats.zscore(self.data['sentiment_score']))
        # Identify outliers
        self.data['is_outlier'] = z_scores > z_threshold
        return self.data

    def detect_change_points(self, threshold=0.05):
        # Compute the mean sentiment score
        mean_val = np.mean(self.data['sentiment_score'])
        # Compute the cumulative sum of the differences from the mean
        self.data['cusum'] = np.cumsum(self.data['sentiment_score'] - mean_val)
        # Identify change points
        self.data['change_point'] = np.abs(self.data['cusum']) > threshold
        return self.data

    def detect_anomalies(self, contamination=0.01):
        # Initialize the Isolation Forest
        clf = IsolationForest(contamination=contamination)
        # Fit the model and get the predictions
        preds = clf.fit_predict(self.data[['sentiment_score']])
        # Identify anomalies
        self.data['is_anomaly'] = preds == -1
        return self.data