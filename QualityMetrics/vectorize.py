#!/usr/bin/python -B 
import collections, os, csv

DOCUMENTS = '/Users/dima/Boston/Data/QualityMetrics/Asthma/Text/'
CSVFILE = '/Users/dima/Boston/QualityMetrics/Asthma/data.csv'
LABELS = '/Users/dima/Boston/Data/QualityMetrics/Asthma/labels.txt'
WORD2INDEX = './word2index.txt'
LABEL2INDEX = './label2index.txt'
TRAIN = './train.txt'
MINFREQUENCY = 50

def read_unigrams(file):
  """Return a file as a list of words"""      
  
  unigrams = []
  text = open(file).read().replace('\n', ' ')
  words = text.split()
  alpha_words = [word for word in words if word.isalpha()]
  for word in alpha_words:
    unigrams.append(word.lower())
      
  return unigrams

def read_bigrams(file):
  """Return a file as a list of bi-grams"""

  bigrams = []
  text = open(file).read().replace('\n', ' ')
  words = text.split()
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
  
  word_alphabet_file = open(WORD2INDEX, 'w')
  for word, index in word2index.items():
    word_alphabet_file.write('%s|%d\n' % (word, index))

  return word2index

def make_vectors(corpus_path, alphabet, labels):
  """Convert documents to vectors"""

  training_data = open(TRAIN, 'w')
  
  for file in os.listdir(corpus_path):
    vector = []
    document_unique_words = set(read_bigrams(corpus_path + file))
    for word, index in alphabet.items():
      if word in document_unique_words:
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
  
  alphabet = make_alphabet(DOCUMENTS)
  labels = load_labels(LABELS)
  make_vectors(DOCUMENTS, alphabet, labels)
