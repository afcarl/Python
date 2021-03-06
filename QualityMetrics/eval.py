#!/usr/bin/python -B

import sklearn as sk
import numpy as np
import sklearn.datasets
import sklearn.feature_extraction.text
import sklearn.cross_validation
import sklearn.naive_bayes
import sklearn.svm
import locations

WORDLIST = set(['severe', 'persistent', 'mild', 'intermittent', 'moderate'])
VOCABULARY = ['severe asthma', 'persistent asthma', 'mild asthma', 
              'intermittent asthma', 'moderate asthma', 'mild persistent', 
              'mild intermittent', 'moderate persistent', 'severe persistent']
FEATUREFILE = './features.txt'
NFOLDS = 5
NGRAMRANGE = (2, 2)
MINDF = 50

def keyword_contexts(document):
  """Keep words on both sides of each key word"""

  words = document.lower().replace('\n', ' ').split()
  alpha_words = [word for word in words if word.isalpha()]

  selected_indices = []
  for index, word in enumerate(alpha_words):
    if word in WORDLIST:
      if index > 0:                    # except first word in doc
        selected_indices.append(index - 1)
      selected_indices.append(index)
      if index < len(alpha_words) - 1: # except last word in doc
        selected_indices.append(index + 1)

  selected_words = []
  for selected_index in sorted(set(selected_indices)):
    selected_words.append(alpha_words[selected_index])

  return ' '.join(selected_words)

def run_cross_validation(notes_dir):
  """Run n-fold CV and return average accuracy"""      

  bunch = sk.datasets.load_files(notes_dir)

  # raw occurences
  vectorizer = sk.feature_extraction.text.CountVectorizer(
    ngram_range=NGRAMRANGE, 
    stop_words='english',
    min_df=MINDF ,
    vocabulary=None,
    binary=False,
    preprocessor=keyword_contexts)  
  count_matrix = vectorizer.fit_transform(bunch.data)
  
  # print features to file for debugging
  feature_file = open(FEATUREFILE, 'w')
  for feature in vectorizer.get_feature_names():
    feature_file.write(feature + '\n')
  
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

  run_cross_validation(locations.BALANCED)
