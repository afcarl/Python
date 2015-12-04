#!/usr/bin/python -B

import csv, string, datetime, os.path, shutil

"""
A classification instance is an MRN + DATE_OF_SERVICE.
We need to save all notes for a patient with a given MRN
and a DATE_OF_SERVICE in a text file in the output directory.
Each instance (file) will be mapped to a label.
"""

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
    if date_of_service.month == 8 and date_of_service.year == 2015:
      continue # harry doesn't have the labeles for these now
    start_date = date_of_service - delta
    if line['MRN'] not in mrn2dates:
      mrn2dates[line['MRN']] = []
    mrn2dates[line['MRN']].append((start_date, date_of_service))

  return mrn2dates

def get_instance_to_label_map():
  """Save the mapping from file name to label"""

  # key: instance id (mrn + date of service), value: label
  labels = {}

  for line in csv.DictReader(open(ASTHMACSV, "rU")):
    if line['DATA_REPORTING_TYPE'] not in OK_DATA_REPORTING_TYPES:
      continue # they weren't labeled manually
    if line['DATE_OF_LAST_AAP'] != '':
      continue # pdf exists in powerchart
    if line['IS_SEVERITY_DOC_PPM'] == '':
      continue # no label for unknown reason
    date_of_service = datetime.datetime.strptime(line['DATE_OF_SERVICE'], '%m/%d/%y')
    if date_of_service.month == 8 and date_of_service.year == 2015:
      continue # harry doesn't have the labeles for these now
    file_name_no_ext = '%s-%s' % (line['MRN'], date_of_service.strftime('%m-%d-%Y'))
    label = line['IS_SEVERITY_DOC_PPM'] # this is the label, right?
    labels[file_name_no_ext] = label
    
  return labels

def map_to_file_names(mrn, date, mrn2dates, labels):
  """Map mrn and note date to correct patient file(s)"""

  # could be multiple files for some mrns
  # e.g. '1104576' had two visits several days apart
  # thus for this mrn we create two classification instances
  # all available notes should be written to files for both visits
  file_names = []

  for start_date, end_date in mrn2dates[mrn]:
    if date >= start_date and date <= end_date:
      id = '%s-%s' % (mrn, end_date.strftime('%m-%d-%Y'))
      label = 'Unknown'
      if id in labels:
        label = labels[id]      
      file_name = '%s/%s/%s.txt' % (OUTDIR, label, id)
      file_names.append(file_name)
  
  return file_names

def extract_notes(mrn2dates, labels):
  """Loop through notes and write them to files representing instances"""

  # note csv file has columns: MRN, NOTES, NOTE_DATE, CLINIC_DESCRIPTION 
  dict_reader = csv.DictReader(open(NOTECSV))
  
  for line in dict_reader:
    if line['MRN'] not in mrn2dates:
      continue # we don't have labels for all mrns
    note_text = line['NOTES']
    only_printable = ''.join(c for c in note_text if c in string.printable)
    note_date = datetime.datetime.strptime(line['NOTE_DATE'], '%Y/%m/%d')
    file_names = map_to_file_names(line['MRN'], note_date, mrn2dates, labels)
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

  # figure out what dates for an mrn to group together
  mrn2dates = map_patients_to_date_ranges()
  labels = get_instance_to_label_map()
  extract_notes(mrn2dates, labels)
