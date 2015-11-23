#!/usr/bin/python -B

import sklearn
import sklearn.datasets
import sklearn.feature_extraction.text
import sklearn.cross_validation
import sklearn.naive_bayes

NOTES = '/Users/dima/Boston/Data/QualityMetrics/Text'

def main():
  """ """      

  # bunch = sklearn.datasets.load_files(NOTES)
  categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
  bunch = sklearn.datasets.fetch_20newsgroups(subset='train', categories=categories)

  # raw occurences
  vectorizer = sklearn.feature_extraction.text.CountVectorizer()
  counts = vectorizer.fit_transform(bunch.data)
  
  # tf-idf 
  tf = sklearn.feature_extraction.text.TfidfTransformer()
  tfidf = tf.fit_transform(counts)

  folds = sklearn.cross_validation.KFold(len(bunch.data), n_folds=5)
  for train_indices, test_indices in folds:
    train_x = tfidf[train_indices]
    train_y = bunch.target[train_indices]
    test_x = tfidf[test_indices]
    test_y = bunch.target[test_indices]
    classifier = sklearn.naive_bayes.MultinomialNB().fit(train_x, train_y)
    acc = classifier.score(test_x, test_y)
    print acc

if __name__ == "__main__":

  main()
