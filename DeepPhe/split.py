#!/usr/bin/python -B

import os, shutil

ALL = '/Users/dima/Boston/Data/DeepPhe/Metastasis/Anafora/All/'
DEV = '/Users/dima/Boston/Data/DeepPhe/Metastasis/Anafora/Dev/'
TRAIN = '/Users/dima/Boston/Data/DeepPhe/Metastasis/Anafora/Train/'
TEST = '/Users/dima/Boston/Data/DeepPhe/Metastasis/Anafora/Test/'

TRAINPATIENTS = set(['03', '11', '92', '93'])
DEVPATIENTS = set(['02', '21'])
TESTPATIENTS = set(['01', '16'])

if __name__ == "__main__":

  for dir in os.listdir(ALL):
    for patient_num in TESTPATIENTS:
      prefix = 'patient' + patient_num
      if dir.startswith(prefix):
        shutil.copytree(ALL + dir, TEST + dir)
