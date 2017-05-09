#! /usr/bin/env python
import pandas, string, os

CSV = '/Users/Dima/Loyola/Data/MimicIII/Source/DIAGNOSES_ICD.csv'
OUTFILE = '/Users/Dima/Loyola/Data/MimicIII/PatientVec/'

def subject_to_code_map():
  """Dictionary mapping subject ids to icd9 codes"""

  # read data frame from CSV file
  frame = pandas.read_csv(CSV)

  subj2codes = {} # key: subj_id, value: set of icd9 codes
  for subj_id, icd9_code in zip(frame.SUBJECT_ID, frame.ICD9_CODE):
    if subj_id not in subj2codes:
      subj2codes[subj_id] = set()
    subj2codes[subj_id].add(icd9_code)

  return subj2codes

if __name__ == "__main__":

  subj2codes = subject_to_code_map()
  for subj_id, codes in subj2codes.items():
    print subj_id, codes
