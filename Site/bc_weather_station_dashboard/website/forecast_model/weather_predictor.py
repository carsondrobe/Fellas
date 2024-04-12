# -*- coding: utf-8 -*-
"""Weather_Predictor.ipynb

Original file is located at
    https://colab.research.google.com/drive/1dwTHe1mXMGIXcYZ1IDiNDz9HIvENOUp-
We trained this model on a Google cloud computer, but moved the code here for grading

# 🤹‍♀️ Fellas
## Training notebook for weather predictor

### Gathering the data
"""

import pandas as pd
import numpy as np
from datetime import date, timedelta
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

"""Load the dataset:"""

days_to_get = 90

year = 2024
date_obj = date.today()
li = []
for _ in range(days_to_get):
    date_obj = date_obj - timedelta(days=1)
    date_str = date_obj.strftime('%Y-%m-%d')
    url = f'https://www.for.gov.bc.ca/ftp/HPR/external/!publish/BCWS_DATA_MART/{year}/{date_str}.csv'
    df = pd.read_csv(url, index_col=None, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)
df.head()

"""Convert Date time to 2 seperate columns:"""

df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format='%Y%m%d%H')
df['DATE'] = df['DATE_TIME'].dt.date
df['TIME'] = df['DATE_TIME'].dt.time
# df.drop(columns=['DATE_TIME'], inplace=True)
df.head()

df["HOURLY_TEMPERATURE"].plot()

"""Drop data not taken at noon:"""

df = df[df['TIME'] == pd.to_datetime('12:00:00').time()]
df.head()

"""Get station coords"""

station_data = pd.read_csv(
    "https://raw.githubusercontent.com/carsondrobe/Fellas/25501b33a408282b39b1fb4008311f9b81ac92c0/Site/bc_weather_station_dashboard/website/data/BC_Wildfire_Active_Weather_Stations.csv",
    index_col=None, header=0)
station_data.head()

df = pd.merge(df, station_data[['STATION_NAME', 'X', 'Y']], on='STATION_NAME', how='left')
df.head()

"""Drop Rows with nan data"""

columns_we_need = ['X', 'Y', 'HOURLY_PRECIPITATION', 'HOURLY_TEMPERATURE', 'HOURLY_RELATIVE_HUMIDITY',
                   'HOURLY_WIND_SPEED', 'HOURLY_WIND_DIRECTION', 'HOURLY_WIND_GUST', ]
df.dropna(subset=columns_we_need, inplace=True)
pd.isnull(df).any()

"""### Feature engineering

Wind direction and speed and gust to a vector:
"""

plt.hist2d(df['HOURLY_WIND_DIRECTION'], df['HOURLY_WIND_SPEED'], bins=(50, 50))
plt.colorbar()
plt.xlabel('Wind Direction [deg]')
plt.ylabel('Wind Velocity [m/s]')

wv = df.pop('HOURLY_WIND_SPEED')
max_wv = df.pop('HOURLY_WIND_GUST')

# Convert to radians.
wd_rad = df.pop('HOURLY_WIND_DIRECTION') * np.pi / 180

# Calculate the wind x and y components.
df['Wx'] = wv * np.cos(wd_rad)
df['Wy'] = wv * np.sin(wd_rad)

# Calculate the max wind x and y components.
df['max Wx'] = max_wv * np.cos(wd_rad)
df['max Wy'] = max_wv * np.sin(wd_rad)
columns_we_need += ['Wx', 'Wy', 'max Wx', 'max Wy']
columns_we_need.remove('HOURLY_WIND_SPEED')
columns_we_need.remove('HOURLY_WIND_GUST')
columns_we_need.remove('HOURLY_WIND_DIRECTION')
df.head()

plt.hist2d(df['Wx'], df['Wy'], bins=(50, 50))
plt.colorbar()
plt.xlabel('Wind X [m/s]')
plt.ylabel('Wind Y [m/s]')
ax = plt.gca()
ax.axis('tight')

"""Time data:"""

