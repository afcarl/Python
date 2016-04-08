#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy as np
import sklearn as sk
import sklearn.cross_validation
import keras as k
import keras.utils.np_utils
import dataset

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.embeddings import Embedding

NFOLDS = 10
BATCH = 32
EPOCHS = 5
CLASSES = 2
EMBDIMS = 100
MAXLEN = 100
MAXFEATURES = 10000

if __name__ == "__main__":

  np.random.seed(1337) 
  dataset = dataset.Dataset(MAXFEATURES)
  x, y = dataset.load_data()
  labels_one_hot = k.utils.np_utils.to_categorical(np.array(y), CLASSES)  

  x = sequence.pad_sequences(x, maxlen=MAXLEN)

  scores = []
  folds = sk.cross_validation.KFold(len(y), n_folds=NFOLDS)

  for train_indices, test_indices in folds:
    print 'starting new fold...'
    train_x = x[train_indices]
    train_y = labels_one_hot[train_indices]
    test_x = x[test_indices]
    test_y = labels_one_hot[test_indices]
    
    model = k.models.Sequential()

    model.add(Embedding(MAXFEATURES, EMBDIMS, input_length=MAXLEN))
    model.add(Flatten()) # not sure what this is...
    
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))

    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))

    model.add(Dense(CLASSES))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')
    history = model.fit(train_x, train_y,
                        nb_epoch=EPOCHS, batch_size=BATCH, verbose=0,
                        show_accuracy=True, validation_split=0.1)
    score = model.evaluate(test_x, test_y,
                           batch_size=BATCH, verbose=0,
                           show_accuracy=True)

    scores.append(score[1])
  
  print np.mean(scores)
  
