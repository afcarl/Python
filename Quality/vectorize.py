#!/usr/bin/python -B 
import collections, os

PATH = '/Users/Dima/Desktop/Text/'

def read_file(file):
  """Return a file as a list of words"""      
  
  words = []
  for line in open(file):
    for word in line.split():
      if word.isalpha():
        words.append(word.lower())
    
  return words

def make_alphabet():
  """Do a pass over corpus and generate unique words"""
  
  word_counts = collections.Counter()
  for file in os.listdir(PATH):
    words = read_file(PATH + file)
    word_counts.update(words)

  alphabet = []
  for word, count in word_counts.items():
    if count <= 10:
      alphabet.append(word)

  print len(alphabet), "\n"
  print alphabet

if __name__ == "__main__":

  make_alphabet()
