#!/usr/bin/env python

import sys, pandas, string
sys.dont_write_bytecode = True

base = '/Users/Dima/Loyola/Mount/'
csv = base + 'ards/data/FinalDataSet_For_DimaDligach_7.11.2016.csv'
data = base + 'ards/data/ards_patient_notes_07112016.txt'
out = base + 'ards/text'

def map_mrn_to_label():
  """Dictionary mapping mrns to ards outcome"""

  mrn2label = {}
  dframe = pandas.read_csv(csv)
  for mrn, label in zip(dframe.mrn, dframe.ARDS_Final):
    mrn2label[mrn] = label.lower()

  return mrn2label

def organize_files():
  """ """
  
  mrn2label = map_mrn_to_label()
  
  for line in open(data):
    elements = line.split('|')
    mrn = int(elements[0])
    text = elements[16]
    printable = ''.join(c for c in text if c in string.printable)
    file_name = '%s/%s/%s.txt' % (out, mrn2label[mrn], mrn)
    out_file = open(file_name, 'a')
    out_file.write(printable + '\n')
    out_file.close()
    
if __name__ == "__main__":

  organize_files()
