#!/usr/bin/env python
import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score

notes_root = '/Users/Dima/Loyola/Data/Ards/Cuis/'
feature_list = './features.txt'
num_folds = 5
ngram_range = (1, 1) # use unigrams for cuis
min_df = 0

def run_cross_validation():
  """Run n-fold CV and return average accuracy"""

  bunch = load_files(notes_root)
  print 'positive class:', bunch.target_names[1]
  print 'negative class:', bunch.target_names[0]

  # raw occurences
  vectorizer = CountVectorizer(
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
  tf = TfidfTransformer()
  tfidf_matrix = tf.fit_transform(count_matrix)

  classifier = LinearSVC(class_weight='balanced', C=1)
  cv_scores = cross_val_score(
    classifier,
    tfidf_matrix,
    bunch.target,
    scoring='f1',
    cv=num_folds)
  
  print 'fold f1s:', cv_scores
  print 'average f1:', np.mean(cv_scores)
  print 'standard devitation:', np.std(cv_scores)
  
if __name__ == "__main__":

  run_cross_validation()
