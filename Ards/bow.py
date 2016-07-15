#!/usr/bin/env python                                                                     
import sklearn as sk
import numpy as np
import sklearn.datasets
import sklearn.feature_extraction.text
import sklearn.cross_validation
import sklearn.svm

notes_root = '/Users/Dima/Loyola/Mount/ards/text'
feature_list = './features.txt'
num_folds = 5
ngram_range = (1, 2)
min_df = 5

def run_cross_validation():
  """Run n-fold CV and return average accuracy"""      

  bunch = sk.datasets.load_files(notes_root)

  # raw occurences
  vectorizer = sk.feature_extraction.text.CountVectorizer(
    ngram_range=ngram_range, 
    stop_words='english',
    min_df=min_df ,
    vocabulary=None,
    binary=False)
  count_matrix = vectorizer.fit_transform(bunch.data)
  
  # print features to file for debugging
  feature_file = open(feature_list, 'w')
  for feature in vectorizer.get_feature_names():
    feature_file.write(feature + '\n')
  
  # tf-idf 
  tf = sk.feature_extraction.text.TfidfTransformer()
  tfidf_matrix = tf.fit_transform(count_matrix)
  
  scores = []
  folds = sk.cross_validation.KFold(len(bunch.data), n_folds=num_folds)
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
