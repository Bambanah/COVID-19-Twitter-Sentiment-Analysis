import os
import pathlib

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from models import ensemble_classifers, logistic_regression_covid
import pandas as pd
import numpy as np

import models
import datasets
import download_data


def run_simple_models(x_train, y_train, x_test, y_test):
    ensemble_classifers(x_train, y_train, x_test, y_test)

def run_simple_models_covid(x_train, y_train, x_test_covid):
    logistic_regression_covid(x_train, y_train, x_test_covid, dates)

def build_lstm_model(num_features,
                     embedding_size=None,
                     kernel_size=None,
                     filters=None,
                     pool_size=None,
                     lstm_output_size=None):
    """
    Builds and compiles an LSTM model with the provided hyper-parameters
    Args:
        num_features:
        embedding_size:
        kernel_size:
        filters:
        pool_size:
        lstm_output_size:

    Returns:

    """
    # Embedding
    if embedding_size is None:
        embedding_size = 64

    # Convolution
    if kernel_size is None:
        kernel_size = 5
    if filters is None:
        filters = 64
    if pool_size is None:
        pool_size = 4

    # LSTM
    if lstm_output_size is None:
        lstm_output_size = 70

    print('Build model...')

    lstm_model = models.lstm(num_features,
                             embedding_size=embedding_size,
                             kernel_size=kernel_size,
                             filters=filters,
                             pool_size=pool_size,
                             lstm_output_size=lstm_output_size)

    return lstm_model


def build_gru_model(num_features,
                    embedding_size=None,
                    kernel_size=None,
                    filters=None,
                    pool_size=None,
                    gru_output_size=None):
    """
    Builds and compiles an GRU model with the provided hyper-parameters
    Args:
        num_features:
        embedding_size:
        kernel_size:
        filters:
        pool_size:
        lstm_output_size:

    Returns:

    """
    # Embedding
    if embedding_size is None:
        embedding_size = 64

    # Convolution
    if kernel_size is None:
        kernel_size = 5
    if filters is None:
        filters = 64
    if pool_size is None:
        pool_size = 4

    # GRU
    if gru_output_size is None:
        gru_output_size = 70

    print('Build model...')

    gru_model = models.gru(num_features,
                           embedding_size=embedding_size,
                           kernel_size=kernel_size,
                           filters=filters,
                           pool_size=pool_size,
                           gru_output_size=gru_output_size)

    return gru_model


def train_model(model, x_train, y_train, x_test, y_test,
                epochs=None, batch_size=None):
    """
    Trains model on provided data.
    Args:
        model: A compiled tensorflow model
        x_train: Training X data
        y_train: Training Y data
        x_test: Testing X data
        y_test: Testing Y data
        batch_size: Batch size for training and validation
        epochs: Number of epochs to train for
    """

    # Training
    if batch_size is None:
        batch_size = 128
    if epochs is None:
        epochs = 20

    print('x_train shape:', x_train.shape)
    print('x_test shape:', x_test.shape)

    print('Train...')
    model.fit(x_train,
              y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test),
              use_multiprocessing=True)


def eval_model(model, x_test, y_test, batch_size=None):
    """
    Evaluated model on provided testing data
    Args:
        model: Trained tensorflow model
        x_test: X testing data
        y_test: Y testing data
        batch_size: Batch size for evaluations (Default 128)

    Returns:
        Loss and accuracy metrics
    """
    if batch_size is None:
        batch_size = 128

    loss, acc = model.evaluate(x_test, y_test, batch_size=batch_size)
    positive_bias_threshold = models.confusion_matrix_model(model, y_test, x_test)
    return loss, acc, positive_bias_threshold


def run_lstm():
    """"""
    # Build LSTM model
    lstm_model = build_lstm_model(num_features=max_features)

    # Assign data to evaluate model (if training in sequence)
    x_eval, y_eval = x_test_140, y_test_140

    # Train on sentiment 140 dataset
    if train_140:
        # Train and evaluate model
        train_model(lstm_model, x_train_140, y_train_140, x_test_140, y_test_140, epochs, batch_size)

        if not train_in_sequence:
            lstm_loss_140, lstm_acc_140, positive_bias_threshold = eval_model(lstm_model, x_test_140, y_test_140)

            # Show results
            print('Test loss 140:', lstm_loss_140)
            print('Test accuracy 140:', lstm_acc_140)
            print('Positive bias threshold 140:', positive_bias_threshold)
            # Rebuild model
            lstm_model = build_lstm_model(num_features=max_features)

    if train_in_sequence:
        # Evaluate model on assigned eval set
        lstm_loss, lstm_acc, positive_bias_threshold = eval_model(lstm_model, x_eval, y_eval)
        # Show results
        print('Test Loss:', lstm_loss)
        print('Test Accuracy:', lstm_acc)
        print('Positive bias threshold: ', positive_bias_threshold)

    y_pred = lstm_model.predict(processed_covid)


