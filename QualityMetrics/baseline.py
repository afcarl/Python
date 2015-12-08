#!/usr/bin/python -B

import locations
import os

CLASSDIRS = ['Yes', 'No']
VOCABULARY = ['severe asthma', 'persistent asthma', 'mild asthma', 
              'intermittent asthma', 'moderate asthma']

def counting():
  """Count the number of times each vocabulary item is seen"""

  correct = 0
  incorrect = 0

  for label in CLASSDIRS:
    for file in os.listdir(locations.BALANCED + label):
      path = os.path.join(locations.BALANCED, label, file)
      text = open(path).read()
      for bigram in VOCABULARY:
        if bigram in text:
          # baselined labeled this document as a 'yes'
          if label == 'Yes':
            correct = correct + 1
          else:
            incorrect = incorrect + 1

  print correct, incorrect, float(correct) / (correct + incorrect)

if __name__ == "__main__":

  counting()

