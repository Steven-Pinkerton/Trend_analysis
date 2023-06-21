class EventIdentifier:
    def __init__(self, sentiment_data, neg_weight=1.5):
        """
        sentiment_data: pandas DataFrame, expects columns 'timestamp' and 'sentiment_score'
        """
        self.data = pd.DataFrame(sentiment_data)
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data.set_index('timestamp', inplace=True)
        self.data['weighted_sentiment'] = np.where(self.data['sentiment_score'] < 0, self.data['sentiment_score'] * neg_weight, self.data['sentiment_score'])

    def group_by_time(self, freq='H'):
        self.data = self.data.resample(freq)['weighted_sentiment'].mean().reset_index()
        return self.data

    def detect_high_volume_periods(self, freq='H', threshold=50):
        post_counts = self.data.resample(freq).size()
        self.data['high_volume'] = post_counts > threshold
        return self.data

    def detect_keyword_bursts(self, keywords, freq='H', threshold=5):
        if 'keywords' in self.data.columns:
            keyword_counts = self.data[self.data['keywords'].apply(lambda x: any(keyword in x for keyword in keywords))].resample(freq).size()
            self.data['keyword_burst'] = keyword_counts > threshold
        return self.data

    def detect_rolling_trends(self, window=3):
        self.data['rolling_sentiment'] = self.data['sentiment_score'].rolling(window=window).mean()
        return self.data

    def detect_outliers(self, z_threshold=2):
        z_scores = np.abs(stats.zscore(self.data['weighted_sentiment']))
        self.data['is_outlier'] = z_scores > z_threshold
        return self.data

    def detect_change_points(self, threshold=0.05):
        mean_val = np.mean(self.data['sentiment_score'])
        self.data['cusum'] = np.cumsum(self.data['sentiment_score'] - mean_val)
        self.data['change_point'] = np.abs(self.data['cusum']) > threshold
        return self.data

    def detect_anomalies(self, contamination=0.01):
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        sentiment_score_scaled = scaler.fit_transform(self.data[['sentiment_score']])
        
        clf = IsolationForest(contamination=contamination)
        preds = clf.fit_predict(sentiment_score_scaled)
        self.data['is_anomaly'] = preds == -1
        return self.data