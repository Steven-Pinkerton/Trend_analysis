class CorrelationAnalyzer:
    def __init__(self, df, window_size=24, method='spearman', fill_method=None):
        self.df = df
        self.window_size = window_size
        self.method = method
        self.fill_method = fill_method

    def calculate_rolling_correlation(self):
        """
        Calculate the rolling correlation between changes in sentiment and changes in stock prices.

        Returns:
        rolling_correlation : pandas Series
            The rolling correlation between changes in sentiment and changes in stock prices.
        """
        # Check for the required columns
        for column in ['sentiment_score', 'stock_price']:
            if column not in self.df.columns:
                raise ValueError(f"The DataFrame is missing the required column: {column}")

        # Handle missing data
        if self.fill_method is not None:
            if self.fill_method == 'bfill':
                self.df = self.df.bfill()
            elif self.fill_method == 'ffill':
                self.df = self.df.ffill()
            elif self.fill_method == 'interpolate':
                self.df = self.df.interpolate()
            else:
                raise ValueError("Invalid fill_method. Options are 'bfill', 'ffill', and 'interpolate'.")
        else:
            # Drop any rows with missing data
            self.df = self.df.dropna(subset=['sentiment_score', 'stock_price'])

        rolling_correlation = self.df['sentiment_score'].rolling(self.window_size).corr(self.df['stock_price'], method=self.method)
        return rolling_correlation