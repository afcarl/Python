#!/usr/bin/python -B

"""
Convert WebKB dataset into this form:

- One file per instance
- A separate file mapping instances to labels
"""

PATH = '/Users/Dima/Boston/Data/WebKb/webkb-train-stemmed.txt'
OUTDIR = './Corpus/'
LABELS = './labels.txt'

if __name__ == "__main__":

  label_file = open(LABELS, 'w')
  for line_number, line in enumerate(open(PATH)):
    label, text = line.split('\t')
    label_file.write("%s|%s\n" % (line_number, label))
    document_path = "%s/%s.txt" % (OUTDIR, line_number)
    document_file = open(document_path, 'w')
    document_file.write(text + '\n')
