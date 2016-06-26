#!/usr/bin/env python

import numpy as np
np.random.seed(1337)

import sys
sys.path.append('../Lib/')
sys.dont_write_bytecode = True

import sklearn as sk
from sklearn.metrics import f1_score
import keras as k
from keras.utils.np_utils import to_categorical
from keras.optimizers import RMSprop
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Merge
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.layers.embeddings import Embedding
import dataset
import ConfigParser

if __name__ == "__main__":

  cfg = ConfigParser.ConfigParser()
  cfg.read('settings.ini')
  print 'train:', cfg.get('data', 'train')
  print 'test:', cfg.get('data', 'test')
  print 'batches:', cfg.get('cnn', 'batches')
  print 'epochs:', cfg.get('cnn', 'epochs')
  print 'embdims:', cfg.get('cnn', 'embdims')
  print 'filters:', cfg.get('cnn', 'filters')
  print 'filtlen:', cfg.get('cnn', 'filtlen')
  print 'dropout:', cfg.get('cnn', 'dropout')
  print 'learnrt:', cfg.get('cnn', 'learnrt')

  # learn alphabet from training and test data
  dataset = \
    dataset.DatasetProvider([cfg.get('data', 'train'),
                             cfg.get('data', 'test')])
  # now load training examples and labels
  train_x, train_y = dataset.load(cfg.get('data', 'train'))
  # now load test examples and labels
  test_x, test_y = dataset.load(cfg.get('data', 'test'))

  # turn x and y into numpy array among other things
  maxlen = max([len(seq) for seq in train_x + test_x])
  classes = len(set(train_y))
  train_x = pad_sequences(train_x, maxlen=maxlen)
  train_y = to_categorical(np.array(train_y), classes)  
  test_x = pad_sequences(test_x, maxlen=maxlen)
  test_y = to_categorical(np.array(test_y), classes)  

  print 'train_x shape:', train_x.shape
  print 'train_y shape:', train_y.shape
  print 'test_x shape:', test_x.shape
  print 'test_y shape:', test_y.shape, '\n'

  branches = [] # models to be merged
  train_xs = [] # train x for each branch 
  test_xs = []  # test x for each branch
  
  for filter_len in cfg.get('cnn', 'filtlen').split(','):

    branch = Sequential()
    branch.add(Embedding(len(dataset.alphabet),
                         cfg.getint('cnn', 'embdims'),
                         input_length=maxlen,
                         weights=None)) 
    branch.add(Convolution1D(nb_filter=cfg.getint('cnn', 'filters'),
                             filter_length=int(filter_len),
                             border_mode='valid',
                             activation='relu',
                             subsample_length=1))
    branch.add(MaxPooling1D(pool_length=2))
    branch.add(Flatten())

    branches.append(branch)
    train_xs.append(train_x)
    test_xs.append(test_x)

  model = Sequential()

  # keras merge only works if there is more than one layer
  if len(cfg.get('cnn', 'filtlen').split(',')) > 1:
    model.add(Merge(branches, mode='concat'))
  else:
    model.add(branches[0])
    train_xs = train_x
    test_xs = test_x
    
  model.add(Dense(250))
  model.add(Dropout(cfg.getfloat('cnn', 'dropout')))
  model.add(Activation('relu'))

  model.add(Dropout(cfg.getfloat('cnn', 'dropout')))
  model.add(Dense(classes))
  model.add(Activation('softmax'))

  optimizer = RMSprop(lr=cfg.getfloat('cnn', 'learnrt'),
                      rho=0.9, epsilon=1e-08)
  model.compile(loss='categorical_crossentropy',
                optimizer=optimizer,
                metrics=['accuracy'])
  model.fit(train_xs,
            train_y,
            nb_epoch=cfg.getint('cnn', 'epochs'),
            batch_size=cfg.getint('cnn', 'batches'),
            verbose=1,
            validation_split=0.1)

  # distribution over classes
  distribution = \
    model.predict(test_xs, batch_size=cfg.getint('cnn', 'batches'))
  # class predictions
  predictions = np.argmax(distribution, axis=1)
  # gold labels
  gold = np.argmax(test_y, axis=1)
  # f1s for contains + contains-1
  label_f1 = f1_score(gold, predictions, average=None)
  contains_f1 = f1_score(gold, predictions, labels=[1,2], average='micro')
  print 'f1 for contains:', contains_f1
  print 'all f1s:', label_f1