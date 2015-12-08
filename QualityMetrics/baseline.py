#!/usr/bin/python -B

import locations
import os

CLASSDIRS = ['Yes', 'No']
VOCABULARY = ['severe asthma', 'persistent asthma', 'mild asthma', 
              'intermittent asthma', 'moderate asthma']

def counting():
  """Count the number of times each vocabulary item is seen"""

  counts = {} # key: label, total count of vocabulary items
  counts[CLASSDIRS[0]] = 0
  counts[CLASSDIRS[1]] = 0

  for label in CLASSDIRS:
    for file in os.listdir(locations.BALANCED + label):
      path = os.path.join(locations.BALANCED, label, file)
      text = open(path).read()
      for bigram in VOCABULARY:
        if bigram in text:
          counts[label] = counts[label] + 1

if __name__ == "__main__":

  counting()

