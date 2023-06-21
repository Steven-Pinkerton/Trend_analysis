import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
import os
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import time

def create_model(sequence_length, units_list=[50], dense_layers=1, activation='relu',
                 cell=LSTM, dropout=0.3, loss="mean_absolute_error", 
                 optimizer="rmsprop", bidirectional=False, output_units=1):
    model = Sequential()

    for i, units in enumerate(units_list):
        if i == 0:
            # first layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True if len(units_list) > 1 else False), 
                                        input_shape=(None, sequence_length)))
            else:
                model.add(cell(units, return_sequences=True if len(units_list) > 1 else False, 
                               input_shape=(None, sequence_length)))
        elif i == len(units_list) - 1:
            # last layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=False)))
            else:
                model.add(cell(units, return_sequences=False))
        else:
            # hidden layers
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True)))
            else:
                model.add(cell(units, return_sequences=True))
        # add dropout after each layer
        model.add(Dropout(dropout))

    for _ in range(dense_layers):
        model.add(Dense(units=output_units, activation=activation))

    model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)
    return model


def train(self, model, data, sequence_length=30, epochs=100):
    # Prepare the input and target sequences
    X = []
    y = []
    for i in range(sequence_length, len(data)):
        X.append(data[i-sequence_length:i])
        y.append(data[i])
    X = np.array(X)
    y = np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # Reshape for LSTM

    # Train the LSTM
    history = model.fit(X, y, epochs=epochs)

    return model, history

def predict_trends(self, model, data, sequence_length=30, num_days=30):
    # Prepare the input sequences
    inputs = np.array(data[-sequence_length:])
    inputs = np.reshape(inputs, (1, sequence_length, 1))  # Reshape for LSTM

    # Predict the sentiment scores for the next N days
    predictions = []
    for _ in range(num_days):
        prediction = model.predict(inputs)
        predictions.append(prediction[0,0])

        # Update the input sequence for the next prediction
        inputs = np.roll(inputs, -1)
        inputs[0, -1, 0] = prediction

    # Identify the trends based on the predicted sentiment scores
    trends = ['positive' if predictions[i] > predictions[i-1] else 'negative' for i in range(1, num_days)]

    return trends