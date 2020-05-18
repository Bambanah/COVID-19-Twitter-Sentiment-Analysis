import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from tensorflow.keras.preprocessing import sequence

import models
import datasets


def run_lstm_model(x_train, y_train, x_test, y_test,
                   num_features,
                   metrics=None,
                   batch_size=None,
                   epochs=None,
                   maxlen=None,
                   embedding_size=None,
                   kernel_size=None,
                   filters=None,
                   pool_size=None,
                   lstm_output_size=None):
    # Training
    if batch_size is None:
        batch_size = 128
    if epochs is None:
        epochs = 20

    # Embedding
    if maxlen is None:
        maxlen = 100
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

    print('Pad sequences (samples x time)')
    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    print('x_train shape:', x_train.shape)
    print('x_test shape:', x_test.shape)

    print('Build model...')
    lstm_model = models.lstm(num_features,
                             maxlen=maxlen,
                             embedding_size=embedding_size,
                             kernel_size=kernel_size,
                             filters=filters,
                             pool_size=pool_size,
                             lstm_output_size=lstm_output_size,
                             metrics=metrics)

    print('Train...')
    lstm_model.fit(x_train,
                   y_train,
                   batch_size=batch_size,
                   epochs=epochs,
                   validation_data=(x_test, y_test),
                   use_multiprocessing=True)
    lstm_loss, lstm_acc = lstm_model.evaluate(x_test, y_test, batch_size=batch_size)

    return lstm_loss, lstm_acc


if __name__ == "__main__":

    model_LSTM = True
    model_GRU = False

    # Run LSTM Modelling
    if model_LSTM:
        num_rows = 25000  # Number of rows to load from data
        max_features = 20000  # Maximum number of features (words) to process

        # Load Sentiment 140 dataset
        (x_train_140, y_train_140), \
        (x_test_140, y_test_140), vocab_size = datasets.load_sentiment_140(num_words=max_features,
                                                                           num_rows=num_rows,
                                                                           test_split=0.2,
                                                                           seed=69)

        # Load IMDB dataset
        (x_train_imdb, y_train_imdb), \
        (x_test_imdb, y_test_imdb) = tf.keras.datasets.imdb.load_data(num_words=max_features)

        if 'vocab_size' not in locals():
            vocab_size = max_features

        loss_140, acc_140 = run_lstm_model(x_train_140, y_train_140, x_test_140, y_test_140,
                                           num_features=vocab_size,
                                           metrics=["acc"])

        # loss_imdb, acc_imdb = run_lstm_model(x_train_imdb, y_train_imdb, x_test_imdb, y_test_imdb,
        #                                      num_features=max_features,
        #                                      metrics=["acc"])

        print('Test loss 140:', loss_140)
        print('Test accuracy 140:', acc_140)

        # print('Test loss IMDB:', loss_imdb)
        # print('Test accuracy IMDB:', acc_imdb)

    # Run GRU modelling
    if model_GRU:
        pass
