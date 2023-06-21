import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
import os
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import time

def create_model(sequence_length, units=50, cell=LSTM, n_layers=2, dropout=0.3,
                 loss="mean_absolute_error", optimizer="rmsprop", bidirectional=False, output_units=1):
    model = Sequential()

    for i in range(n_layers):
        if i == 0:
            # first layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True), input_shape=(None, sequence_length)))
            else:
                model.add(cell(units, return_sequences=True, input_shape=(None, sequence_length)))
        elif i == n_layers - 1:
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
        
    model.add(Dense(units=output_units))
    
    model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)
    return model

def train(self, data, sequence_length=30, epochs=100):
        """
        Train the LSTM on the provided data.

        Parameters:
        data : array-like
            The input data, which should be a 1D array or list of sentiment scores.
        sequence_length : int
            The length of the sequences to use for training the LSTM.
        epochs : int
            The number of epochs to train for.
        """
        # Convert the data to a PyTorch tensor
        data = torch.tensor(data, dtype=torch.float)

        # Prepare the input and target sequences
        inputs = []
        targets = []
        for i in range(len(data) - sequence_length):
            inputs.append(data[i:i+sequence_length])
            targets.append(data[i+sequence_length])
        inputs = torch.stack(inputs)
        targets = torch.tensor(targets, dtype=torch.float)

        # Create the optimizer
        optimizer = optim.Adam(self.parameters())

        # Train the LSTM
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self(inputs)
            loss = torch.mean((outputs - targets) ** 2)
            loss.backward()
            optimizer.step()

def predict_trends(self, data, sequence_length=30, num_days=30):
        """
        Predict trends in the sentiment scores for the next N days.

        Parameters:
        data : array-like
            The input data, which should be a 1D array or list of sentiment scores.
        sequence_length : int
            The length of the sequences to use for training the LSTM.
        num_days : int
            The number of days to predict sentiment scores for.

        Returns:
        trends : list of str
            The predicted trends for the next N days, where each trend is either 'positive' or 'negative'.
        """
        # Convert the data to a PyTorch tensor
        data = torch.tensor(data, dtype=torch.float)

        # Prepare the input sequences
        inputs = [data[-sequence_length:]]
        inputs = torch.stack(inputs)

        # Predict the sentiment scores for the next N days
        predictions = []
        for _ in range(num_days):
            prediction = self(inputs)
            predictions.append(prediction.item())

            # Update the input sequence for the next prediction
            inputs = torch.cat((inputs[0, 1:], prediction)).unsqueeze(0)

        # Identify the trends based on the predicted sentiment scores
        trends = ['positive' if predictions[i] > predictions[i-1] else 'negative' for i in range(1, num_days)]

        return trends