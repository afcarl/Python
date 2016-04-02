#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import glob, string, collections, operator

PATH = '/Users/Dima/Loyola/Data/RtPolarity/rt-polarity.*'

class Dataset:
  """Interface to RT sentiment data"""

  def __init__(self):
    """ """

  def make_alphabet(self):
    """ """

    unigrams = []
    for file_name in glob.glob(PATH):
      print 'reading file:', file_name
      for line in open(file_name):
        printable = ''.join(c for c in line if c in string.printable)
        unigrams.extend(printable.split())

    alphabet = {} # key: unigram, value: index
    index = 1     # zero used to encode unknown words
    unigram_counts = collections.Counter(unigrams)
    for unigram, count in unigram_counts.most_common():
      alphabet[unigram] = index
      index = index + 1

    return alphabet

if __name__ == "__main__":

  dataset = Dataset()
  dataset.make_alphabet()
