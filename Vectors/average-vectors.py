#!/usr/bin/python -B                                                                     
from __future__ import division

import numpy

ALLVECTORS = '/Users/dima/Boston/Vectors/Models/PubMed-w2v.txt'

def average_vectors():
  """Average vectors in a model file. Print vectors."""

  total_vectors = 0
  sum = None

  for line in open(ALLVECTORS):
    
    elements = line.strip().split()
    if len(elements) < 10: # read info line
      dimensions = int(elements[1])
      sum = numpy.zeros(dimensions)
      continue

    word = elements[0]
    # some non-numeric chars at the end, so can't do [1:]
    vector = ' '.join(elements[1:dimensions + 1]) 
    print word, vector
    sum = sum + numpy.fromstring(vector, sep=' ')
    total_vectors = total_vectors + 1

  average = sum / total_vectors
  return ' '.join(map(str, list(average)))

if __name__ == "__main__":

  average = average_vectors()
  print "oov", average
