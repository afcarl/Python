#!/usr/bin/python -B

"""
It seems like counts rather than tfidf work better. 
Also check out 'binary=True' option to count vectorizer. Might work better.
"""

import sklearn as sk
import numpy as np
import sklearn.datasets
import sklearn.feature_extraction.text
import sklearn.cross_validation
import sklearn.naive_bayes
import sklearn.svm

NOTES = '/Users/dima/Boston/Data/QualityMetrics/Balanced/'
WORDLIST = set(['severe', 'persistent', 'mild', 'intermittent'])
NFOLDS = 5

# one, two, three, four, five, six, seven, eight, nine
# WORDLIST = set(['four', 'five']) # doesn't work for 'one'

def keyword_contexts(document):
  """Keep certain kind of bi-grams"""

  words = document.lower().replace('\n', ' ').split()
  alpha_words = [word for word in words if word.isalpha()]

  selected_sequences = [] 
  selected_indices = set()
  for i in range(1, len(alpha_words) - 1):
    if alpha_words[i] in WORDLIST:
      if i - 1 not in selected_indices:
        selected_sequences.append(alpha_words[i - 1])
        selected_indices.add(i - 1)
      if i not in selected_indices:
        selected_sequences.append(alpha_words[i])
        selected_indices.add(i)
      if i + 1 not in selected_indices:
        selected_sequences.append(alpha_words[i + 1])
        selected_indices.add(i + 1)

  return ' '.join(selected_sequences)

def main():
  """ """      

  bunch = sk.datasets.load_files(NOTES)

  # raw occurences
  vectorizer = sk.feature_extraction.text.CountVectorizer(
    ngram_range=(2, 2), 
    stop_words='english',
    min_df=50,
    preprocessor=keyword_contexts)  
  counts = vectorizer.fit_transform(bunch.data)
  
  # print features to file
  feature_file = open('features.txt', 'w')
  for feature in vectorizer.get_feature_names():
    feature_file.write(feature + '\n')
  
  # tf-idf 
  tf = sk.feature_extraction.text.TfidfTransformer()
  tfidf = tf.fit_transform(counts)
  
  scores = []
  folds = sk.cross_validation.KFold(len(bunch.data), n_folds=NFOLDS)
  for train_indices, test_indices in folds:
    train_x = tfidf[train_indices]
    train_y = bunch.target[train_indices]
    test_x = tfidf[test_indices]
    test_y = bunch.target[test_indices]
    classifier = sk.svm.LinearSVC().fit(train_x, train_y)
    scores.append(classifier.score(test_x, test_y))
  
  print np.mean(scores)

if __name__ == "__main__":

  main()
  # print keyword_contexts('one two three four five six seven eight nine')
