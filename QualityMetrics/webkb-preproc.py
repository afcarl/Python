#!/usr/bin/python -B

TRAIN = '/Users/dima/Boston/Data/WebKb/webkb-train-stemmed.txt'
OUTDIR = '/Users/dima/Boston/Data/WebKb/Text/'
LABELFILE = '/Users/dima/Boston/Data/WebKb/labels.txt'

def main():
  """ """      
  
  label_file = open(LABELFILE, 'w')
  for linenum, line in enumerate(open(TRAIN)):
    label, text = line.split('\t')
    label_file.write('%d|%s\n' % (linenum, label))
    text_file_name = '%s%d.txt' % (OUTDIR, linenum)
    text_file = open(text_file_name, 'w')
    text_file.write(text)

if __name__ == "__main__":

  main()
