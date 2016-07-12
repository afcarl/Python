#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

data_file = '/Volumes/LsomVm/ards/data/ards_patient_notes_07112016.txt'
output_dir = '/Volumes/LsomVm/ards/text/'

if __name__ == "__main__":

  for line in open(data_file):
    elements = line.split('|')
    mrn = elements[0]
    text = elements[16]
    file_name = '%s/%s.txt' % (output_dir, mrn)
    out = open(file_name, 'a')
    out.write(text + '\n')
    out.close()
