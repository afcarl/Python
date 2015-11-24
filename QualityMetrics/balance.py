#!/usr/bin/python -B

import random, shutil, os, os.path

DOCUMENTS = '/Users/dima/Boston/Data/QualityMetrics/Text/'
BALANCED = '/Users/dima/Boston/Data/QualityMetrics/Balanced/'
INFILE = './train.txt'
OUTFILE = './balanced.txt'

def balance_training_files():
  """Ensure each class has same number of files"""

  # find number of files in smallest subdir
  smallest_size = 100000
  for subdir in os.listdir(DOCUMENTS):
    size = len(os.listdir(os.path.join(DOCUMENTS, subdir)))
    if size < smallest_size:
      smallest_size = size

  # create directory structure
  if os.path.exists(BALANCED):
    shutil.rmtree(BALANCED)
  os.makedirs(BALANCED)
  os.makedirs(os.path.join(BALANCED, 'Yes'))
  os.makedirs(os.path.join(BALANCED, 'No'))

  # make sure each subdir has same number of files
  for subdir in os.listdir(DOCUMENTS):
    files = os.listdir(os.path.join(DOCUMENTS, subdir))
    for file in random.sample(files, smallest_size):
      source = os.path.join(DOCUMENTS, subdir, file)
      target = os.path.join(BALANCED, subdir)
      shutil.copy(source, target)

def balance_libsvm_data():
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
  smallest_size = 1000000
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

  balance_training_files()
