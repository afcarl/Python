#!/usr/bin/python -B

import sklearn as sk
import numpy as np
import sklearn.datasets
import sklearn.feature_extraction.text
import sklearn.cross_validation
import sklearn.naive_bayes
import sklearn.svm

NOTES = '/Users/dima/Boston/Data/QualityMetrics/Balanced/'

def main():
  """ """      

  bunch = sk.datasets.load_files(NOTES)

  # raw occurences
  vectorizer = sk.feature_extraction.text.CountVectorizer(
    ngram_range=(2, 2), 
    stop_words='english',
    min_df=3)  
  counts = vectorizer.fit_transform(bunch.data)
  
  # tf-idf 
  tf = sk.feature_extraction.text.TfidfTransformer()
  tfidf = tf.fit_transform(counts)
  
  scores = []
  folds = sk.cross_validation.KFold(len(bunch.data), n_folds=5)
  for train_indices, test_indices in folds:
    train_x = tfidf[train_indices]
    train_y = bunch.target[train_indices]
    test_x = tfidf[test_indices]
    test_y = bunch.target[test_indices]
    # classifier = sk.naive_bayes.MultinomialNB().fit(train_x, train_y)
    classifier = sk.svm.LinearSVC().fit(train_x, train_y)
    scores.append(classifier.score(test_x, test_y))
  
  print np.mean(scores)

if __name__ == "__main__":

  main()
