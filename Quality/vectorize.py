#!/usr/bin/python -B 
import collections, os, csv

PATH = '/Users/Dima/Boston/Data/Temp/Asthma/Text/'
CSVFILE = '/Users/dima/Boston/QualityMetrics/Asthma/data.csv'

def read_file(file):
  """Return a file as a list of words"""      
  
  words = []
  for line in open(file):
    for word in line.split():
      if word.isalpha():
        words.append(word.lower())
    
  return words

def make_alphabet():
  """Do a pass over corpus and map all unique words to dimensions"""
  
  word_counts = collections.Counter()
  for file in os.listdir(PATH):
    words = read_file(PATH + file)
    word_counts.update(words)

  # libsvm indexes start from 1
  index = 1
  # key: word, value: index
  alphabet = collections.OrderedDict() 
  for word, count in word_counts.items():
    if count > 10:
      alphabet[word] = index
      index = index + 1
  
  return alphabet

def make_vectors(alphabet, labels):
  """Convert documents to vectors"""

  for file in os.listdir(PATH):
    vector = []
    document_unique_words = set(read_file(PATH + file))
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
    mrn = file.split('.')[0]
    label = labels[mrn]
    print label2index[label], ' '.join(vector)

def severity_score_labels():
  """Gold labels for severity score compliance data"""

  mrn2label = {} # key: MRN, value: gold label
  dict_reader = csv.DictReader(open(CSVFILE, "rU"))
  for line in dict_reader:
     mrn2label[line['MRN']] = line['IS_SEVERITY_DOCUMENTED']
  
  return mrn2label

if __name__ == "__main__":

  alphabet = make_alphabet()
  labels = severity_score_labels()
  make_vectors(alphabet, labels)
