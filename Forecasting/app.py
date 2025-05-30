
# Importing necessary libraries and frameworks
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os
from datetime import timedelta
from datetime import datetime as dt
from dateutil import parser
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time

# TensorFlow and LSTM-related imports
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

# Facebook Prophet imports for time series forecasting
from prophet import Prophet

# StatsModels for statistical analysis
import statsmodels.api as sm
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\sugip\Downloads\suhas\suhas\suhas\src\Forecasting\lstm-442301-8b1ec0bdda12.json"
# Import required storage package from Google Cloud Storage

from google.cloud import storage
matplotlib.use('agg')
# Initilize flask app
app = Flask(__name__)
# Handles CORS (cross-origin resource sharing)
CORS(app)
# Initlize Google cloud storage client
client = storage.Client()

# Add response headers to accept all types of  requests

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods",
                         "PUT, GET, POST, DELETE, OPTIONS")
    return response

#  Modify response headers when returning to the origin

def build_actual_response(response):
    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers.set("Access-Control-Allow-Methods",
                         "PUT, GET, POST, DELETE, OPTIONS")
    return response

'''
API route path is  "/api/forecast"
This API will accept only POST request
'''

@app.route('/api/statmis', methods=['POST'])
def statmis():
    body = request.get_json()
    type = body["type"]
    repo_name = body["repo"]
    print("type",type)
    issues = body["issues"]

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    OBSERVATION_IMAGE_NAME = "stats_observation_" + type +"_"+ repo_name + ".png"
    OBSERVATION_IMAGE_URL = BASE_IMAGE_PATH + OBSERVATION_IMAGE_NAME

    FORECAST_IMAGE_NAME = "stats_forecast_" + type +"_" + repo_name + ".png"
    FORECAST_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_IMAGE_NAME

    df = pd.DataFrame(issues)
    df1 = df.groupby(['created_at'], as_index = False).count()
    dataFrame = df1[['created_at','issue_number']]
    dataFrame.columns = ['ds', 'y']
    dataFrame.set_index('y')
    period = len(dataFrame) // 2
    predict = sm.tsa.seasonal_decompose(dataFrame.index, period=period)
    figure = predict.plot()
    figure.set_size_inches(12,7)
    plt.title("Observations plot of created issues")
    figure.get_figure().savefig(LOCAL_IMAGE_PATH + OBSERVATION_IMAGE_NAME)               #observation image
    model = sm.tsa.ARIMA(dataFrame['y'].iloc[1:], order = (1, 0, 0))
    results = model.fit()
    dataFrame['forecast'] = results.fittedvalues
    fig = dataFrame[['y', 'forecast']].plot(figsize=(12,7))
    plt.title("Timeseries forecasting of created issues")
    fig.get_figure().savefig(LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)                      #forecast image

     # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(OBSERVATION_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + OBSERVATION_IMAGE_NAME)

    new_blob = bucket.blob(FORECAST_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

    # Construct the response
    json_response = {
        "stats_observation_url": OBSERVATION_IMAGE_URL,
        "stats_forecast_url": FORECAST_IMAGE_URL
    }
    print("statmis,",json_response)
    # Returns image url back to flask microservice
    return jsonify(json_response)


@app.route('/api/statmisc', methods=['POST'])
def statmisc():
    body = request.get_json()
    type = body["type"]
    repo_name = body["repo"]
    print("type",type)
    issues = body["issues"]

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    OBSERVATION_IMAGE_NAME = "stats_observation_" + type +"_"+ repo_name + ".png"
    OBSERVATION_IMAGE_URL = BASE_IMAGE_PATH + OBSERVATION_IMAGE_NAME

    FORECAST_IMAGE_NAME = "stats_forecast_" + type +"_" + repo_name + ".png"
    FORECAST_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_IMAGE_NAME

    df = pd.DataFrame(issues)
    df1 = df.groupby(['closed_at'], as_index = False).count()
    dataFrame = df1[['closed_at','issue_number']]
    dataFrame.columns = ['ds', 'y']
    dataFrame.set_index('y')
    period = len(dataFrame) // 2
    predict = sm.tsa.seasonal_decompose(dataFrame.index, period=period)
    figure = predict.plot()
    figure.set_size_inches(12,7)
    plt.title("Observations plot of closed issues")
    figure.get_figure().savefig(LOCAL_IMAGE_PATH + OBSERVATION_IMAGE_NAME)               #observation image
    model = sm.tsa.ARIMA(dataFrame['y'].iloc[1:], order = (1, 0, 0))
    results = model.fit()
    dataFrame['forecast'] = results.fittedvalues
    fig = dataFrame[['y', 'forecast']].plot(figsize=(12,7))
    plt.title("Timeseries forecasting of closed issues")
    fig.get_figure().savefig(LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)


     # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(OBSERVATION_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + OBSERVATION_IMAGE_NAME)

    new_blob = bucket.blob(FORECAST_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

    # Construct the response
    json_response = {
        "stats_observation_url": OBSERVATION_IMAGE_URL,
        "stats_forecast_url": FORECAST_IMAGE_URL
    }
    print("statmisc,",json_response)
    # Returns image url back to flask microservice
    return jsonify(json_response)


@app.route('/api/statmcommits', methods=['POST'])
def statmcommits():
    body = request.get_json()
    commit_response = body["pull"]
    repo_name = body["repo"]
    type = body["type"]
    print("type:",type)

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    OBSERVATION_IMAGE_NAME = "stats_observation_" + type +"_"+ repo_name + ".png"
    OBSERVATION_IMAGE_URL = BASE_IMAGE_PATH + OBSERVATION_IMAGE_NAME

    FORECAST_IMAGE_NAME = "stats_forecast_" + type +"_" + repo_name + ".png"
    FORECAST_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_IMAGE_NAME

    df = pd.DataFrame(commit_response)
    df1 = df.groupby(['created_at'], as_index = False).count()
    dataFrame = df1[['created_at','commit_number']]
    dataFrame.columns = ['ds', 'y']
    print(dataFrame)
    dataFrame.set_index('y')
    period = len(dataFrame) // 2
    predict = sm.tsa.seasonal_decompose(dataFrame.index, period=period)
    figure = predict.plot()
    figure.set_size_inches(12,7)
    plt.title("Observations plot of commits")
    figure.get_figure().savefig(LOCAL_IMAGE_PATH + OBSERVATION_IMAGE_NAME)               #observation image
    model = sm.tsa.ARIMA(dataFrame['y'].iloc[1:], order = (1, 0, 0))
    results = model.fit()
    dataFrame['forecast'] = results.fittedvalues
    fig = dataFrame[['y', 'forecast']].plot(figsize=(12,7))
    plt.title("Timeseries forecasting of commits")
    fig.get_figure().savefig(LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

     # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(OBSERVATION_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + OBSERVATION_IMAGE_NAME)

    new_blob = bucket.blob(FORECAST_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

    # Construct the response
    json_response = {
        "stats_observation_url": OBSERVATION_IMAGE_URL,
        "stats_forecast_url": FORECAST_IMAGE_URL
    }
    print("statmcommits,",json_response)

    # Returns image url back to flask microservice
    return jsonify(json_response)
    

@app.route('/api/statmpull', methods=['POST'])
def statmpull():
    body = request.get_json()
    pull_req_response = body["pull"]
    repo_name = body["repo"]
    type = body["type"]

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    OBSERVATION_IMAGE_NAME = "stats_observation_" + type +"_"+ repo_name + ".png"
    OBSERVATION_IMAGE_URL = BASE_IMAGE_PATH + OBSERVATION_IMAGE_NAME

    FORECAST_IMAGE_NAME = "stats_forecast_" + type +"_" + repo_name + ".png"
    FORECAST_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_IMAGE_NAME

    df = pd.DataFrame(pull_req_response)
    df1 = df.groupby(['created_at'], as_index = False).count()
    dataFrame = df1[['created_at','pull_req_number']]
    dataFrame.columns = ['ds', 'y']
    dataFrame.set_index('y')
    period = len(dataFrame) // 2
    predict = sm.tsa.seasonal_decompose(dataFrame.index, period=period)
    figure = predict.plot()
    figure.set_size_inches(12,7)
    plt.title("Observations plot of pull requests")
    figure.get_figure().savefig(LOCAL_IMAGE_PATH + OBSERVATION_IMAGE_NAME)               #observation image
    model = sm.tsa.ARIMA(dataFrame['y'].iloc[1:], order = (1, 0, 0))
    results = model.fit()
    dataFrame['forecast'] = results.fittedvalues
    fig = dataFrame[['y', 'forecast']].plot(figsize=(12,7))
    plt.title("Timeseries forecasting of pull requests")
    fig.get_figure().savefig(LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)
    
    # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(OBSERVATION_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + OBSERVATION_IMAGE_NAME)

    new_blob = bucket.blob(FORECAST_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

    # Construct the response
    json_response = {
        "stats_observation_url": OBSERVATION_IMAGE_URL,
        "stats_forecast_url": FORECAST_IMAGE_URL
    }
    print("statmpull,",json_response)
    # Returns image url back to flask microservice
    return jsonify(json_response)


@app.route('/api/fbprophetis', methods=['POST'])
def fbprophetis():
    body = request.get_json()
    type = body["type"]
    repo_name = body["repo"]
    issues = body["issues"]

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    FORECAST_IMAGE_NAME = "fbprophet_forecast_" + type +"_"+ repo_name + ".png"
    FORECAST_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_IMAGE_NAME

    FORECAST_COMPONENTS_IMAGE_NAME = "fbprophet_forecast_components_" + type +"_" + repo_name + ".png"
    FORECAST_COMPONENTS_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME

    df = pd.DataFrame(issues)
    df1 = df.groupby(['created_at'], as_index = False).count()
    dataFrame = df1[['created_at','issue_number']]
    dataFrame.columns = ['ds', 'y']
    model = Prophet(daily_seasonality=True)
    model.fit(dataFrame)
    future = model.make_future_dataframe(periods=60)
    forecast = model.predict(future)
    forcast_fig1 = model.plot(forecast)
    forcast_fig2 = model.plot_components(forecast)
    forcast_fig1.savefig(LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)
    forcast_fig2.savefig(LOCAL_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME)

    

    # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(FORECAST_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

    new_blob = bucket.blob(FORECAST_COMPONENTS_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME)

    # Construct the response
    json_response = {
        "fbprophet_forecast_url": FORECAST_IMAGE_URL,
        "fbprophet_forecast_components_url": FORECAST_COMPONENTS_IMAGE_URL
    }
    print("fbprophetis,",json_response)

    # Returns image url back to flask microservice
    return jsonify(json_response)

@app.route('/api/fbprophetisc', methods=['POST'])
def fbprophetisc():
    body = request.get_json()
    type = body["type"]
    repo_name = body["repo"]
    print("type",type)
    issues = body["issues"]

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    FORECAST_IMAGE_NAME = "fbprophet_forecast_" + type +"_"+ repo_name + ".png"
    FORECAST_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_IMAGE_NAME

    FORECAST_COMPONENTS_IMAGE_NAME = "fbprophet_forecast_components_" + type +"_" + repo_name + ".png"
    FORECAST_COMPONENTS_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME


    df = pd.DataFrame(issues)
    df1 = df.groupby(['closed_at'], as_index = False).count()
    dataFrame = df1[['closed_at','issue_number']]
    dataFrame.columns = ['ds', 'y']
    model = Prophet(daily_seasonality=True)
    model.fit(dataFrame)
    future = model.make_future_dataframe(periods=60)
    forecast = model.predict(future)
    forcast_fig1 = model.plot(forecast)
    forcast_fig2 = model.plot_components(forecast)
    forcast_fig1.savefig(LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)
    forcast_fig2.savefig(LOCAL_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME)

    

    # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(FORECAST_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

    new_blob = bucket.blob(FORECAST_COMPONENTS_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME)

    # Construct the response
    json_response = {
        "fbprophet_forecast_url": FORECAST_IMAGE_URL,
        "fbprophet_forecast_components_url": FORECAST_COMPONENTS_IMAGE_URL
    }
    print("fbprophetisc,",json_response)
    # Returns image url back to flask microservice
    return jsonify(json_response)

@app.route('/api/fbprophetpull', methods=['POST'])
def fbprophetpull():
    body = request.get_json()
    pull_req_response = body["pull"]
    repo_name = body["repo"]
    type = body["type"]

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    FORECAST_IMAGE_NAME = "fbprophet_forecast_" + type +"_"+ repo_name + ".png"
    FORECAST_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_IMAGE_NAME

    FORECAST_COMPONENTS_IMAGE_NAME = "fbprophet_forecast_components_" + type +"_" + repo_name + ".png"
    FORECAST_COMPONENTS_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME

    df = pd.DataFrame(pull_req_response)
    df1 = df.groupby(['created_at'], as_index = False).count()
    dataFrame = df1[['created_at','pull_req_number']]
    dataFrame.columns = ['ds', 'y']
    model = Prophet(daily_seasonality=True)
    model.fit(dataFrame)
    future = model.make_future_dataframe(periods=60)
    forecast = model.predict(future)
    forcast_fig1 = model.plot(forecast)
    forcast_fig2 = model.plot_components(forecast)
    forcast_fig1.savefig(LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)
    forcast_fig2.savefig(LOCAL_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME)

    

    # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(FORECAST_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

    new_blob = bucket.blob(FORECAST_COMPONENTS_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME)

    # Construct the response
    json_response = {
        "fbprophet_forecast_url": FORECAST_IMAGE_URL,
        "fbprophet_forecast_components_url": FORECAST_COMPONENTS_IMAGE_URL
    }
    
    print("fbprophetpull,",json_response)
    # Returns image url back to flask microservice
    return jsonify(json_response)

@app.route('/api/commits', methods=['POST'])
def commits():
    body = request.get_json()
    commit_response = body["pull"]
    repo_name = body["repo"]
    type = body["type"]
    print("type:",type)

    data_frame = pd.DataFrame(commit_response)
    df1 = data_frame.groupby(["created_at"], as_index=False).count()
    df = df1[["created_at", 'commit_number']]
    df.columns = ['ds', 'y']
    print(df)
    df['ds'] = pd.to_datetime(df['ds'])
    array = df.to_numpy()
    x = np.array([time.mktime(i[0].timetuple()) for i in array])
    y = np.array([i[1] for i in array])
    print("Y: ", y)

    # Find the first day directly from the DataFrame
    firstDay = df['ds'].min()

    '''
    To achieve data consistency with both actual data and predicted values, 
    add zeros to dates that do not have orders
    [firstDay + timedelta(days=day) for day in range((max(df['ds']) - firstDay).days + 1)]
    '''
    Ys = [0] * ((max(df['ds']) - firstDay).days + 1)
    days = pd.Series([firstDay + timedelta(days=i)
                    for i in range(len(Ys))])
    for d, y_val in zip(df['ds'], y):
        Ys[(d - firstDay).days] = y_val

    # Modify the data that is suitable for LSTM
    Ys = np.array(Ys)
    Ys = Ys.astype('float32')
    Ys = np.reshape(Ys, (-1, 1))
    # Apply min max scaler to transform the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    Ys = scaler.fit_transform(Ys)
    # Divide training - test data with 80-20 split
    train_size = int(len(Ys) * 0.80)
    test_size = len(Ys) - train_size
    train, test = Ys[0:train_size, :], Ys[train_size:len(Ys), :]
    print('train size:', len(train), ", test size:", len(test))

    # Create the training and test dataset
    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)
    '''
    Look back decides how many days of data the model looks at for prediction
    Here LSTM looks at approximately one month data
    '''
    look_back = min(30, len(test) - 2)
    print(len(test))

    # Assuming create_dataset is a function that formats the data for LSTM
    if len(test) > look_back + 1:
        X_test, Y_test = create_dataset(test, look_back)
    else:
        print("Test dataset is too small for the specified look_back period.")
    X_train, Y_train = create_dataset(train, look_back)
   # X_test, Y_test = create_dataset(test, look_back)

    # Additional check: Ensure that X_test and X_train are not empty
    if len(X_train) == 0:
        print("X_train is empty. Check the train dataset and look_back parameter.")
    if len(X_test) == 0:
        print("X_test is empty. Check the test dataset and look_back parameter.")

    # Reshape input to be [samples, time steps, features]
    # Add a check to avoid reshaping if the dataset is empty
    if len(X_train) > 0:
        X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    if len(X_test) > 0:
        X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # Verifying the shapes
    print('Shapes:', X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

    # Model to forecast
    model = Sequential()
    model.add(LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    # Fit the model with training data and set appropriate hyper parameters
    history = model.fit(X_train, Y_train, epochs=20, batch_size=70, validation_data=(X_test, Y_test),
    callbacks=[EarlyStopping(monitor='val_loss', patience=10)], verbose=1, shuffle=False)

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    MODEL_LOSS_IMAGE_NAME = "model_loss_" + type +"_"+ repo_name + ".png"
    MODEL_LOSS_URL = BASE_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME

    LSTM_GENERATED_IMAGE_NAME = "lstm_generated_data_" + type +"_" + repo_name + ".png"
    LSTM_GENERATED_URL = BASE_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME

    ALL_ISSUES_DATA_IMAGE_NAME = "all_issues_data_" + type + "_"+ repo_name + ".png"
    ALL_ISSUES_DATA_URL = BASE_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME

    # Plot the model loss image
    plt.figure(figsize=(8, 4))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Test Loss')
    plt.title('Model Loss For ' + "Commits")
    plt.ylabel('Loss')
    plt.xlabel('Epochs')
    plt.legend(loc='upper right')
    # Save the figure in /static/images folder
    #plt.savefig(LOCAL_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME)
    plt.savefig(LOCAL_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME)

    # Predict issues for test data
    y_pred = model.predict(X_test)

    # Plot the LSTM Generated image
    fig, axs = plt.subplots(1, 1, figsize=(10, 4))
    X = mdates.date2num(days)
    axs.plot(np.arange(0, len(Y_train)), Y_train, 'g', label="history")
    axs.plot(np.arange(len(Y_train), len(Y_train) + len(Y_test)),
    Y_test, marker='.', label="true")
    axs.plot(np.arange(len(Y_train), len(Y_train) + len(Y_test)),
    y_pred, 'r', label="prediction")
    axs.legend()
    axs.set_title('LSTM Generated Data For ' + "Commits")
    axs.set_xlabel('Time Steps')
    axs.set_ylabel('Commits')
    # Save the figure in /static/images folder
    plt.savefig(LOCAL_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME)


    # Plot the All Pull request data images
    fig, axs = plt.subplots(1, 1, figsize=(10, 4))
    X = mdates.date2num(days)
    axs.plot(X, Ys, 'purple', marker='.')
    locator = mdates.AutoDateLocator()
    axs.xaxis.set_major_locator(locator)
    axs.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    axs.legend()
    axs.set_title('All Commits Data')
    axs.set_xlabel('Date')
    axs.set_ylabel('Commits')
    # Save the figure in /static/images folder
    plt.savefig(LOCAL_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME)

    # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(MODEL_LOSS_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME)
    new_blob = bucket.blob(ALL_ISSUES_DATA_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME)
    new_blob = bucket.blob(LSTM_GENERATED_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME)

    # Construct the response
    json_response = {
        "model_loss_image_url": MODEL_LOSS_URL,
        "lstm_generated_image_url": LSTM_GENERATED_URL,
        "all_issues_data_image": ALL_ISSUES_DATA_URL
    }
    
    print("/api/commits,",json_response)

    # Returns image url back to flask microservice

    return jsonify(json_response)


@app.route('/api/fbprophetcommits', methods=['POST'])
def fbprophetcommits():
    body = request.get_json()
    commit_response = body["pull"]
    repo_name = body["repo"]
    type = body["type"]
    print("type:",type)

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')

    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    LOCAL_IMAGE_PATH = "static/images/"
    FORECAST_IMAGE_NAME = "fbprophet_forecast_" + type +"_"+ repo_name + ".png"
    FORECAST_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_IMAGE_NAME

    FORECAST_COMPONENTS_IMAGE_NAME = "fbprophet_forecast_components_" + type +"_" + repo_name + ".png"
    FORECAST_COMPONENTS_IMAGE_URL = BASE_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME

    df = pd.DataFrame(commit_response)
    df1 = df.groupby(['created_at'], as_index = False).count()
    dataFrame = df1[['created_at','commit_number']]
    dataFrame.columns = ['ds', 'y']
    model = Prophet(daily_seasonality=True)
    model.fit(dataFrame)
    future = model.make_future_dataframe(periods=60)
    forecast = model.predict(future)
    forcast_fig1 = model.plot(forecast)
    forcast_fig2 = model.plot_components(forecast)
    forcast_fig1.savefig(LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)
    forcast_fig2.savefig(LOCAL_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME)

    

    # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(FORECAST_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_IMAGE_NAME)

    new_blob = bucket.blob(FORECAST_COMPONENTS_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + FORECAST_COMPONENTS_IMAGE_NAME)

    # Construct the response
    json_response = {
        "fbprophet_forecast_url": FORECAST_IMAGE_URL,
        "fbprophet_forecast_components_url": FORECAST_COMPONENTS_IMAGE_URL
    }
    print("fbprophetcommits,",json_response)
    # Returns image url back to flask microservice
    return jsonify(json_response)


@app.route('/api/pulls', methods=['POST'])
def pulls():
    body = request.get_json()
    pull_req_response = body["pull"]
    repo_name = body["repo"]
    type = body["type"]
    print("type",type)

    data_frame = pd.DataFrame(pull_req_response)
    print(data_frame)
    df1 = data_frame.groupby(["created_at"], as_index=False).count()
    df = df1[["created_at", 'pull_req_number']]
    df.columns = ['ds', 'y']
    print(df)
    df['ds'] = pd.to_datetime(df['ds'])
    array = df.to_numpy()
    x = np.array([time.mktime(i[0].timetuple()) for i in array])
    y = np.array([i[1] for i in array])
    print("Y: ", y)

    # Find the first day directly from the DataFrame
    firstDay = df['ds'].min()

  
    Ys = [0] * ((max(df['ds']) - firstDay).days + 1)
    days = pd.Series([firstDay + timedelta(days=i)
                    for i in range(len(Ys))])
    for d, y_val in zip(df['ds'], y):
        Ys[(d - firstDay).days] = y_val

    # Modify the data that is suitable for LSTM
    Ys = np.array(Ys)
    Ys = Ys.astype('float32')
    Ys = np.reshape(Ys, (-1, 1))
    # Apply min max scaler to transform the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    Ys = scaler.fit_transform(Ys)
    # Divide training - test data with 80-20 split
    train_size = int(len(Ys) * 0.80)
    test_size = len(Ys) - train_size
    train, test = Ys[0:train_size, :], Ys[train_size:len(Ys), :]
    print('train size:', len(train), ", test size:", len(test))

    # Create the training and test dataset
    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)
 
    look_back = min(30, len(test) - 2)
    print(len(test))

    # Assuming create_dataset is a function that formats the data for LSTM
    if len(test) > look_back + 1:
        X_test, Y_test = create_dataset(test, look_back)
    else:
        print("Test dataset is too small for the specified look_back period.")
    X_train, Y_train = create_dataset(train, look_back)
   # X_test, Y_test = create_dataset(test, look_back)

    # Additional check: Ensure that X_test and X_train are not empty
    if len(X_train) == 0:
        print("X_train is empty. Check the train dataset and look_back parameter.")
    if len(X_test) == 0:
        print("X_test is empty. Check the test dataset and look_back parameter.")

    # Reshape input to be [samples, time steps, features]
    # Add a check to avoid reshaping if the dataset is empty
    if len(X_train) > 0:
        X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    if len(X_test) > 0:
        X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # Verifying the shapes
    print('Shapes:', X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)


    # Model to forecast
    model = Sequential()
    model.add(LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    # Fit the model with training data and set appropriate hyper parameters
    history = model.fit(X_train, Y_train, epochs=20, batch_size=70, validation_data=(X_test, Y_test),
    callbacks=[EarlyStopping(monitor='val_loss', patience=10)], verbose=1, shuffle=False)

    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')
    # DO NOT DELETE "static/images" FOLDER as it is used to store figures/images generated by matplotlib
    LOCAL_IMAGE_PATH = "static/images/"
    MODEL_LOSS_IMAGE_NAME = "model_loss_" + type +"_"+ repo_name + ".png"
    MODEL_LOSS_URL = BASE_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME

    LSTM_GENERATED_IMAGE_NAME = "lstm_generated_data_" + type +"_" + repo_name + ".png"
    LSTM_GENERATED_URL = BASE_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME

    ALL_ISSUES_DATA_IMAGE_NAME = "all_issues_data_" + type + "_"+ repo_name + ".png"
    ALL_ISSUES_DATA_URL = BASE_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME

    # Add your unique Bucket Name if you want to run it local
    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    # Plot the model loss image
    plt.figure(figsize=(8, 4))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Test Loss')
    plt.title('Model Loss For ' + "Pull Request")
    plt.ylabel('Loss')
    plt.xlabel('Epochs')
    plt.legend(loc='upper right')
    # Save the figure in /static/images folder
    #plt.savefig(LOCAL_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME)
    plt.savefig(LOCAL_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME)

    # Predict issues for test data
    y_pred = model.predict(X_test)

    # Plot the LSTM Generated image
    fig, axs = plt.subplots(1, 1, figsize=(10, 4))
    X = mdates.date2num(days)
    axs.plot(np.arange(0, len(Y_train)), Y_train, 'g', label="history")
    axs.plot(np.arange(len(Y_train), len(Y_train) + len(Y_test)),
    Y_test, marker='.', label="true")
    axs.plot(np.arange(len(Y_train), len(Y_train) + len(Y_test)),
    y_pred, 'r', label="prediction")
    axs.legend()
    axs.set_title('LSTM Generated Data For ' + "Pull request")
    axs.set_xlabel('Time Steps')
    axs.set_ylabel('Pull Request')
    # Save the figure in /static/images folder
    plt.savefig(LOCAL_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME)


    # Plot the All Pull request data images
    fig, axs = plt.subplots(1, 1, figsize=(10, 4))
    X = mdates.date2num(days)
    axs.plot(X, Ys, 'purple', marker='.')
    locator = mdates.AutoDateLocator()
    axs.xaxis.set_major_locator(locator)
    axs.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    axs.legend()
    axs.set_title('All Pull Request Data')
    axs.set_xlabel('Date')
    axs.set_ylabel('Pull Request')
    # Save the figure in /static/images folder
    plt.savefig(LOCAL_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME)
    # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(MODEL_LOSS_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME)
    new_blob = bucket.blob(ALL_ISSUES_DATA_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME)
    new_blob = bucket.blob(LSTM_GENERATED_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME)

    # Construct the response
    json_response = {
        "model_loss_image_url": MODEL_LOSS_URL,
        "lstm_generated_image_url": LSTM_GENERATED_URL,
        "all_issues_data_image": ALL_ISSUES_DATA_URL
    }
    
    print("/api/pulls",json_response)
    # Returns image url back to flask microservice
    return jsonify(json_response)
@app.route('/api/forecast', methods=['POST'])
def forecast():
    body = request.get_json()
    issues = body["issues"]
    type = body["type"]
    repo_name = body["repo"]
    data_frame = pd.DataFrame(issues)
    df1 = data_frame.groupby([type], as_index=False).count()
    df = df1[[type, 'issue_number']]
    df.columns = ['ds', 'y']
    print("df: ", df)
    df['ds'] = pd.to_datetime(df['ds'])

    # Converting to numpy array
    array = df.to_numpy()
    x = np.array([time.mktime(i[0].timetuple()) for i in array])
    y = np.array([i[1] for i in array])

    print("Y: ", y)

    # Find the first day directly from the DataFrame
    firstDay = df['ds'].min()

   
    Ys = [0] * ((max(df['ds']) - firstDay).days + 1)
    days = pd.Series([firstDay + timedelta(days=i)
                    for i in range(len(Ys))])
    for d, y_val in zip(df['ds'], y):
        Ys[(d - firstDay).days] = y_val

    # Modify the data that is suitable for LSTM
    Ys = np.array(Ys)
    Ys = Ys.astype('float32')
    Ys = np.reshape(Ys, (-1, 1))
    # Apply min max scaler to transform the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    Ys = scaler.fit_transform(Ys)
    # Divide training - test data with 80-20 split
    train_size = int(len(Ys) * 0.80)
    test_size = len(Ys) - train_size
    train, test = Ys[0:train_size, :], Ys[train_size:len(Ys), :]
    print('train size:', len(train), ", test size:", len(test))

    # Create the training and test dataset
    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)
  
    look_back = min(30, len(test) - 2)
    print(len(test))

    # Assuming create_dataset is a function that formats the data for LSTM
    if len(test) > look_back + 1:
        X_test, Y_test = create_dataset(test, look_back)
    else:
        print("Test dataset is too small for the specified look_back period.")
    X_train, Y_train = create_dataset(train, look_back)
   # X_test, Y_test = create_dataset(test, look_back)

    # Additional check: Ensure that X_test and X_train are not empty
    if len(X_train) == 0:
        print("X_train is empty. Check the train dataset and look_back parameter.")
    if len(X_test) == 0:
        print("X_test is empty. Check the test dataset and look_back parameter.")

    # Reshape input to be [samples, time steps, features]
    # Add a check to avoid reshaping if the dataset is empty
    if len(X_train) > 0:
        X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    if len(X_test) > 0:
        X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # Verifying the shapes
    print('Shapes:', X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)


    # Model to forecast
    model = Sequential()
    model.add(LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    print("TEST ---------")
    print(X_train.shape)
    print(Y_train.shape)
    print(X_test.shape)
    print(Y_test.shape)

    model = Sequential()
    model.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1))  # Output layer: adjust the number of neurons and activation function based on your task

    # Compile the model - this example is for a regression task
    model.compile(optimizer='adam', loss='mean_squared_error',metrics=['accuracy'],run_eagerly=True)

    # Fit the model with training data and set appropriate hyper parameters
    history = model.fit(X_train, Y_train, epochs=20, batch_size=70, validation_data=(X_test, Y_test),
                        callbacks=[EarlyStopping(monitor='val_loss', patience=10)], verbose=1, shuffle=False)

    '''
    Creating image URL
    BASE_IMAGE_PATH refers to Google Cloud Storage Bucket URL.Add your Base Image Path in line 145
    if you want to run the application local
    LOCAL_IMAGE_PATH refers local directory where the figures generated by matplotlib are stored
    These locally stored images will then be uploaded to Google Cloud Storage
    '''
    BASE_IMAGE_PATH = os.environ.get(
        'BASE_IMAGE_PATH', 'https://storage.googleapis.com/lstm_95/')
    # DO NOT DELETE "static/images" FOLDER as it is used to store figures/images generated by matplotlib
    LOCAL_IMAGE_PATH = "static/images/"

    # Creating the image path for model loss, LSTM generated image and all issues data image
    MODEL_LOSS_IMAGE_NAME = "model_loss_" + type +"_"+ repo_name + ".png"
    MODEL_LOSS_URL = BASE_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME

    LSTM_GENERATED_IMAGE_NAME = "lstm_generated_data_" + type +"_" + repo_name + ".png"
    LSTM_GENERATED_URL = BASE_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME

    ALL_ISSUES_DATA_IMAGE_NAME = "all_issues_data_" + type + "_"+ repo_name + ".png"
    ALL_ISSUES_DATA_URL = BASE_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME

    DAY_MAX_ISSUE_CREATED_IMAGE_NAME = "day_max_issues_created_data_" + type + "_"+ repo_name + ".png"
    DAY_MAX_ISSUE_CREATED_DATA_URL = BASE_IMAGE_PATH + DAY_MAX_ISSUE_CREATED_IMAGE_NAME

    DAY_MAX_ISSUE_CLOSED_IMAGE_NAME = "day_max_issues_closed_data_" + type + "_"+ repo_name + ".png"
    DAY_MAX_ISSUE_CLOSED_DATA_URL = BASE_IMAGE_PATH + DAY_MAX_ISSUE_CLOSED_IMAGE_NAME

    MONTH_MAX_ISSUE_CLOSED_IMAGE_NAME = "month_max_issues_closed_data_" + type + "_"+ repo_name + ".png"
    MONTH_MAX_ISSUE_CLOSED_DATA_URL = BASE_IMAGE_PATH + MONTH_MAX_ISSUE_CLOSED_IMAGE_NAME

        # Parse incoming request data
    body = request.get_json()
    issues = body.get("issues", [])
    forecast_type = body.get("type", "created_at")
    repo_name = body.get("repo", "unknown_repo")
    
        # Generate a complete time series, filling missing days with zeros
    start_date = formatted_data['ds'].min()
    full_series_length = (formatted_data['ds'].max() - start_date).days + 1
    complete_series = [0] * full_series_length
    date_range = pd.Series([start_date + timedelta(days=i) for i in range(full_series_length)])
    for date, count in zip(formatted_data['ds'], issue_counts):
        complete_series[(date - start_date).days] = count

    # Add your unique Bucket Name if you want to run it local
    BUCKET_NAME = os.environ.get(
        'BUCKET_NAME', 'lstm_95')

    # Model summary()

   

    print("TEST1 y_pred_sample",X_test.shape)
    print(X_test.shape)

    


    # Plot the model loss image
    print("HISTORY: ",history.history.keys())
    plt.figure(figsize=(8, 4))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Test Loss')
    plt.title('Model Loss For ' + type)
    plt.ylabel('Loss')
    plt.xlabel('Epochs')
    plt.legend(loc='upper right')
    # Save the figure in /static/images folder
    plt.savefig(LOCAL_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME)

    # Predict issues for test data
    y_pred = model.predict(X_test)

    # Plot the LSTM Generated image
    fig, axs = plt.subplots(1, 1, figsize=(10, 4))
    X = mdates.date2num(days)
    axs.plot(np.arange(0, len(Y_train)), Y_train, 'g', label="history")
    axs.plot(np.arange(len(Y_train), len(Y_train) + len(Y_test)),
             Y_test, marker='.', label="true")
    axs.plot(np.arange(len(Y_train), len(Y_train) + len(Y_test)),
             y_pred, 'r', label="prediction")
    axs.legend()
    axs.set_title('LSTM Generated Data For ' + type)
    axs.set_xlabel('Time Steps')
    axs.set_ylabel('Issues')
    # Save the figure in /static/images folder
    plt.savefig(LOCAL_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME)

    # Plot the All Issues data images
    fig, axs = plt.subplots(1, 1, figsize=(10, 4))
    X = mdates.date2num(days)
    axs.plot(X, Ys, 'purple', marker='.')
    locator = mdates.AutoDateLocator()
    axs.xaxis.set_major_locator(locator)
    axs.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    axs.legend()
    axs.set_title('All Issues Data')
    axs.set_xlabel('Date')
    axs.set_ylabel('Issues')
    # Save the figure in /static/images folder
    plt.savefig(LOCAL_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME)

    #REQ 1,2,3
    x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data_frame = pd.DataFrame(issues)
    data_frame['created_at'] = pd.to_datetime(data_frame['created_at'], errors='coerce')
    week_df = data_frame.groupby(data_frame['created_at'].dt.day_name()).size()
    week_df = pd.DataFrame({'Created_On':week_df.index, 'Count':week_df.values})
    week_df = week_df.groupby(['Created_On']).sum().reindex(x)
    max_issue_count = week_df.max()
    max_issue_day = week_df['Count'].idxmax()
    plt.figure(figsize=(12, 7))
    plt.plot(week_df['Count'], label='Issues')
    plt.title('Number of Issues Created for particular Week Days.')
    plt.ylabel('Number of Issues')
    plt.xlabel('Week Days')
    plt.savefig(LOCAL_IMAGE_PATH + DAY_MAX_ISSUE_CREATED_IMAGE_NAME)

    data_frame['closed_at'] = pd.to_datetime(data_frame['closed_at'], errors='coerce')
    week_df = data_frame.groupby(data_frame['closed_at'].dt.day_name()).size()
    week_df = pd.DataFrame({'Closed_On':week_df.index, 'Count':week_df.values})
    week_df = week_df.groupby(['Closed_On']).sum().reindex(x)
    max_issue_count_closed = week_df.max()
    max_issue_day_closed = week_df['Count'].idxmax()
    plt.figure(figsize=(12, 7))
    plt.plot(week_df['Count'], label='Issues')
    plt.title('Number of Issues Closed for particular Week Days.')
    plt.ylabel('Number of Issues')
    plt.xlabel('Week Days')
    plt.savefig(LOCAL_IMAGE_PATH + DAY_MAX_ISSUE_CLOSED_IMAGE_NAME)

    
      # Helper function to create dataset for LSTM
    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset) - look_back - 1):
            X.append(dataset[i:(i + look_back), 0])
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

    # Set look_back parameter
    look_back = min(30, len(test_data) - 2)
    X_train, Y_train = create_dataset(train_data, look_back)
    X_test, Y_test = create_dataset(test_data, look_back)

    # Reshape data for LSTM input
    if X_train.size > 0:
        X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    if X_test.size > 0:
        X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])

    # Define and compile the LSTM model
    model = Sequential([
        LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    
    data_frame = pd.DataFrame(issues)
    x = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    data_frame['closed_at'] = pd.to_datetime(data_frame['closed_at'], errors='coerce')
    month_df = data_frame.groupby(data_frame['closed_at'].dt.month_name()).size()
    month_df = pd.DataFrame({'Closed_On':month_df.index, 'Count':month_df.values})
    month_df = month_df.groupby(['Closed_On']).sum().reindex(x)
    max_issue_count_closed_month = month_df.max()
    max_issue_closed_month = month_df['Count'].idxmax()
    plt.figure(figsize=(12, 7))
    plt.plot(month_df['Count'], label='Issues')
    plt.title('Number of Issues Closed for particular Month.')
    plt.ylabel('Number of Issues')
    plt.xlabel('Month Names')
    plt.savefig(LOCAL_IMAGE_PATH + MONTH_MAX_ISSUE_CLOSED_IMAGE_NAME)
    # Uploads an images into the google cloud storage bucket
    bucket = client.get_bucket(BUCKET_NAME)
    new_blob = bucket.blob(MODEL_LOSS_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + MODEL_LOSS_IMAGE_NAME)
    new_blob = bucket.blob(ALL_ISSUES_DATA_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + ALL_ISSUES_DATA_IMAGE_NAME)
    new_blob = bucket.blob(LSTM_GENERATED_IMAGE_NAME)
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + LSTM_GENERATED_IMAGE_NAME)
    new_blob = bucket.blob(DAY_MAX_ISSUE_CREATED_IMAGE_NAME)    
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + DAY_MAX_ISSUE_CREATED_IMAGE_NAME)
    new_blob = bucket.blob(DAY_MAX_ISSUE_CLOSED_IMAGE_NAME)    
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + DAY_MAX_ISSUE_CLOSED_IMAGE_NAME)
    new_blob = bucket.blob(MONTH_MAX_ISSUE_CLOSED_IMAGE_NAME)    
    new_blob.upload_from_filename(
        filename=LOCAL_IMAGE_PATH + MONTH_MAX_ISSUE_CLOSED_IMAGE_NAME)

    # Construct the response
    json_response = {
        "model_loss_image_url": MODEL_LOSS_URL,
        "lstm_generated_image_url": LSTM_GENERATED_URL,
        "all_issues_data_image": ALL_ISSUES_DATA_URL,
        "day_max_issue_created": DAY_MAX_ISSUE_CREATED_DATA_URL,
        "day_max_issue_closed": DAY_MAX_ISSUE_CLOSED_DATA_URL,
        "month_max_issues_closed": MONTH_MAX_ISSUE_CLOSED_DATA_URL
    }
    
    print("/api/forecast",json_response)

    # Returns image url back to flask microservice
    return jsonify(json_response)


# Run LSTM app server on port 8080
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
