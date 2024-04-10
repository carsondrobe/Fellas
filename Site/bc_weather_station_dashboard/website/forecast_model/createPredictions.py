import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import base64
import urllib.parse
from django.http import JsonResponse
import os
from scipy.interpolate import make_interp_spline

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging
import tensorflow as tf
from tensorflow import keras
import datetime
from ..models import StationData, WeatherStation
from django.conf import settings

loaded_model = keras.models.load_model('website/forecast_model/weather_predictor.h5')
response = None

# Receives request from view_predictions.js
# This function generates a plot
# and returns the URI of the plot to the frontend. Essentially passing back an encoded image
# to the frontend.


def create_predictions(request):
    global response
    if response is not None:
        return response
    matplotlib.use("agg")  # IMPORTANT for Django to use matplotlib

    data_points = get_data_points(request)[1]
    temperature_data = data_points[:-1]
    prediction = data_points[-1]

    days_of_week = get_days_of_week(datetime.datetime.now().date(), len(temperature_data) - 1)
    days_of_week.append('Today')
    days_of_week.append('Tomorrow')

    # Generate more points for smooth curve
    x_original = np.arange(len(temperature_data))
    x_smooth = np.linspace(x_original.min(), x_original.max(), len(temperature_data) * 10)

    # Interpolate data points for smooth curve
    spline = make_interp_spline(x_original, temperature_data, k=3)
    temperature_smooth = spline(x_smooth)

    bg_color = '#1e1e1e'

    # Plotting
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))
    fig.patch.set_facecolor(bg_color)  # Set background color
    ax.set_facecolor(bg_color)  # Set background color

    plt.plot(days_of_week[:-1], temperature_data, marker='o', color='g', linestyle="", label='Previous Temperature')
    plt.plot(days_of_week[-1], prediction, marker='o', markersize=10, color='#fcba03', label='Prediction')
    # Annotate prediction value
    plt.annotate(f'{prediction:.1f}°C', xy=(days_of_week[-1], prediction), xytext=(days_of_week[-1], prediction + 0.6),
                 color='#fcba03', fontsize=10, ha='center', va='bottom')
    plt.plot(x_smooth, temperature_smooth, color='g')

    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Forecast')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    # Remove box around plot
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    # Add grid and legend
    plt.grid(False)
    legend = plt.legend()
    frame = legend.get_frame()
    frame.set_facecolor(bg_color)
    frame.set_edgecolor(bg_color)
    for text in legend.get_texts():
        text.set_color("white")
    # frame.set_
    plt.tight_layout()

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(
        buf, format="png", bbox_inches="tight"
    )  # Ensuring no clipping of the figure
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    response = JsonResponse({"uri": uri})
    return response


def get_days_of_week(start_date, num_days):
    days_of_week = []
    current_date = start_date
    for _ in range(num_days):
        days_of_week.append(current_date.strftime("%A"))  # Get the full name of the day (e.g., Monday, Tuesday)
        current_date += datetime.timedelta(days=1)
    return days_of_week


def get_data_points(request):
    past_days = get_previous_days(request)
    coords = get_coords(request)
    inputs = preprocess_data(past_days, coords)
    inputs = inputs.reshape(1, 7, 11)
    prediction = loaded_model.predict(inputs, verbose=0)
    scatter_points = format_data_as_scatter(past_days, prediction)
    return scatter_points


def get_previous_days(request, num_days=7):
    current_station_code = request.session.get("currentStationCode", None)

    previous_day = datetime.datetime.now() - datetime.timedelta(days=1)
    previous_day = previous_day.replace(hour=12, minute=0, second=0, microsecond=0)

    noon_data = []
    for _ in range(num_days):
        station_data = StationData.objects.filter(
            STATION_CODE=current_station_code,
            DATE_TIME=previous_day
        ).values()
        if len(station_data) > 0:
            noon_data.append(station_data[0])
        else:
            print("No data for", previous_day)
        previous_day = previous_day - datetime.timedelta(days=1)
    return noon_data


