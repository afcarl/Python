#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy as np
import sklearn as sk
import sklearn.cross_validation
import os, os.path

import keras as k
import keras.models
import keras.layers.core
import keras.utils.np_utils

NFOLDS = 10
BATCH = 32
EPOCHS = 5
CLASSES = 2
DIMENSIONS = 300

if __name__ == "__main__":

  np.random.seed(1337) 
  
  pos_examples = np.loadtxt('pos.txt')
  pos_labels = [1] * pos_examples.shape[0]
  neg_examples = np.loadtxt('neg.txt')
  neg_labels = [0] * neg_examples.shape[0]
  examples = np.vstack((pos_examples, neg_examples))
  labels = np.array(pos_labels + neg_labels)
  labels_one_hot = k.utils.np_utils.to_categorical(labels, CLASSES)

  scores = []
  folds = sk.cross_validation.KFold(len(labels), n_folds=NFOLDS)

  for train_indices, test_indices in folds:
    train_x = examples[train_indices]
    train_y = labels_one_hot[train_indices]
    test_x = examples[test_indices]
    test_y = labels_one_hot[test_indices]

    model = k.models.Sequential()
    model.add(k.layers.core.Dense(512, input_shape=(DIMENSIONS,)))
    model.add(k.layers.core.Activation('relu'))
    model.add(k.layers.core.Dropout(0.5))
    model.add(k.layers.core.Dense(CLASSES))
    model.add(k.layers.core.Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')
    history = model.fit(train_x, train_y,
                        nb_epoch=EPOCHS, batch_size=BATCH, verbose=0,
                        show_accuracy=True, validation_split=0.1)
    score = model.evaluate(test_x, test_y,
                           batch_size=BATCH, verbose=0,
                           show_accuracy=True)

    scores.append(score[1])
  
  print np.mean(scores)
  
