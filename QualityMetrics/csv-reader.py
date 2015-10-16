#!/usr/bin/python -B
import csv, string, datetime

# note csv file has the following columns:
# MRN, NOTES, Date
ASTHMACSV = '/Users/dima/Boston/QualityMetrics/Asthma/Data/data.csv'
NOTECSV = '/Users/dima/Boston/Data/QualityMetrics/Asthma/severity-notes.csv'
OUTDIR = '/Users/dima/Boston/Data/QualityMetrics/Asthma/Text/'

def map_patients_to_date_ranges():
  """Generate a patient to 13 month date range map"""

  # key: mrn, value: [(start_date1, end_date1), ...]
  # end date is date of service
  mrn2dates = {} 
  # 13 months expressed in days
  delta = datetime.timedelta(days = 396)

  dict_reader = csv.DictReader(open(ASTHMACSV, "rU"))
  for line in dict_reader:
    if line['DATE_OF_LAST_AAP'] == '':
      date_of_service = datetime.datetime.strptime(line['DATE_OF_SERVICE'], '%m/%d/%y')
      start_date = date_of_service - delta
      if line['MRN'] not in mrn2dates:
        mrn2dates[line['MRN']] = []
      mrn2dates[line['MRN']].append((start_date, date_of_service))

  return mrn2dates

def map_date_to_file(mrn2dates, mrn, date):
  """Map mrn and date to correct patient file"""

  for start_date, end_date in mrn2dates[mrn]:
    if date >= start_date and date <= end_date:
      file_name = '%s%s-%s.txt' % (OUTDIR, mrn, end_date.strftime('%m-%d-%Y'))
      return file_name

def extract_notes(mrn2dates):
  """Read each row of a csv file into a dictionary"""

  dict_reader = csv.DictReader(open(NOTECSV))
  for line in dict_reader:
    note_text = line['NOTES']
    only_printable = ''.join(c for c in note_text if c in string.printable)
    note_date = datetime.datetime.strptime(line['Date'], '%m/%d/%Y')
    outfile_name = map_date_to_file(mrn2dates, line['MRN'], note_date)
    outfile = open(outfile_name, 'a') 
    outfile.write(only_printable + '\n')

if __name__ == "__main__":
  
  mrn2dates = map_patients_to_date_ranges()
  extract_notes(mrn2dates)
