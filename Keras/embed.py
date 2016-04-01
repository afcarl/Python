#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy as np
import sklearn as sk
import sklearn.cross_validation
import sklearn.feature_extraction.text
import os, os.path
import keras as k
import keras.models
import keras.layers.core
import keras.layers.embeddings
import keras.utils.np_utils
import svm_words

NFOLDS = 10
BATCH = 32
EPOCHS = 5
CLASSES = 2
MINDF = 0
DIMENSIONS = 100

if __name__ == "__main__":

  np.random.seed(1337) 
  bunch = svm_words.make_bunch()

  vectorizer = sk.feature_extraction.text.CountVectorizer(min_df=MINDF)
  count_matrix = vectorizer.fit_transform(bunch.data)
  seqs = [np.nonzero(row)[0].tolist() for row in count_matrix.toarray()]
  sequences = np.array(seqs)

  labels = np.array(bunch.target)
  labels[labels == 'neg'] = 0
  labels[labels == 'pos'] = 1
  
  labels_one_hot = k.utils.np_utils.to_categorical(labels, CLASSES)
  
  scores = []
  folds = sk.cross_validation.KFold(len(labels), n_folds=NFOLDS)

  for train_indices, test_indices in folds:
    train_x = sequences[train_indices]
    train_y = labels_one_hot[train_indices]
    test_x = sequences[test_indices]
    test_y = labels_one_hot[test_indices]
    
    model = k.models.Sequential()

    model.add(k.layers.embeddings.Embedding(count_matrix.shape[1],
                                            DIMENSIONS, input_length=100))
    # model.add(k.layers.core.Dropout(0.25))
    
    model.add(k.layers.core.Dense(1128))
    model.add(k.layers.core.Activation('relu'))
    model.add(k.layers.core.Dropout(0.3))

    model.add(k.layers.core.Dense(128))
    model.add(k.layers.core.Activation('relu'))
    model.add(k.layers.core.Dropout(0.3))

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
  
