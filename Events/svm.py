#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import dataset
import numpy as np
import sklearn as sk
from sklearn.cross_validation import cross_val_score
import sklearn.svm
 
NFOLDS = 2

if __name__ == "__main__":

  dataset = dataset.DatasetProvider()
  examples, labels = dataset.load()

  classifier = sk.svm.LinearSVC()
  scores = cross_val_score(classifier,
                           examples[:10000,:],
                           labels[:10000],
                           cv=NFOLDS,
                           scoring='f1')
  print scores
