#!/usr/bin/python -B 
import collections, os, csv

DOCUMENTS = '/Users/dima/Boston/Data/QualityMetrics/Asthma/Text/'
CSVFILE = '/Users/dima/Boston/QualityMetrics/Asthma/data.csv'
LABELS = '/Users/dima/Boston/Data/QualityMetrics/Asthma/labels.txt'
STOPWORDS = '/Users/dima/Boston/Data/Misc/stopwords.txt'
FEATURE2INDEX = './feature2index.txt'
LABEL2INDEX = './label2index.txt'
TRAIN = './train.txt'
MINFREQUENCY = 50

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

def read_bigrams(file, stopwords):
  """Return a file as a list of bi-grams"""

  bigrams = []
  text = open(file).read().lower().replace('\n', ' ')
  words = text.split()
  alpha_words = [word for word in words if word.isalpha()]
  no_junk = [word for word in alpha_words if word not in stopwords]
  for i in range(len(no_junk) - 1):
    bigram = '%s_%s' % (no_junk[i], no_junk[i+1])
    bigrams.append(bigram)

  return bigrams

def make_alphabet(corpus_path, feature_extractors, stopwords):
  """Do a pass over corpus and map all unique features to dimensions"""
  
  feature_counts = collections.Counter()
  for file in os.listdir(corpus_path):
    for feature_extractor in feature_extractors:
      features = feature_extractor(corpus_path + file, stopwords)
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

def make_vectors(corpus_path, alphabet, labels, feature_extractors, stopwords):
  """Convert documents to vectors"""

  training_data = open(TRAIN, 'w')
  
  for file in os.listdir(corpus_path):
    vector = []
    doc_features = []
    for feature_extractor in feature_extractors:
      doc_features.extend(feature_extractor(corpus_path + file, stopwords))
    doc_unique_features = set(doc_features)
    for feature, index in alphabet.items():
      if feature in doc_unique_features:
        vector.append('%s:%s' % (index, 1))
    
    # make label alphabet
    index = 1
    label2index = {}
    label_alphabet_file = open(LABEL2INDEX, 'w')
    for label in set(labels.values()):
      label2index[label] = index
      label_alphabet_file.write('%s|%s\n' % (label, index))
      index = index + 1

    # output vector
    document_name_no_extension = file.split('.')[0]
    label = labels[document_name_no_extension]
    line = '%s %s\n' % (label2index[label], ' '.join(vector))
    training_data.write(line)

def load_labels(dsv_file):
  """Pipe/bar separated file stores the labels"""

  # key: file name (no extension), value: label
  name2label = {}
  for line in open(dsv_file):
    name, label = line.strip().split('|')
    name2label[name] = label

  return name2label

if __name__ == "__main__":

  feature_extractors = [read_unigrams, read_bigrams]

  stopwords = read_stopwords(STOPWORDS)
  alphabet = make_alphabet(DOCUMENTS, feature_extractors, stopwords)
  labels = load_labels(LABELS)
  make_vectors(DOCUMENTS, alphabet, labels, feature_extractors, stopwords)
