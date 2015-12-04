#!/usr/bin/python -B 
import collections, os, csv

WORDLIST = set(['severe', 'persistent', 'mild', 'intermittent'])
CLASSDIRS = ['Yes/', 'No/']
STOPWORDS = '/Users/dima/Boston/Data/Misc/stopwords.txt'
FEATURE2INDEX = './feature2index.txt'
LABEL2INDEX = './label2index.txt'
TRAIN = './train.txt'
MINFREQUENCY = 100

def read_stopwords(stopword_file):
  """Read stopwords from a file into a set"""

  stopwords = []
  for line in open(stopword_file):
    if not line.startswith('#'):
      stopwords.append(line.strip())

  return set(stopwords)

def read_unigrams(file, stopwords):
  """Return a file as a list of words"""      
  
  unigrams = []
  text = open(file).read().lower().replace('\n', ' ')
  words = text.split()
  alpha_words = [word for word in words if word.isalpha()]
  no_junk = [word for word in alpha_words if word not in stopwords]
  for word in no_junk:
    unigrams.append(word)
      
  return unigrams

def read_bigrams(file, stopwords, word_list = WORDLIST):
  """Return a file as a list of bi-grams"""

  bigrams = []
  text = open(file).read().lower().replace('\n', ' ')
  words = text.split()
  alpha_words = [word for word in words if word.isalpha()]
  no_junk = [word for word in alpha_words if word not in stopwords]
  for i in range(len(no_junk) - 1):
    if len(word_list) == 0:
      # include all bigrams
      bigram = '%s_%s' % (no_junk[i], no_junk[i+1])
    else:
      # include only bigrams where one of the words is in word list
      if (no_junk[i] in word_list) or (no_junk[i+1] in word_list):
        bigram = '%s_%s' % (no_junk[i], no_junk[i+1])
      else:
        continue
    bigrams.append(bigram)

  return bigrams

def make_alphabet(corpus_path, feature_extractors, stopwords):
  """Do a pass over corpus and map all unique features to dimensions"""
  
  feature_counts = collections.Counter()
  for label in CLASSDIRS:
    for file in os.listdir(corpus_path + label):
      for feature_extractor in feature_extractors:
        features = feature_extractor(corpus_path + label + file, stopwords)
        feature_counts.update(features)

  # libsvm indexes start from 1
  index = 1
  # remember the order in which features were inserted
  feature2index = collections.OrderedDict() 
  for feature, count in feature_counts.items():
    if count >= MINFREQUENCY:
      feature2index[feature] = index
      index = index + 1
  
  feature_alphabet_file = open(FEATURE2INDEX, 'w')
  for feature, index in feature2index.items():
    feature_alphabet_file.write('%s|%d\n' % (feature, index))

  return feature2index

def make_vectors(corpus_path, alphabet, feature_extractors, stopwords):
  """Convert documents to vectors"""

  # make label alphabet
  index = 1
  label2index = {}
  label_alphabet_file = open(LABEL2INDEX, 'w')
  for label in CLASSDIRS:
    label2index[label] = index
    label_alphabet_file.write('%s|%s\n' % (label, index))
    index = index + 1
  
  training_data = open(TRAIN, 'w')
  for label in CLASSDIRS:
    for file in os.listdir(corpus_path + label):
      vector = []
      doc_features = []
      for feature_extractor in feature_extractors:
        doc_features.extend(feature_extractor(corpus_path + label + file, stopwords))
      doc_unique_features = set(doc_features)
      for feature, index in alphabet.items():
        if feature in doc_unique_features:
          vector.append('%s:%s' % (index, 1))

      # output vector
      line = '%s %s\n' % (label2index[label], ' '.join(vector))
      training_data.write(line)

if __name__ == "__main__":

  feature_extractors = [read_bigrams]

  stopwords = read_stopwords(STOPWORDS)
  alphabet = make_alphabet(DOCUMENTS, feature_extractors, stopwords)
  make_vectors(DOCUMENTS, alphabet, feature_extractors, stopwords)
