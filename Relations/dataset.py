#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import glob, string, collections, operator

data_path = '/Users/Dima/Temp/out.txt'
label2int = {
  'none':0,
  'before':1,
  'begins-on':2,
  'contains':3,
  'continues':4,
  'ends-on':5,
  'initiates':6,
  'overlap':7,
  'reinitiates':8,
  'terminates':9
  }

class DatasetProvider:
  """Interface to RT sentiment data"""
  
  def __init__(self):
    """Index words by overall frequency in the dataset"""

    self.alphabet = {} # words indexed by frequency

    unigrams = [] # read entire corpus into a list
    for line in open(data_path):
      _, text = line.strip().split('|')
      unigrams.extend(text.split())

    index = 1 # zero used to encode unknown words
    unigram_counts = collections.Counter(unigrams)
    self.alphabet['unknown_word'] = 0
    for unigram, count in unigram_counts.most_common():
      self.alphabet[unigram] = index
      index = index + 1

  def load_data(self):
    """Convert sentences (examples) into lists of indices"""

    examples = []
    labels = []
    for line in open(data_path):
      label, text = line.strip().split('|')
      example = []
      for unigram in text.split():
        if unigram in self.alphabet:
          example.append(self.alphabet[unigram])
      examples.append(example)
      labels.append(label)

    return examples, labels

if __name__ == "__main__":

  dataset = DatasetProvider()
  print 'alphabet size:', len(dataset.alphabet)
  x,y = dataset.load_data()
  print 'max seq len:', max([len(s) for s in x])