def run_gru():
    """"""
    # Build GRU model
    gru_model = build_gru_model(num_features=max_features)

    # Assign data to evaluate model (if training in sequence)
    x_eval, y_eval = x_test_140, y_test_140

    # Train on sentiment 140 dataset
    if train_140:
        # Train and evaluate model
        train_model(gru_model, x_train_140, y_train_140, x_test_140, y_test_140, epochs, batch_size)

        if not train_in_sequence:
            gru_loss_140, gru_acc_140, positive_bias_threshold = eval_model(gru_model, x_test_140, y_test_140)

            # Show results
            print('Test loss 140:', gru_loss_140)
            print('Test accuracy 140:', gru_acc_140)
            print('Positive bias threshold 140:', positive_bias_threshold)

            # Rebuild model
            gru_model = build_gru_model(num_features=max_features)

    if train_in_sequence:
        # Evaluate model on assigned eval set
        gru_loss, gru_acc, positive_bias_threshold = eval_model(gru_model, x_eval, y_eval)

        # Show results
        print('Test Loss:', gru_loss)
        print('Test Accuracy:', gru_acc)
        print('Positive bias threshold: ', positive_bias_threshold)


def run_simple():
    if train_140:
        run_simple_models(x_train_140, y_train_140, x_test_140, y_test_140)


if __name__ == "__main__":
    # ----- SWITCHES -----

    # RNNs
    model_LSTM = False
    model_GRU = False

    train_in_sequence = True  # Train model on multiple datasets, instead of resetting and training seperately

    # Simple Classifiers
    simple_classifiers = True

    # Datasets to train model on
    train_140 = True  # Train selected models on sentiment 140 dataset

    # ----- SETUP -----

    grab_data = False

    if grab_data:
        # Download all files in shared data folder
        download_data.download_from_drive(file_names=['sentiment140.zip'])

        # Unzip each zip saved in local data folder
        download_data.unzip_data()

        print("Data organised")

    pathlib.Path("figures/RNN").mkdir(parents=True, exist_ok=True)
    pathlib.Path("logs").mkdir(parents=True, exist_ok=True)

    # ----- LOAD DATA -----

    # Data parameters
    data_dir = "data"

    num_rows = 300000  # Number of rows to load from data
    seed = 69
    test_split = 0.2

    max_features = 20000  # Maximum number of features (words) to process
    maxlen = 100  # Maximum length of sequences - all sequences will be cut or padded to this length

    force_covid_reload = False

    corpus = []
    dates = []

    print("Loading corpus for vectorizer...", end="")

    # Check if exists
    if os.path.isfile(data_dir + "/covid19-tweets/dataframe.csv") and not force_covid_reload:
        covid_data = pd.read_csv(data_dir + "/covid19-tweets/dataframe.csv")
    else:
        covid_data = datasets.load_covid(num_rows=num_rows, seed=seed)
        covid_data.to_csv(data_dir + "/covid19-tweets/dataframe.csv")
    corpus = covid_data["text"]
    dates = covid_data["created_at"]
    print(dates)
    print("Loaded %d rows from covid data." % (len(corpus) - 1))
    print(" Done")

    # Create vectorizer
    print("Creating vectorizer...", end="")
    vectorizer = datasets.create_vectorizer(corpus, max_features=max_features, simple_classifier = simple_classifiers)
    print(" Done")

    if train_140:
        # Sentiment 140
        print("Loading Sentiment 140...", end="")
        (x_train_140, y_train_140), \
        (x_test_140, y_test_140) = datasets.load_sentiment_140(vectorizer=vectorizer,
                                                               data_dir=data_dir,
                                                               num_rows=num_rows,
                                                               maxlen=maxlen,
                                                               simple_classifier=simple_classifiers,
                                                               test_split=test_split,
                                                               seed=seed)
        print(" Done")

    # Covid-19 Tweets
    print("Loading COVID-19 Tweets...", end="")
    processed_covid = datasets.preprocess(vectorizer, corpus, maxlen, simple_classifier = simple_classifiers)
    print(" Done")

    # ----- TRAINING -----

    # Training parameters
    epochs = 1
    batch_size = 128

    # Run LSTM Model
    if model_LSTM:
        run_lstm()

    # Run GRU modelling
    if model_GRU:
        run_gru()

    if simple_classifiers:
        run_simple()
        run_simple_models_covid(x_train_140, y_train_140,processed_covid,)
