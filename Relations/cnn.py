#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy as np
np.random.seed(1337) # for reproducibility

import sklearn as sk
import sklearn.cross_validation
from sklearn.metrics import f1_score
import keras as k
import keras.utils.np_utils
import dataset
import word2vec_model
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.layers.embeddings import Embedding

batch = 25
epochs = 5
embdims = 300
filters = 100
filtlen = 2

emb_path = '/Users/Dima/Loyola/Data/Word2Vec/Models/mimic.txt'
data_path = '/Users/Dima/Loyola/Data/Thyme/Deep/Rel/both.txt'
train_size = 78452 # first 78452 indices

if __name__ == "__main__":

  dataset = dataset.DatasetProvider(data_path)
  x, y = dataset.load_data()

  # turn x and y into numpy array among other things
  maxlen = max([len(seq) for seq in x])
  classes = len(set(y))
  x = sequence.pad_sequences(x, maxlen=maxlen)
  y = k.utils.np_utils.to_categorical(np.array(y), classes)  

  print 'x shape:', x.shape
  print 'y shape:', y.shape
  
  train_x = x[:train_size, :]
  train_y = y[:train_size, :]
  test_x = x[train_size:, :]
  test_y = y[train_size:, :]

  print 'train_x shape:', train_x.shape
  print 'train_y shape:', train_y.shape
  print 'test_x shape:', test_x.shape
  print 'test_y shape:', test_y.shape
  
  model = k.models.Sequential()
    
  model.add(Embedding(len(dataset.alphabet),
                      embdims,
                      input_length=maxlen))

  model.add(Convolution1D(nb_filter=filters,
                          filter_length=filtlen,
                          border_mode='valid',
                          activation='relu',
                          subsample_length=1))
  model.add(MaxPooling1D(pool_length=2))
  model.add(Flatten())

  model.add(Dense(classes))
  model.add(Activation('softmax'))
  
  model.compile(loss='categorical_crossentropy',
                optimizer='rmsprop',
                metrics=['accuracy'])
  model.fit(train_x,
            train_y,
            nb_epoch=epochs,
            batch_size=batch,
            verbose=1,
            validation_split=0.1)

  # distribution over classes
  distribution = model.predict(test_x, batch_size=batch)
  # class predictions
  predictions = np.argmax(distribution, axis=1)
  # gold labels
  gold = np.argmax(test_y, axis=1)
  # f1 for each class
  f1 = f1_score(gold, predictions, average=None)

  print 'f1 for contains:', f1[1]
