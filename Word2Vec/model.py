#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy, os, os.path

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
        if len(elements) < 5: # parse header
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
      if word in self.vectors:
        sum = sum + self.vectors[word]

    return sum / len(words)

  def words_to_vectors(self, infile, outfile):
    """Convert text from infile to vectors and save in outfile"""

    matrix = []
    with open(infile) as file:
      for line in file:
        average = self.average_words(line.split())
        matrix.append(list(average))

    numpy.savetxt(outfile, numpy.array(matrix))
      
if __name__ == "__main__":

  path = '/Users/Dima/Loyola/Data/Word2Vec/Models/GoogleNews-vectors-negative300.txt'
  model = Model(path)
  model.load()
  print 'model loaded'

  data = '/Users/Dima/Soft/CnnBritz/cnn-text-classification-tf/data/rt-polaritydata/'
  model.words_to_vectors(os.path.join(data, 'rt-polarity.neg'), 'neg.txt')
  model.words_to_vectors(os.path.join(data, 'rt-polarity.pos'), 'pos.txt')
