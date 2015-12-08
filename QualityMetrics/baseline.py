#!/usr/bin/python -B

import locations
import os

CLASSDIRS = ['Yes', 'No']
KEYPHRASES = ['severe asthma', 'persistent asthma', 'mild asthma', 
              'intermittent asthma', 'moderate asthma']

def counting():
  """Count the number of times each vocabulary item is seen"""

  correct = 0
  incorrect = 0

  for label in CLASSDIRS:
    for file in os.listdir(locations.BALANCED + label):

      path = os.path.join(locations.BALANCED, label, file)
      document_text = open(path).read()
      key_phrase_seen = False
      for key_phrase in KEYPHRASES:
        if key_phrase in document_text:
          key_phrase_seen = True

      if key_phrase_seen:
        # baselined labeled this document as a 'yes'
        if label == 'Yes':
          correct = correct + 1
        else:
          incorrect = incorrect + 1
      else:
        # baseline labeled this document as a 'no'
        if label == 'Yes':
          incorrect = incorrect + 1
        else:
          correct = correct + 1

  print correct, incorrect, float(correct) / (correct + incorrect)

if __name__ == "__main__":

  counting()

