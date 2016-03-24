#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy as np
import sklearn as sk
import sklearn.datasets
import sklearn.feature_extraction.text
import sklearn.cross_validation
import sklearn.svm

DATADIR = '/Users/Dima/Soft/CnnBritz/cnn-text-classification-tf/data/rt-polaritydata'
NFOLDS = 5
NGRAMRANGE = (1, 1)
MINDF = 0

def run_cross_validation():
  """Run n-fold CV and return average accuracy"""      

  bunch = sk.datasets.load_files(DATADIR)

  # raw occurences
  vectorizer = sk.feature_extraction.text.CountVectorizer(
    ngram_range=NGRAMRANGE, 
    stop_words=None,
    min_df=MINDF ,
    vocabulary=None,
    binary=False,
    preprocessor=None)  
  count_matrix = vectorizer.fit_transform(bunch.data)
  
  # tf-idf 
  tf = sk.feature_extraction.text.TfidfTransformer()
  tfidf_matrix = tf.fit_transform(count_matrix)
  
  scores = []
  folds = sk.cross_validation.KFold(len(bunch.data), n_folds=NFOLDS)
  for train_indices, test_indices in folds:
    train_x = tfidf_matrix[train_indices]
    train_y = bunch.target[train_indices]
    test_x = tfidf_matrix[test_indices]
    test_y = bunch.target[test_indices]
    classifier = sk.svm.LinearSVC()
    model = classifier.fit(train_x, train_y)
    accuracy = classifier.score(test_x, test_y)
    scores.append(accuracy)
  
  print np.mean(scores)

if __name__ == "__main__":

  run_cross_validation()
