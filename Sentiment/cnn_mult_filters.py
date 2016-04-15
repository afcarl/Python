#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy as np
import sklearn as sk
import sklearn.cross_validation
import keras as k
import keras.utils.np_utils
import dataset

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Merge
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.layers.embeddings import Embedding

NFOLDS = 10
BATCH = 25
EPOCHS = 5
CLASSES = 2
EMBDIMS = 300
MAXLEN = 55
MAXFEATURES = 18000
FILTERS = 100
# FILTLEN = 4

if __name__ == "__main__":

  np.random.seed(1337) 
  dataset = dataset.Dataset(MAXFEATURES)
  x, y = dataset.load_data()

  # turn x and y into numpy arrays among other things
  x = sequence.pad_sequences(x, maxlen=MAXLEN)
  y = k.utils.np_utils.to_categorical(np.array(y), CLASSES)  

  scores = []
  folds = sk.cross_validation.KFold(len(y), n_folds=NFOLDS)

  for fold_num, (train_indices, test_indices) in enumerate(folds):
    train_x = x[train_indices]
    train_y = y[train_indices]
    test_x = x[test_indices]
    test_y = y[test_indices]
    
    left = Sequential()
    left.add(Embedding(MAXFEATURES, EMBDIMS, input_length=MAXLEN))
    left.add(Convolution1D(nb_filter=FILTERS,
                           filter_length=3,
                           border_mode='valid',
                           activation='relu',
                           subsample_length=1))
    left.add(MaxPooling1D(pool_length=2))
    left.add(Flatten())

    right = Sequential()
    right.add(Embedding(MAXFEATURES, EMBDIMS, input_length=MAXLEN))
    right.add(Convolution1D(nb_filter=FILTERS,
                           filter_length=4,
                           border_mode='valid',
                           activation='relu',
                           subsample_length=1))
    right.add(MaxPooling1D(pool_length=2))
    right.add(Flatten())

    model = Sequential()
    model.add(Merge([left, right], mode='concat'))
    model.add(Dense(CLASSES))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop')
    model.fit(train_x, train_y,
              nb_epoch=EPOCHS, batch_size=BATCH, verbose=0,
              show_accuracy=True, validation_split=0.1)
    score = model.evaluate(test_x, test_y,
                           batch_size=BATCH, verbose=0,
                           show_accuracy=True)

    print 'fold %d accuracy: %f' % (fold_num, score[1])
    scores.append(score[1])
  
  print np.mean(scores)
  
