#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import numpy, os, os.path

class Model:
  """Represents a word2vec model"""

  def __init__(self, path):
    """Initiaize from a word2vec model file"""
                
    self.count = None      # number of vectors
    self.dimensions = None # number of dimensions
    self.vectors = {}      # key: word, value: numpy vector
        
    with open(path) as file:
      for line in file:
        elements = line.strip().split()
        if len(elements) < 5: # parse header
          self.count = int(elements[0])
          self.dimensions = int(elements[1])
          continue
        word = elements[0]
        vector = [float(element) for element in elements[1:self.dimensions+1]]
        self.vectors[word] = numpy.array(vector)

  def subset_vectors(self, alphabet):
    """Return vectors for items in alphabet"""

    vecs = numpy.zeros((len(alphabet), 300))

    for word, index in alphabet.items():
      if word in self.vectors:
        vecs[index, :] = self.vectors[word]
      else:
        vecs[index, :] = numpy.random.uniform(low=0.0, high=1.0, size=300)

    return vecs

  def average_words(self, words):
    """Compute average vector for a list of words"""

    words_found = 0 # words in vocabulary
    sum = numpy.zeros(self.dimensions)
    for word in words:
      if word in self.vectors:
        sum = sum + self.vectors[word]
        words_found = words_found + 1

    if words_found == 0:
      return sum
    else:
      return sum / words_found

  def words_to_vectors(self, infile, outfile):
    """Convert texts from infile to vectors and save in outfile"""

    matrix = []
    with open(infile) as file:
      for line in file:
        average = self.average_words(line.split())
        matrix.append(list(average))

    numpy.savetxt(outfile, numpy.array(matrix))
      
if __name__ == "__main__":

  path = '/Users/Dima/Loyola/Data/Word2Vec/Models/GoogleNews-vectors-negative300.txt'
  model = Model(path)

  data = '/Users/Dima/Soft/CnnBritz/cnn-text-classification-tf/data/rt-polaritydata/'
  model.words_to_vectors(os.path.join(data, 'rt-polarity.neg'), 'neg.txt')
  model.words_to_vectors(os.path.join(data, 'rt-polarity.pos'), 'pos.txt')
