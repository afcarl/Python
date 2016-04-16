#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

"""10-fold CV performance is about 0.76"""

import numpy as np
import sklearn as sk
import sklearn.cross_validation
import keras as k
import keras.utils.np_utils
import dataset

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, SimpleRNN, GRU

NFOLDS = 10
BATCH = 50
EPOCHS = 5
EMBDIMS = 300
MAXLEN = 55
MAXFEATURES = 18000

if __name__ == "__main__":

  np.random.seed(1337) 
  dataset = dataset.DatasetProvider(MAXFEATURES)
  x, y = dataset.load_data()

  x = sequence.pad_sequences(x, maxlen=MAXLEN)
  y = np.array(y)

  scores = []
  folds = sk.cross_validation.KFold(len(y), n_folds=NFOLDS, shuffle=True)

  for fold_num, (train_indices, test_indices) in enumerate(folds):
    train_x = x[train_indices]
    train_y = y[train_indices]
    test_x = x[test_indices]
    test_y = y[test_indices]
    
    model = k.models.Sequential()
    model.add(Embedding(MAXFEATURES, EMBDIMS, input_length=MAXLEN))
    model.add(LSTM(128)) 
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
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
