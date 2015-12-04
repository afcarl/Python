#!/usr/bin/python -B 
import csv, datetime

OK_DATA_REPORTING_TYPES = set(['1', '3'])

def severity_score_patients():
  """Patients for severy score compliance metric"""

  # 13 months expressed in days
  delta = datetime.timedelta(days = 396)
  dict_reader = csv.DictReader(open(ASTHMACSV, "rU"))
  print 'mrn', 'start_date', 'end_date', 'clinic'

  for line in dict_reader:
    if line['DATA_REPORTING_TYPE'] not in OK_DATA_REPORTING_TYPES:
      continue # not in the sample so no manual label
    if line['DATE_OF_LAST_AAP'] != '':
      continue # aap pdf is available
    if line['IS_SEVERITY_DOC_PPM'] == '':
      continue # no label for unknown reason
    date_of_service = datetime.datetime.strptime(line['DATE_OF_SERVICE'], '%m/%d/%y')
    if date_of_service.month == 8 and date_of_service.year == 2015:
      continue # harry doesn't have the labeles for these now
    start_date = date_of_service - delta
    print line['MRN'], start_date.strftime('%m/%d/%y'), \
          line['DATE_OF_SERVICE'], line['DATA_CLASS_TYPE']

def controller_medication_compliance():
  """Patients for controler medication compliance metric"""

  # 12 months expressed in days
  delta = datetime.timedelta(days = 365)
  dict_reader = csv.DictReader(open(ASTHMACSV, "rU"))
  print 'MRN', 'start_date', 'end_date'

  for line in dict_reader:
    if line['DATE_OF_LAST_AAP'] == '' and line['SEVERITY_PPM'] == 'Persistent':
      date_of_service = datetime.datetime.strptime(line['DATE_OF_SERVICE'], '%m/%d/%y')
      start_date = date_of_service - delta
      print line['MRN'], start_date.strftime('%m/%d/%y'), line['DATE_OF_SERVICE']

if __name__ == "__main__":
  
  severity_score_patients()




    
