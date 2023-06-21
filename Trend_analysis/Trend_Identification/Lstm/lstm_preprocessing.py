import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from sklearn.preprocessing import MinMaxScaler


def difference(data: pd.DataFrame, column: str, interval: int = 1) -> pd.DataFrame:
    """
    Make a DataFrame time series stationary by differencing.

    :param data: DataFrame containing the time series data
    :param column: Name of the time series column
    :param interval: Differencing interval, default is 1
    :returns: DataFrame with the differenced time series
    """
    data[column] = data[column].diff(interval)
    data.dropna(inplace=True)  # First row will be NaN, so drop it
    return data

def plot_series(time_series):
    plt.figure(figsize=(10,6))
    plt.plot(time_series, label='Sentiment Score')
    plt.legend(loc='best')
    plt.show()
    
def test_stationarity(time_series):
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(time_series, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    
def normalize_series(series):
    scaler = MinMaxScaler(feature_range=(-1, 1))
    normalized_series = scaler.fit_transform(series.values.reshape(-1, 1))
    return normalized_series, scaler

def train_test_split(series, test_size=0.2):
    split_point = int(len(series) * (1 - test_size))
    train = series[:split_point]
    test = series[split_point:]
    return train, test

def create_sequences(data, seq_length):
    xs = []
    ys = []

    for i in range(len(data)-seq_length-1):
        x = data[i:(i+seq_length)]
        y = data[i+seq_length]
        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)

def fill_missing_values(data):
    data.fillna(method='bfill', inplace=True)
    return data