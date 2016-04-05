#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import glob, string, collections, operator

PATH = '/Users/Dima/Loyola/Data/RtPolarity/rt-polarity.*'

class Dataset:
  """Interface to RT sentiment data"""
  
  def __init__(self, max_features=None):
    """Index words by overall frequency in the dataset"""

    self.alphabet = {} # words indexed by frequency

    unigrams = []
    for file_name in glob.glob(PATH):
      for line in open(file_name):
        printable = ''.join(c for c in line if c in string.printable)
        unigrams.extend(printable.split())

    index = 1 # zero used to encode unknown words
    unigram_counts = collections.Counter(unigrams)
    for unigram, count in unigram_counts.most_common(max_features):
      self.alphabet[unigram] = index
      index = index + 1

  def load_data(self):
    """Convert sentences (examples) into lists of indices"""

    examples = []
    labels = []
    for file_name in glob.glob(PATH):
      for line in open(file_name):
        example = []
        printable = ''.join(c for c in line if c in string.printable)
        for unigram in printable.split():
          if unigram in self.alphabet:
            example.append(self.alphabet[unigram])
        examples.append(example)
        labels.append(file_name.split('.')[1])

    return examples, labels

if __name__ == "__main__":

  dataset = Dataset(max_features=5)
  print 'vocabulary size:', len(dataset.alphabet)
  x,y = dataset.load_data()
  print x[600], y[600]
