#!/usr/bin/python -B
import csv, string

# has the following columns:
# MRN, NOTES, Date
CSVFILE = '/Volumes/chip-nlp/Groups/QualityMetrics/Asthma/severity-score.csv'
OUTDIR = '/Volumes/chip-nlp/Groups/QualityMetrics/Asthma/Text/'

def extract_notes_via_dictionary():
  """Read each row of a csv file into a dictionary"""

  dict_reader = csv.DictReader(open(CSVFILE))
  for line in dict_reader:
    note_text = line['NOTES']
    only_printable = ''.join(c for c in note_text if c in string.printable)
    outfile_name = '%s/%s.txt' % (OUTDIR, line['MRN'])
    outfile = open(outfile_name, 'a') # multiple entries for a patient
    outfile.write(only_printable + '\n')

def extract_notes():
  """Read each row of a csv file into a list"""

  csv_reader = csv.reader(open(CSVFILE))
  header = csv_reader.next()
  for entry in csv_reader:
    mrn = entry[0]
    text = entry[1]
    outfile = open('Data/' + mrn + '.txt', 'w')
    outfile.write(text + '\n')

if __name__ == "__main__":
  
  extract_notes_via_dictionary()

    
