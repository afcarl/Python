#!/usr/bin/python -B

import csv, string, datetime, os.path, shutil

"""
A classification instance is an MRN + DATE_OF_SERVICE.
We need to save all notes for a patient with a given MRN
and a DATE_OF_SERVICE in a text file in the output directory.
Each instance (file) will be mapped to a label.
"""

ASTHMACSV = '/Users/dima/Boston/QualityMetrics/Asthma/Data/data.csv'
NOTECSV = '/Users/dima/Boston/Data/QualityMetrics/Asthma/severity-notes.csv'
OUTDIR = '/Users/dima/Boston/Data/QualityMetrics/Asthma/Text'
LABELFILE = '/Users/dima/Boston/Data/QualityMetrics/Asthma/labels.txt'
OK_DATA_REPORTING_TYPES = set(['1', '3'])

def map_patients_to_date_ranges():
  """Generate a patient to 13 month date range map"""

  # key: mrn, value: [(start_date1, end_date1), ...]
  # end date is date of service
  mrn2dates = {} 
  # 13 months expressed in days
  delta = datetime.timedelta(days = 396)

  dict_reader = csv.DictReader(open(ASTHMACSV, "rU"))
  for line in dict_reader:
    if line['DATA_REPORTING_TYPE'] not in OK_DATA_REPORTING_TYPES:
      continue # they weren't labeled manually
    if line['DATE_OF_LAST_AAP'] != '':
      continue # pdf exists in powerchart
    if line['IS_SEVERITY_DOC_PPM'] == '':
      continue # no label for unknown reason
    date_of_service = datetime.datetime.strptime(line['DATE_OF_SERVICE'], '%m/%d/%y')
    start_date = date_of_service - delta
    if line['MRN'] not in mrn2dates:
      mrn2dates[line['MRN']] = []
    mrn2dates[line['MRN']].append((start_date, date_of_service))

  return mrn2dates

def write_instance_to_label_map():
  """Save the mapping from file name to label"""

  dict_reader = csv.DictReader(open(ASTHMACSV, "rU"))
  label_file = open(LABELFILE, 'w')

  for line in dict_reader:
    if line['DATA_REPORTING_TYPE'] not in OK_DATA_REPORTING_TYPES:
      continue # they weren't labeled manually
    if line['DATE_OF_LAST_AAP'] != '':
      continue # pdf exists in powerchart
    if line['IS_SEVERITY_DOC_PPM'] == '':
      continue # no label for unknown reason
    date_of_service = datetime.datetime.strptime(line['DATE_OF_SERVICE'], '%m/%d/%y')
    file_name_no_ext = '%s-%s' % (line['MRN'], date_of_service.strftime('%m-%d-%Y'))
    label = line['IS_SEVERITY_DOC_PPM'] # this is the label, right?
    label_file.write('%s|%s\n' % (file_name_no_ext, label))

def map_date_to_file(mrn2dates, mrn, date):
  """Map mrn and date to correct patient file"""

  # could be multiple files for some mrns
  # e.g. '1104576' had two visits several days apart
  # thus for this mrn we create two classification instances
  # all available notes should be written to files for both visits
  file_names = []

  # need label to place file into the right dir
  labels = {}
  for line in open(LABELFILE):
    id, label = line.strip().split('|')
    labels[id] = label

  for start_date, end_date in mrn2dates[mrn]:
    if date >= start_date and date <= end_date:
      id = '%s-%s' % (mrn, end_date.strftime('%m-%d-%Y'))
      label = 'Unknown'
      if id in labels:
        label = labels[id]      
      file_name = '%s/%s/%s.txt' % (OUTDIR, label, id)
      file_names.append(file_name)
  
  return file_names

def extract_notes(mrn2dates):
  """Loop through notes and write them to files representing instances"""

  # note csv file has columns: MRN, NOTES, NOTE_DATE, CLINIC_DESCRIPTION 
  dict_reader = csv.DictReader(open(NOTECSV))
  
  for line in dict_reader:
    if line['MRN'] not in mrn2dates:
      continue # we don't have labels for all mrns
    note_text = line['NOTES']
    only_printable = ''.join(c for c in note_text if c in string.printable)
    note_date = datetime.datetime.strptime(line['NOTE_DATE'], '%Y/%m/%d')
    file_names = map_date_to_file(mrn2dates, line['MRN'], note_date)
    for outfile_name in file_names:
      outfile = open(outfile_name, 'a') 
      output = 'note date: %s\n%s\n' % (line['NOTE_DATE'], only_printable)
      outfile.write(output)

if __name__ == "__main__":

  if os.path.exists(OUTDIR):
    shutil.rmtree(OUTDIR)
  os.makedirs(OUTDIR)
  os.makedirs(OUTDIR + '/Yes')
  os.makedirs(OUTDIR + '/No')

  mrn2dates = map_patients_to_date_ranges()
  write_instance_to_label_map()
  extract_notes(mrn2dates)