def get_coords(request):
    current_station_code = request.session.get("currentStationCode", None)
    station = WeatherStation.objects.filter(STATION_CODE=current_station_code).values()
    x = station[0]["X"]
    y = station[0]["Y"]
    return x, y


# This should be saved programmatically in the model, but time crunch means its here
train_mean = np.array([-122.289505,
                       52.272775,
                       0.146956,
                       3.186029,
                       57.329437,
                       -1.939490,
                       -0.249218,
                       -4.039542,
                       -0.564725,
                       0.876123,
                       0.374235, ])
train_std = np.array([3.861687,
                      2.858695,
                      0.583744,
                      6.913500,
                      21.431285,
                      6.532320,
                      6.204363,
                      13.395522,
                      12.815088,
                      0.124792,
                      0.277112, ])


def preprocess_data(past_days, coords):
    li = []
    for day in past_days:
        li.append(pd.DataFrame(day, index=[0]))
    df = pd.concat(li, axis=0, ignore_index=True)

    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format='%Y%m%d%H')
    df['DATE'] = df['DATE_TIME'].dt.date
    df['TIME'] = df['DATE_TIME'].dt.time
    df['X'], df['Y'] = coords

    wv = df.pop('HOURLY_WIND_SPEED')
    max_wv = df.pop('HOURLY_WIND_GUST')

    wd_rad = df.pop('HOURLY_WIND_DIRECTION') * np.pi / 180

    df['Wx'] = wv * np.cos(wd_rad)
    df['Wy'] = wv * np.sin(wd_rad)

    df['max Wx'] = max_wv * np.cos(wd_rad)
    df['max Wy'] = max_wv * np.sin(wd_rad)

    timestamp_s = df['DATE_TIME'].map(pd.Timestamp.timestamp)
    day = 24 * 60 * 60
    year = 365.2425 * day
    df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

    columns_we_need = ['X',
                       'Y',
                       'HOURLY_PRECIPITATION',
                       'HOURLY_TEMPERATURE',
                       'HOURLY_RELATIVE_HUMIDITY',
                       'Wx',
                       'Wy',
                       'max Wx',
                       'max Wy',
                       'Year sin',
                       'Year cos']

    df = df[columns_we_need]
    df = (df - train_mean) / train_std
    return np.array(df)
    input_width = 7
    label_width = 1
    shift = 1
    columns_to_predict = ['HOURLY_PRECIPITATION', 'HOURLY_TEMPERATURE', 'HOURLY_RELATIVE_HUMIDITY', 'Wx', 'Wy',
                          'max Wx', 'max Wy']
    w_generator = WindowGenerator(input_width=input_width, label_width=label_width, shift=shift,
                                  df=df,
                                  label_columns=columns_to_predict)
    inputs = w_generator.make_single_window(df)
    return inputs


def format_data_as_scatter(past_days, prediction):
    columns_to_show = ['HOURLY_TEMPERATURE']
    prediction_indices = [1]
    denormalize_indices = [3]
    x, y = [], []
    for i, day in enumerate(past_days):
        x.append(i)
        y.append(day[columns_to_show[0]])
    x.append(len(past_days))
    y.append(denormalize(prediction[0][prediction_indices[0]][0], denormalize_indices[0]))
    return x, y


def denormalize(data, index):
    return data * train_std[index] + train_mean[index]


class WindowGenerator:
    def __init__(self, input_width, label_width, shift, df,
                 label_columns=None):
        # Store the raw dataframes
        self.df = df

        # Work out the label column indices.
        if label_columns is not None:
            self.label_columns = label_columns
        elif label_columns is None:
            self.label_columns = None
        else:
            raise ValueError(f"label_columns: {label_columns} not found in df")

        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}
        self.column_indices = {name: i for i, name in enumerate(df.columns)}

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
            batch_size=32, )

        ds = ds.map(self.split_window)

        return ds

    def make_single_window(self, data):
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
