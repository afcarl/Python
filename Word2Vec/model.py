#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy

class Model:
  """Represents a word2vec model"""

  def __init__(self, path):
    """Initiaize from a word2vec model file"""
                
    self.path = path
    self.count = None      # number of vectors
    self.dimensions = None # number of dimensions
    self.vectors = {}      # key: word, value: vector
        
  def load(self):
    """Load word2vec model file into memory"""

    with open(self.path) as file:
      for line in file:
        elements = line.strip().split()
        if len(elements) < 3: # parse header
          self.count = int(elements[0])
          self.dimensions = int(elements[1])
          continue
        word = elements[0]
        vector = [float(element) for element in elements[1:self.dimensions+1]]
        self.vectors[word] = numpy.array(vector)

  def average_words(self, words):
    """Compute average vector for a list of words"""

    sum = numpy.zeros(self.dimensions)
    for word in words:
      sum = sum + self.vectors[word]
    return sum / len(words)
        
if __name__ == "__main__":

  path = '/Users/Dima/Boston/Vectors/Models/mimic.txt'
  model = Model(path)
  model.load()

  average = model.average_words(['intrathoric', 'clubbed', 'wanning'])
  print average
  
