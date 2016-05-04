#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python -B

import collections

PATH = '/Users/Dima/Loyola/Data/Thyme/events.txt'
EMBPATH = ''

class DatasetProvider:
  """Provide data"""

  def __init__(self, path=PATH):
    """Load data. Events are marked as [event_text]"""

    self.data = []
    self.labels = []
    
    for line in open(PATH):
      for token in line.split():
        if token.startswith('[') and token.endswith(']'):
          self.labels.append(1)   # this is an event
          self.data.append(token[1:-1])
        else:
          self.labels.append(0)   # this is not an event
          self.data.append(token)


  def map_to_vectors(self, path=EMBPATH):
    """Map words to vectors"""

    

if __name__ == "__main__":

  dataset = DatasetProvider()
  print len(dataset.data)
  print len(dataset.labels)
  print collections.Counter(dataset.labels)
  
