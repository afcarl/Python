#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import glob, string

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

    print len(set(unigrams))

  def read_unigrams(self, file_name):
    """Return a file as a list of words"""
    
    unigrams = []
    with open(file_name) as file:
      for line in file:
        printable = ''.join(c for c in line if c in string.printable)
        unigrams.extend(printable.split())

    return unigrams

if __name__ == "__main__":

  dataset = Dataset()
  dataset.make_alphabet()
