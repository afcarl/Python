#!/usr/bin/python -B 
import collections, os

PATH = '/Users/Dima/Boston/Data/Temp/Asthma/SampleText/'

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

def make_vectors(alphabet):
  """Convert documents to vectors"""

  for file in os.listdir(PATH):
    vector = []
    document_unique_words = set(read_file(PATH + file))
    for word, index in alphabet.items():
      if word in document_unique_words:
        vector.append("%s:%s" % (index, 1))
    print ' '.join(vector)

if __name__ == "__main__":

  alphabet = make_alphabet()
  make_vectors(alphabet)
