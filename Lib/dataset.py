#!/usr/bin/env python

import numpy as np

import sys
sys.dont_write_bytecode = True

import ConfigParser

import glob, string, collections, operator

label2int = {
  'none':0,
  'contains':1,
  'contains-1':2
  }

# will have to do this eventually
# label2int = {
#   'none': 0,
#   'contains': 1,
#   'contains-1': 2,
#   'before': 3,
#   'before-1': 4,
#   'begins-on': 5,
#   'begins-on-1': 6,
#   'ends-on': 7,
#   'ends-on-1': 8,
#   'overlap': 9,
#   'overlap-1': 10,
# }

class DatasetProvider:
  """THYME relation data"""
  
  def __init__(self, file_names):
    """Index words by frequency in a list of files"""

    self.alphabet = {} # words indexed by frequency

    unigrams = [] # read entire corpus into a list
    for file_name in file_names:
      for line in open(file_name):
        label, text = line.strip().split('|')
        unigrams.extend(text.split())

    index = 1 # zero used to encode unknown words
    unigram_counts = collections.Counter(unigrams)
    self.alphabet['oov_word'] = 0
    for unigram, count in unigram_counts.most_common():
      self.alphabet[unigram] = index
      index = index + 1

  def load(self, path):
    """Convert sentences (examples) into lists of indices"""

    examples = []
    labels = []
    for line in open(path):
      label, text = line.strip().split('|')
      example = []
      for unigram in text.split():
        example.append(self.alphabet[unigram])
      examples.append(example)
      labels.append(label2int[label])

    return examples, labels

if __name__ == "__main__":

  cfg = ConfigParser.ConfigParser()
  cfg.read('settings.ini')

  dataset = DatasetProvider([cfg.get('data', 'train'),
                             cfg.get('data', 'test')])
  print 'alphabet size:', len(dataset.alphabet)

  x,y = dataset.load(cfg.get('data', 'test'))

  print 'max seq len:', max([len(s) for s in x])
  print 'number of examples:', len(x)
  print 'number of labels:', len(set(y))
  print 'label counts:', collections.Counter(y)
  print 'first 10 examples:', x[:10]
  print 'class proportions:'
  counter = collections.Counter(y)
  for label in counter:
    print label, counter[label] / float(len(y)), float(len(y)) / counter[label]
