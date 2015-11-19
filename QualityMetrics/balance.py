#!/usr/bin/python -B

import random

INFILE = 'train.txt'
OUTFILE = 'balanced.txt'

def balance():
  """Balance a training set"""      

  # key: label, value: list of vectors
  data = {}

  # read examples into an index
  for line in open(INFILE):
    elements = line.split()
    label = elements[0]
    vector = elements[1:]
    if label not in data:
      data[label] = []
    data[label].append(vector)
    
  # find label with smallest number of examples
  smallest_label = ''
  smallest_size = 10000000
  for label, vectors in data.items():
    if len(vectors) < smallest_size:
      smallest_size = len(vectors)
      smallest_label = label

  # pick this number of examples from other labels
  outfile = open(OUTFILE, 'w')
  for label, vectors in data.items():
    for vector in random.sample(vectors, smallest_size):
      line = '%s %s\n' % (label, ' '.join(vector))
      outfile.write(line)
  
if __name__ == "__main__":

  balance()
