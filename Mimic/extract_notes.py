#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import pandas, string, os

NOTES_CSV = '/Users/Dima/Loyola/Data/MimicIII/NOTEEVENTS.csv'
OUT_DIR = 'Text/'
BATCH = 500000

if __name__ == "__main__":

  data_frame = pandas.read_csv(NOTES_CSV)

  for id, text in zip(data_frame.ROW_ID, data_frame.TEXT):
    out_dir = '%s/%s' % (OUT_DIR, id / BATCH)
    outfile = open('%s/%s.txt' % (out_dir, id), 'w')
    printable = ''.join(c for c in text if c in string.printable)
    outfile.write(printable)
