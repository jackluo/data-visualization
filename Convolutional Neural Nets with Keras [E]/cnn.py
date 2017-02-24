# In[]:
# Import required libraries

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D


# In[]:
# CNN model

def CNN(input_shape, nb_classes):

    nb_filters = 32
    pool_size = 2, 2
    kernel_size = 3, 3

    # Create model
    model = Sequential()
    model.name = 'CNN'

    # Input layer
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                            border_mode='valid', input_shape=input_shape))
    model.add(Activation('relu'))

    # Pooling layer 1
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.25))  # Dropout to prevent overfitting
    model.add(Flatten())

    # Hidden layer 2
    model.add(Dense(128))
    model.add(Activation('relu'))

    # Hidden layer 3
    model.add(Dense(32))
    model.add(Activation('relu'))

    # Output layer
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    return model
