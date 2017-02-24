# In[]:
# Import required libraries

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten


# In[]:
# MLP model

def MLP(input_shape, nb_classes):

    # Create model
    model = Sequential()
    model.name = 'MLP'

    # Input layer
    model.add(Flatten(input_shape=input_shape))
    model.add(Dense(784))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    # Hidden layer 1
    model.add(Dense(1568))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    # Hidden layer 2
    model.add(Dense(784))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    # Output layer
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model
