import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from fbprophet import Prophet

def decompose_time_series(time_series, model='additive', freq=7):
    """
    Decompose a time series using statsmodels's seasonal_decompose function.

    Parameters:
    time_series: The time series to decompose.
    model: The model to use for decomposition - 'additive' or 'multiplicative'.
    freq: The frequency of the seasonality component.

    Returns:
    The decomposed time series, which includes the trend, seasonal, and residual components.
    """

    # Convert the time series to a Pandas Series if it isn't already
    if not isinstance(time_series, pd.Series):
        time_series = pd.Series(time_series)

    # Decompose the time series
    decomposed = seasonal_decompose(time_series, model=model, freq=freq)

    return decomposed

def apply_exponential_smoothing(series, trend=None, seasonal=None, damping_trend=None, damping_seasonal=None):
    # First, we convert the series to a pandas Series (if it's not already), 
    # as the ExponentialSmoothing class works with pandas Series.
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    # Then, we fit the ExponentialSmoothing model to our data.
    model = ExponentialSmoothing(series, trend=trend, seasonal=seasonal,
                                 damped_trend=damping_trend, damped_seasonal=damping_seasonal)
    model_fit = model.fit()

    # Finally, we return the smoothed series.
    return model_fit.fittedvalues

def apply_prophet(df, periods=30):
    # Prophet requires a DataFrame with two columns: 'ds' and 'y'
    # 'ds' is the date column and should be of datetime type
    # 'y' is the value you want to forecast
    
    # Instantiate a new Prophet object
    model = Prophet()

    # Fit the Prophet model to your data
    model.fit(df)

    # Make a future DataFrame for prediction
    future = model.make_future_dataframe(periods=periods) # forecast for the next given periods

    # Use the model to make a forecast
    forecast = model.predict(future)

    # 'forecast' is now a DataFrame that includes a column 'yhat' with the forecasted values
    # Other useful columns include 'yhat_lower' and 'yhat_upper', which provide uncertainty intervals for the forecast

    return forecast