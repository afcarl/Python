#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import glob, string, collections, operator

PATH = '/Users/Dima/Loyola/Data/RtPolarity/rt-polarity.*'

class Dataset:
  """Interface to RT sentiment data"""
  
  def __init__(self):
    """ """

    self.alphabet = {} # key: unigram, value: index

  def make_alphabet(self):
    """Words indexed by overall frequency in the dataset"""

    unigrams = []
    for file_name in glob.glob(PATH):
      for line in open(file_name):
        printable = ''.join(c for c in line if c in string.printable)
        unigrams.extend(printable.split())

    index = 1 # zero used to encode unknown words
    unigram_counts = collections.Counter(unigrams)
    for unigram, count in unigram_counts.most_common():
      self.alphabet[unigram] = index
      index = index + 1

  def get_examples(self):
    """Convert sentences (examples) into lists of indices"""

    examples = []
    for file_name in glob.glob(PATH):
      for line in open(file_name):
        example = []
        printable = ''.join(c for c in line if c in string.printable)
        for unigram in printable.split():
          example.append(self.alphabet[unigram])
        examples.append(example)

    return examples

if __name__ == "__main__":

  dataset = Dataset()
  dataset.make_alphabet()
  examples = dataset.get_examples()
  print examples[6]
