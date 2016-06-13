#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

import glob, string, collections, operator

label2int = {
  'none':0,
  'contains':1,
  'before':2,
  'begins-on':3,
  'continues':4,
  'ends-on':5,
  'initiates':6,
  'overlap':7,
  'reinitiates':8,
  'terminates':9
  }

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

  dataset = DatasetProvider([properties.train, properties.test])
  print 'alphabet size:', len(dataset.alphabet)
  x,y = dataset.load(properties.test)
  print 'max seq len:', max([len(s) for s in x])
  print 'number of examples:', len(x)
  print 'number of labels:', len(set(y))
  print 'label counts:', collections.Counter(y)
  print 'first 10 examples:', x[:10]
