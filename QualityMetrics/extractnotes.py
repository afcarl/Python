#!/usr/bin/python -B
import csv, string, datetime

"""
A classification instance is an MRN + DATE_OF_SERVICE.
We need to save all notes for a patient with a given MRN
and a DATE_OF_SERVICE in a text file in the output directory.
Each instance (file) will be mapped to a label.
"""

# note csv file has the following columns: MRN, NOTES, Date
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

def map_instances_to_labels():
  """Save the mapping from file name to label"""
  
  label_file = open(LABELFILE, 'w')
  dict_reader = csv.DictReader(open(ASTHMACSV, "rU"))
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

  for start_date, end_date in mrn2dates[mrn]:
    if date >= start_date and date <= end_date:
      file_name = '%s/%s-%s.txt' % (OUTDIR, mrn, end_date.strftime('%m-%d-%Y'))
      return file_name
  
  # no date range found for this mrn/date
  # probably this mrn was seen multiple times
  # and for some of them DATA_REPORTING_TYPE is 0
  return None

def extract_notes(mrn2dates):
  """Read each row of a csv file into a dictionary"""

  dict_reader = csv.DictReader(open(NOTECSV))
  for line in dict_reader:
    if line['MRN'] not in mrn2dates:
      continue # we don't have labels for all mrns
    note_text = line['NOTES']
    only_printable = ''.join(c for c in note_text if c in string.printable)
    note_date = datetime.datetime.strptime(line['Date'], '%m/%d/%Y')
    outfile_name = map_date_to_file(mrn2dates, line['MRN'], note_date)
    if outfile_name != None:
      outfile = open(outfile_name, 'a') 
      # save note date in addition to note text for debugging
      output = 'note date: %s\n%s\n' % (line['Date'], only_printable)
      outfile.write(output)

if __name__ == "__main__":
  
  mrn2dates = map_patients_to_date_ranges()
  map_instances_to_labels()
  extract_notes(mrn2dates)