timestamp_s = df['DATE_TIME'].map(pd.Timestamp.timestamp)
day = 24 * 60 * 60
year = 365.2425 * day
df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
df.pop('TIME')
columns_we_need += ['Year sin', 'Year cos']
df.head()

"""### Splitting and normalization"""

features_df = df[columns_we_need]
features_df.head()

column_indices = {name: i for i, name in enumerate(features_df.columns)}

n = len(features_df)
train_df = features_df[0:int(n * 0.7)]
val_df = features_df[int(n * 0.7):int(n * 0.9)]
test_df = features_df[int(n * 0.9):]

num_features = features_df.shape[1]
train_df.head()

train_mean = train_df.mean()
train_std = train_df.std()

train_df = (train_df - train_mean) / train_std
val_df = (val_df - train_mean) / train_std
test_df = (test_df - train_mean) / train_std
train_df.head()


class WindowGenerator():
    def __init__(self, input_width, label_width, shift, train_df, val_df, test_df,
                 label_columns=None):
        # Store the raw dataframes
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

        # Work out the label column indices.
        if label_columns is not None:
            self.label_columns = label_columns
        elif label_columns is None:
            self.label_columns = None
        else:
            raise ValueError(f"label_columns: {label_columns} not found in df")

        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}
        self.column_indices = {name: i for i, name in enumerate(train_df.columns)}

        # Work out the window parameters.
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])

    def split_window(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_columns is not None:
            labels = tf.stack(
                [labels[:, :, self.column_indices[name]] for name in self.label_columns],
                axis=-1)

        # Slicing doesn't preserve static shape information, so set the shapes
        # manually. This way the `tf.data.Datasets` are easier to inspect.
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels

    def make_dataset(self, data):
        data = np.array(data, dtype=np.float32)
        ds = tf.keras.preprocessing.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=True,
            batch_size=1, )

        ds = ds.map(self.split_window)

        return ds

    def plot(self, model=None, plot_cols=['HOURLY_TEMPERATURE']):
        inputs, labels = self.example
        plt.figure(figsize=(12, 8))

        num_cols = len(plot_cols)
        plot_col_indices = [self.column_indices[col] for col in plot_cols]

        for i, plot_col_index in enumerate(plot_col_indices, start=1):
            plt.subplot(num_cols, 1, i)
            plt.ylabel(f'{plot_cols[i - 1]}')
            plt.plot(self.input_indices, inputs[0, :, plot_col_index],
                     label='Inputs', marker='.', zorder=-10)

            plt.scatter(self.label_indices, labels[0, :, plot_col_index],
                        edgecolors='k', label='Labels', c='#2ca02c', s=64)

            if model is not None:
                predictions = model(inputs)
                plt.scatter(self.label_indices, predictions[0, plot_col_index],
                            marker='X', edgecolors='k', label='Predictions',
                            c='#ff7f0e', s=64)

        plt.legend()
        plt.xlabel('Time [h]')

    @property
    def train(self):
        return self.make_dataset(self.train_df)

    @property
    def val(self):
        return self.make_dataset(self.val_df)

    @property
    def test(self):
        return self.make_dataset(self.test_df)

    @property
    def example(self):
        result = getattr(self, '_example', None)
        if result is None:
            # No example batch was found, so get one from the `.train` dataset
            result = next(iter(self.train))
            # And cache it for next time
            self._example = result
        return result


# Example usage:
# Assume train_df, val_df, and test_df are your pandas DataFrames containing time series data
# Define parameters for the window generator
input_width = 7  # Number of time steps to consider as input
label_width = 1  # Number of time steps to predict
shift = 1  # Number of time steps between input and label

# Create an instance of WindowGenerator
w_generator = WindowGenerator(input_width=input_width, label_width=label_width, shift=shift,
                              train_df=train_df, val_df=val_df, test_df=test_df,
                              label_columns=['HOURLY_TEMPERATURE'])
# Check the properties of the WindowGenerator
print(w_generator)

# Get the train, validation, and test datasets
train_ds = w_generator.train
val_ds = w_generator.val
test_ds = w_generator.test

