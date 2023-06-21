import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from sklearn.preprocessing import MinMaxScaler


def difference(data: pd.DataFrame, column: str, interval: int = 1) -> pd.DataFrame:
    if column not in data.columns:
        raise ValueError(f"Column {column} not in DataFrame.")
    data[column] = data[column].diff(interval)
    data.dropna(inplace=True)  # First row will be NaN, so drop it
    return data


def plot_series(time_series, title='Sentiment Score'):
    plt.figure(figsize=(10,6))
    plt.plot(time_series, label='Sentiment Score')
    plt.title(title)
    plt.legend(loc='best')
    plt.show()
    
def test_stationarity(time_series):
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(time_series, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    return dfoutput
    
def normalize_series(train_series, test_series=None):
    scaler = MinMaxScaler(feature_range=(-1, 1))
    normalized_train_series = scaler.fit_transform(train_series.values.reshape(-1, 1))
    normalized_test_series = scaler.transform(test_series.values.reshape(-1, 1)) if test_series is not None else None
    return normalized_train_series, normalized_test_series, scaler

def train_test_split(series, test_size=0.2, random_state=None):
    if random_state is not None:
        train_series, test_series = train_test_split(series, test_size=test_size, random_state=random_state)
    else:
        split_point = int(len(series) * (1 - test_size))
        train_series = series[:split_point]
        test_series = series[split_point:]
    return train_series, test_series


def create_sequences(data, seq_length):
    data = np.array(data)
    stride = data.strides[0]
    sequences = stride_tricks.as_strided(data, shape=(len(data) - seq_length, seq_length), strides=(stride, stride))
    return sequences[:-1], data[seq_length:]
    return np.array(xs), np.array(ys)

def fill_missing_values(data):
    data.fillna(method='bfill', inplace=True)
    return data