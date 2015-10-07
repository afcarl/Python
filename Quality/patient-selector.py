#!/usr/bin/python -B                                                                      

import csv, datetime

CSVFILE = '/Users/dima/Boston/Quality/Asthma/data.csv'

def find_severity_score_patients():
  """Patients for severy score compliance metric"""

  # 13 months expressed in days
  delta = datetime.timedelta(days = 396)
  dict_reader = csv.DictReader(open(CSVFILE, "rU"))
  print 'MRN', 'start_date', 'end_date'

  for line_num, line in enumerate(dict_reader):
    if line['DATE_OF_LAST_AAP'] == '':
      date_of_service = datetime.datetime.strptime(line['DATE_OF_SERVICE'], '%m/%d/%y')
      start_date = date_of_service - delta
      print line['MRN'], start_date.strftime('%m/%d/%y'), line['DATE_OF_SERVICE']

if __name__ == "__main__":
  
  find_severity_score_patients()


    
