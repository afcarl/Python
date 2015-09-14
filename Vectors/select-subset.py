#!/usr/bin/python -B                                                                     
from __future__ import division

import numpy

HEADWORDS = './sharp-uniq-arg-head-words.txt'
ALLVECTORS = '/Users/dima/Boston/Vectors/Models/wikipedia-pubmed-and-PMC-w2v.txt'
DIMENSIONS = 200

def file_as_a_set(filename):
  """Read file and turn it into a set"""

  content = set()
  for line in open(filename):
    content.add(line.strip())

  return content

def select_subset(filename, subset):
  """Process word2vec model file and select subset"""

  vectors = {} # key: word, value: vector as a string
  for line in open(ALLVECTORS):
    elements = line.strip().split()
    word = elements[0]
    if word in subset:
      vector = ' '.join(elements[1:DIMENSIONS + 1])
      vectors[word] = vector
  
  return vectors

def average_vector(vectors):
  """Compute average vector"""

  sum = numpy.zeros(DIMENSIONS)
  for value in vectors.values():
    sum = sum + numpy.fromstring(value, sep=' ')
    # print numpy.fromstring(value, sep=' ')
  
  average = sum / len(vectors)
  return ' '.join(map(str, list(average)))

def main():
  """ """     

  vocabulary = file_as_a_set(HEADWORDS)
  vectors = select_subset(ALLVECTORS, vocabulary)
  average = average_vector(vectors)

  for key, value in vectors.items():
    print key, value
  print "oov", average
    
if __name__ == "__main__":

  main()