for inputs, labels in w_generator.train.take(1):  # Take one batch
    if (pd.isnull(inputs).any()):
        for i in range(len(inputs)):
            if pd.isnull(inputs[i]).any():
                print(i, inputs[i])
    # print(f'Inputs shape (batch, time, features): {inputs.shape}')
    # print(f'Labels shape (batch, time, features): {labels.shape}')

"""### Baseline Model for Testing"""


def baseline_model(input_shape):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(units=1)
    ])
    return model


# Create an instance of the baseline model
baseline = baseline_model(input_shape=(w_generator.total_window_size,))

# Compile the model
baseline.compile(loss=tf.losses.MeanSquaredError(),
                 metrics=[tf.metrics.MeanAbsoluteError()])

# Train the model
history = baseline.fit(w_generator.train, epochs=10, validation_data=w_generator.val)

# Evaluate the model on the test dataset
loss, mae = baseline.evaluate(w_generator.test)
print("Test Loss:", loss)
print("Test MAE:", mae)


def plot_history(history):
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()


"""### Model"""

columns_to_predict = ['HOURLY_PRECIPITATION', 'HOURLY_TEMPERATURE', 'HOURLY_RELATIVE_HUMIDITY', 'Wx', 'Wy', 'max Wx',
                      'max Wy']
input_width = 7
label_width = 1
shift = 1
w_generator = WindowGenerator(input_width=input_width, label_width=label_width, shift=shift,
                              train_df=train_df, val_df=val_df, test_df=test_df,
                              label_columns=columns_to_predict)
print(w_generator)


def build_linear_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=input_shape),
        tf.keras.layers.Dense(units=7)  # 7 units because you want to predict 7 columns
    ])
    return model


# Build the linear model
linear_model = build_linear_model(input_shape=(7, 11))  # Assuming input width is 7 and there are 11 input columns

# Compile the model
linear_model.compile(optimizer='adam', loss='mse')  # Using Mean Squared Error as loss function

# Train the model
history = linear_model.fit(w_generator.train, epochs=10, validation_data=w_generator.val)

plot_history(history)

w_generator.plot(linear_model, plot_cols=['HOURLY_TEMPERATURE', 'HOURLY_RELATIVE_HUMIDITY', 'HOURLY_PRECIPITATION'])
# w_generator.plot(linear_model, plot_cols=['HOURLY_TEMPERATURE'])

"""predictions = predictions * train_std[columns] + train_mean[columns]

### Better model
"""

lstm_model = tf.keras.models.Sequential([
    # Shape [batch, time, features] => [batch, time, lstm_units]
    tf.keras.layers.LSTM(1, return_sequences=True),
    # Shape => [batch, time, features]
    tf.keras.layers.Dense(units=1)
])

print('Input shape:', w_generator.example[0].shape)
print('Output shape:', lstm_model(w_generator.example[0]).shape)


def compile_and_fit(model, window, epochs=10, patience=4, learning_rate=0.001):
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                      patience=patience,
                                                      mode='min')

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(loss=tf.keras.losses.MeanSquaredError(),
                  optimizer=optimizer,
                  metrics=[tf.keras.metrics.MeanAbsoluteError()])

    history = model.fit(window.train, epochs=epochs,
                        validation_data=window.val,
                        callbacks=[early_stopping])
    return history


history = compile_and_fit(lstm_model, w_generator)

val_performance = {}
performance = {}
val_performance['LSTM'] = lstm_model.evaluate(w_generator.val, return_dict=True)
performance['LSTM'] = lstm_model.evaluate(w_generator.test, verbose=0, return_dict=True)

plot_history(history)

w_generator.plot(lstm_model, plot_cols=['HOURLY_TEMPERATURE', 'HOURLY_RELATIVE_HUMIDITY', 'HOURLY_PRECIPITATION'])
# print(lstm_model(w_generator.example))

keras.utils.plot_model(lstm_model, show_shapes=True)

lstm_model.save("weather_predictor.h5")

new_model = tf.keras.models.load_model('weather_predictor.h5')

# Show the model architecture
new_model.summary()
