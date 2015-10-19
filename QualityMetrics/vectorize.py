#!/usr/bin/python -B 
import collections, os, csv

DOCUMENTS = '/Users/dima/Boston/Data/QualityMetrics/Asthma/Text/'
CSVFILE = '/Users/dima/Boston/QualityMetrics/Asthma/data.csv'
LABELS = '/Users/dima/Boston/Data/QualityMetrics/Asthma/labels.txt'
MINFREQUENCY = 100

def read_unigrams(file):
  """Return a file as a list of words"""      
  
  words = []
  for line in open(file):
    for word in line.split():
      if word.isalpha():
        words.append(word.lower())
    
  return words

def read_bigrams(file):
  """Return a file as a list of bi-grams"""

  bigrams = []
  for line in open(file):
    words = line.split()
    alpha_words = [word for word in words if word.isalpha()]
    for i in range(len(alpha_words) - 1):
      bigram = '%s_%s' % (alpha_words[i], alpha_words[i+1])
      bigrams.append(bigram.lower())

  return bigrams

def make_alphabet(corpus_path):
  """Do a pass over corpus and map all unique words to dimensions"""
  
  word_counts = collections.Counter()
  for file in os.listdir(corpus_path):
    words = read_bigrams(corpus_path + file)
    word_counts.update(words)

  # libsvm indexes start from 1
  index = 1
  # remember the order in which words were inserted
  word2index = collections.OrderedDict() 
  for word, count in word_counts.items():
    if count >= MINFREQUENCY:
      word2index[word] = index
      index = index + 1
  
  return word2index

def make_vectors(corpus_path, alphabet, labels):
  """Convert documents to vectors"""

  for file in os.listdir(corpus_path):
    vector = []
    document_unique_words = set(read_bigrams(corpus_path + file))
    for word, index in alphabet.items():
      if word in document_unique_words:
        vector.append("%s:%s" % (index, 1))
    
    # make label alphabet
    index = 1
    label2index = {}
    for label in set(labels.values()):
      label2index[label] = index
      index = index + 1

    # output vector
    document_name_no_extension = file.split('.')[0]
    label = labels[document_name_no_extension]
    print label2index[label], ' '.join(vector)

def load_labels_from_file(dsv_file):
  """Pipe/bar separated file stores the labels"""

  # key: file name (no extension), value: label
  name2label = {}
  for line in open(dsv_file):
    name, label = line.strip().split('|')
    name2label[name] = label

  return name2label

if __name__ == "__main__":
  
  alphabet = make_alphabet(DOCUMENTS)
  labels = load_labels_from_file(LABELS)
  make_vectors(DOCUMENTS, alphabet, labels)
