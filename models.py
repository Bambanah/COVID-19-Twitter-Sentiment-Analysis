# Disable tensorflow debugging information

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM, GRU
from tensorflow.keras.layers import Conv1D, MaxPooling1D



def lstm(vocab_size,
         embedding_size=128,
         maxlen=100,
         filters=64,
         pool_size=None,
         kernel_size=5,
         lstm_output_size=70,
         metrics=None):

    model = Sequential()

    model.add(Embedding(vocab_size, embedding_size, input_length=maxlen))
    model.add(Dropout(0.2))
    #
    model.add(Conv1D(filters,
                     kernel_size,
                     padding='valid',
                     activation='relu',
                     strides=1))
    model.add(MaxPooling1D(pool_size=pool_size))

    model.add(LSTM(lstm_output_size, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(lstm_output_size))
    model.add(Dropout(0.2))

    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))

    model.add(Dense(1, activation='sigmoid'))

    opt = tf.keras.optimizers.Adam(lr=1e-3, decay=1e-5)

    model.compile(loss='binary_crossentropy',
                  optimizer=opt,
                  metrics=metrics)

    print(model.summary())

    return model