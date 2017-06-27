#!/usr/bin/env python
import numpy as np
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

notes_root = '/Users/Dima/Loyola/Data/Ards/Cuis/'
feature_list = './features.txt'
# ngram_range = (1, 2)
ngram_range = (1, 1)
min_df = 50

def run_experiment():
  """Split into train and test and run an experiment"""

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

  x_train, x_test, y_train, y_test = train_test_split(tfidf_matrix,
                                                      bunch.target,
                                                      test_size = 0.2,
                                                      random_state=1)

  classifier = LinearSVC(class_weight='balanced')
  model = classifier.fit(x_train, y_train)
  predicted = classifier.predict(x_test)

  precision = precision_score(y_test, predicted, pos_label=1)
  recall = recall_score(y_test, predicted, pos_label=1)
  f1 = f1_score(y_test, predicted, pos_label=1)
  print 'p =', precision
  print 'r =', recall
  print 'f1 =', f1

if __name__ == "__main__":

  run_experiment()
