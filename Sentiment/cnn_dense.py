#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy as np
np.random.seed(1337)

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

  path = '/Users/Dima/Loyola/Data/Word2Vec/Models/GoogleNews-vectors-negative300.txt'
  word2vec = word2vec_model.Model(path)
  init_vectors = word2vec.select_vectors(dataset.alphabet)

  # turn x and y into numpy arrays among other things
  
  x = sequence.pad_sequences(x, maxlen=MAXLEN)
  y = k.utils.np_utils.to_categorical(np.array(y), CLASSES)

  print x[0]
  print x[1]

  X = np.zeros((10662, 55, 300))
  for row in range(10662):
    for col in range(55):
      # X[row, col, :] = np.random.uniform(-1, 1, 300)
      word = x[row][col]
      X[row, col, :] = init_vectors[word]
  
  scores = []
  folds = sk.cross_validation.KFold(len(y), n_folds=NFOLDS,
                                    shuffle=True, random_state=1337)

  # todo: look at train_indices and test_indices
  for fold_num, (train_indices, test_indices) in enumerate(folds):
    train_x = X[train_indices]
    train_y = y[train_indices]
    test_x = X[test_indices]
    test_y = y[test_indices]

    model = k.models.Sequential()

    model.add(Convolution1D(input_shape=(55, 300),
                            nb_filter=FILTERS,
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
