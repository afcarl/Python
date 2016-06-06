#!/usr/bin/env python

import sys
sys.path.append('../Lib/')
sys.dont_write_bytecode = True

import numpy as np
np.random.seed(1337)

import sklearn as sk
from sklearn.metrics import f1_score
import keras as k
import keras.utils.np_utils
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.layers import LSTM, SimpleRNN, GRU

import dataset
import properties 

if __name__ == "__main__":

  # learn alphabet from training data
  dataset = dataset.DatasetProvider([properties.train,
                                     properties.test])
  # now load training examples and labels
  train_x, train_y = dataset.load(properties.train)
  # now load test examples and labels
  test_x, test_y = dataset.load(properties.test)

  # turn x and y into numpy array among other things
  maxlen = max([len(seq) for seq in train_x + test_x])
  classes = len(set(train_y))
  train_x = sequence.pad_sequences(train_x, maxlen=maxlen)
  train_y = k.utils.np_utils.to_categorical(np.array(train_y), classes)  
  test_x = sequence.pad_sequences(test_x, maxlen=maxlen)
  test_y = k.utils.np_utils.to_categorical(np.array(test_y), classes)  

  print 'train_x shape:', train_x.shape
  print 'train_y shape:', train_y.shape
  print 'test_x shape:', test_x.shape
  print 'test_y shape:', test_y.shape
  
  model = k.models.Sequential()
    
  model.add(Embedding(len(dataset.alphabet),
                      properties.embdims,
                      input_length=maxlen,
                      dropout=0.2,
                      weights=None)) 
  
  model.add(LSTM(64))

  model.add(Dense(classes))
  model.add(Activation('softmax'))
  model.summary()
  model.compile(loss='categorical_crossentropy',
                optimizer='rmsprop',
                metrics=['accuracy'])
  model.fit(train_x,
            train_y,
            nb_epoch=5,
            batch_size=50,
            verbose=1,
            validation_split=0.1)

  # distribution over classes
  distribution = model.predict(test_x, batch_size=50)
  # class predictions
  predictions = np.argmax(distribution, axis=1)
  # gold labels
  gold = np.argmax(test_y, axis=1)
  # f1 for each class
  f1 = f1_score(gold, predictions, average=None)

  print 'f1 for contains:', f1[1]
  print 'all scores:', f1
