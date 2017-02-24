# In[]:
# Import required libraries

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from keras.utils import np_utils
from keras.datasets import mnist

from cnn import CNN
from mlp import MLP


# In[]:
# Set parameters / hyperparameters

batch_size = 128
nb_epoch = 12


# In[]:
# Import data

(X_train, Y_train), (X_test, Y_test) = mnist.load_data() # (60000, 28, 28)
input_shape = (28, 28, 1) #
nb_classes = 10
input_shape[0] * input_shape[1]


# In[]:
# Preprocess data

# Reshape data (if theano place the '1's as first argument for CNN)
X_train = X_train.reshape(X_train.shape[0], input_shape[0], input_shape[1], input_shape[2])
X_test = X_test.reshape(X_test.shape[0], input_shape[0], input_shape[1], input_shape[2])

# Other
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

# Labels
Y_train = np_utils.to_categorical(Y_train, 10)
Y_test = np_utils.to_categorical(Y_test, 10)


# In[]:
# Build model using Keras

model = MLP(input_shape, nb_classes) # Around 98.0% accuracy but much simpler model
#model = CNN(input_shape, nb_classes) # Around 99.1% acucracy


# In[]:
# Run model

model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
         verbose=1, validation_data=(X_test, Y_test))

score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
model.save('models/mnist_model_' + model.name + '.h5')
print('Saved model to disk.')
