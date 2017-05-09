#! /usr/bin/env python
import pandas, string, os

NOTES_CSV = '/Users/Dima/Loyola/Data/MimicIII/Source/NOTEEVENTS.csv'
OUT_DIR = '/Users/Dima/Loyola/Data/MimicIII/PatientVec/Patients/'
BATCH = 500000

def write_to_single_dir():
  """Write files to one directory. Group by patient."""

  frame = pandas.read_csv(NOTES_CSV)

  for row_id, subj_id, text in zip(frame.ROW_ID, frame.SUBJECT_ID, frame.TEXT):
    outfile = open('%s%s.txt' % (OUT_DIR, subj_id), 'a')
    # outfile.write('* * * * * ROW_ID: %s * * * * * \n\n' % row_id)
    outfile.write(text + '\n')

def write_to_multiple_dirs():
  """Split input into files grouped in several directories"""

  data_frame = pandas.read_csv(NOTES_CSV)

  for id, text in zip(data_frame.ROW_ID, data_frame.TEXT):
    out_dir = '%s/%s' % (OUT_DIR, id / BATCH)
    outfile = open('%s/%s.txt' % (out_dir, id), 'w')
    printable = ''.join(c for c in text if c in string.printable)
    outfile.write(printable)

if __name__ == "__main__":

  write_to_single_dir()
