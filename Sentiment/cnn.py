#!/usr/bin/env python

"""
params: 50 batches, filter len 4, 5 epochs
output:
Using Theano backend.
fold 0 accuracy: 0.761012
fold 1 accuracy: 0.798500
fold 2 accuracy: 0.787992
fold 3 accuracy: 0.809568
fold 4 accuracy: 0.757974
fold 5 accuracy: 0.768293
fold 6 accuracy: 0.781426
fold 7 accuracy: 0.772983
fold 8 accuracy: 0.783302
fold 9 accuracy: 0.798311
0.781936252272
"""

import sys
sys.path.append('../Lib/')
sys.dont_write_bytecode = True

import numpy as np
np.random.seed(1337) # for reproducibility

import sklearn as sk
import sklearn.cross_validation
import keras as k
import keras.utils.np_utils
import dataset
import word2vec_model
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.layers.embeddings import Embedding

NFOLDS = 10
BATCH = 50
EPOCHS = 5
CLASSES = 2
EMBDIMS = 300
MAXLEN = 55
MAXFEATURES = 18000
FILTERS = 100
FILTLEN = 4

if __name__ == "__main__":

  dataset = dataset.DatasetProvider(MAXFEATURES)
  x, y = dataset.load_data()

  # TODO: what what are we doing for index 0 (oov words)?
  path = '/Users/Dima/Loyola/Data/Word2Vec/Models/GoogleNews-vectors-negative300.txt'
  word2vec = word2vec_model.Model(path)
  init_vectors = word2vec.select_vectors(dataset.alphabet)

  # turn x and y into numpy array among other things
  x = sequence.pad_sequences(x, maxlen=MAXLEN)
  y = k.utils.np_utils.to_categorical(np.array(y), CLASSES)  

  scores = []
  folds = sk.cross_validation.KFold(len(y),
                                    n_folds=NFOLDS,
                                    shuffle=True)

  # todo: look at train_indices and test_indices
  for fold_num, (train_indices, test_indices) in enumerate(folds):
    train_x = x[train_indices]
    train_y = y[train_indices]
    test_x = x[test_indices]
    test_y = y[test_indices]
    
    model = k.models.Sequential()

    model.add(Embedding(MAXFEATURES,
                        EMBDIMS,
                        input_length=MAXLEN,
                        weights=[init_vectors]))

    model.add(Convolution1D(nb_filter=FILTERS,
                            filter_length=FILTLEN,
                            border_mode='valid',
                            activation='relu',
                            subsample_length=1))
    model.add(MaxPooling1D(pool_length=2))
    model.add(Flatten())

    model.add(Dense(CLASSES))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    model.fit(train_x,
              train_y,
              nb_epoch=EPOCHS,
              batch_size=BATCH,
              verbose=0,
              validation_split=0.1)
    score, accuracy = model.evaluate(test_x,
                                     test_y,
                                     batch_size=BATCH,
                                     verbose=0)
    # todo: what is score?
    print 'fold %d accuracy: %f' % (fold_num, accuracy)
    scores.append(accuracy)
  
  print np.mean(scores)
