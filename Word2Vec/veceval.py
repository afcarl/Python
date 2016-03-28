#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy as np
import sklearn as sk
import sklearn.cross_validation
import sklearn.svm
import os, os.path

NFOLDS = 10

if __name__ == "__main__":

  pos_examples = np.loadtxt('pos.txt')
  pos_labels = [1] * pos_examples.shape[0]
  neg_examples = np.loadtxt('neg.txt')
  neg_labels = [0] * neg_examples.shape[0]
  examples = np.vstack((pos_examples, neg_examples))
  labels = np.array(pos_labels + neg_labels)
  
  scores = []
  folds = sk.cross_validation.KFold(len(labels), n_folds=NFOLDS)

  for train_indices, test_indices in folds:
    train_x = examples[train_indices]
    train_y = labels[train_indices]
    test_x = examples[test_indices]
    test_y = labels[test_indices]
    classifier = sk.svm.LinearSVC()
    model = classifier.fit(train_x, train_y)
    accuracy = classifier.score(test_x, test_y)
    scores.append(accuracy)
  
  print np.mean(scores)
  
